import os
import time
import sys
import requests
import webbrowser
from getpass import getpass
from transformers import (
    AutoModelForCausalLM, 
    AutoTokenizer, 
    TrainingArguments,
    Trainer
)
from huggingface_hub import login, HfFolder, ModelCard
from .utils import show_progress
from .optim import apply_optimizations

def _get_masked_input(prompt):
    """Get input with masked display"""
    if sys.stdin.isatty():
        return getpass(prompt)
    return input(prompt)

def _check_model_access(model_name, token):
    """Check if model requires and has accepted license"""
    try:
        api_url = f"https://huggingface.co/api/models/{model_name}"
        headers = {"Authorization": f"Bearer {token}"} if token else {}
        
        response = requests.get(api_url, headers=headers, timeout=10)
        response.raise_for_status()
        
        model_data = response.json()
        if model_data.get("gated", False):
            print(f"\n🔒 Model requires access approval: {model_name}")
            print(f"License: {model_data.get('cardData', {}).get('license', 'Unknown')}")
            
            model_url = f"https://huggingface.co/{model_name}"
            try:
                webbrowser.open(model_url)
                print(f"Opened model page in your browser: {model_url}")
            except Exception:
                print(f"Please visit: {model_url}")
            
            while True:
                response = input("Have you accepted the terms? (y/n) [n]: ").lower()
                if response == 'y':
                    return True
                elif response == 'n':
                    return False
                print("Please answer 'y' or 'n'")
        return True
    except Exception:
        return True

def _get_hf_token():
    """Get HF token from multiple sources with priority:
    1. Existing cached token
    2. Environment variable (HF_TOKEN)
    3. Interactive prompt
    """

    token = HfFolder.get_token()
    if token:
        return token
        
    token = os.getenv("HF_TOKEN")
    if token:
        if not token.startswith("hf_"):
            raise ValueError("Environment token must start with 'hf_'")
        HfFolder.save_token(token)
        return token
        
    print("\n🔑 Hugging Face authentication required")
    print("1. Get your token at: https://huggingface.co/settings/tokens")
    print("2. Make sure it has 'read' access")
    token = _get_masked_input("Enter your HF token (will be hidden): ")
    
    if not token.startswith("hf_"):
        raise ValueError("Token must start with 'hf_'")
        
    HfFolder.save_token(token)
    return token

def _load_model_with_retry(model_name, token, max_retries=2):
    """Attempt to load model with retries for gated models"""
    for attempt in range(max_retries):
        try:
            model = AutoModelForCausalLM.from_pretrained(
                model_name,
                token=token,
                trust_remote_code=True
            )
            tokenizer = AutoTokenizer.from_pretrained(
                model_name,
                token=token
            )
            return model, tokenizer
        except Exception as e:
            if attempt == max_retries - 1:
                raise
            print(f"\n⚠️ Attempt {attempt + 1} failed: {str(e)}")
            if not _check_model_access(model_name, token):
                raise RuntimeError(f"Access not granted for {model_name}")
            print("Retrying...")

def fine_tune(model_name, dataset, output_dir, epochs=3, batch_size=4, learning_rate=5e-5):
    """Main fine-tuning function."""

    show_progress("initializing", 0)
    
    try:
        token = _get_hf_token()
        login(token=token)
        
        if not _check_model_access(model_name, token):
            raise RuntimeError(f"Model access not granted for {model_name}")
            
    except Exception as e:
        show_progress("error", 0)
        print(f"\n❌ Authentication failed: {str(e)}")
        print("\n💡 Required steps:")
        print(f"1. Visit https://huggingface.co/{model_name.split('/')[0]}")
        print("2. Accept the model terms")
        print("3. Get your access token from settings")
        print("4. Either:")
        print("   - Run: huggingface-cli login")
        print("   - Set HF_TOKEN environment variable")
        raise
    
    show_progress("loading_model", 20)
    try:
        model, tokenizer = _load_model_with_retry(model_name, token)
    except Exception as e:
        show_progress("error", 20)
        print(f"\n⚠️ Model loading failed: {str(e)}")
        print("\n🔧 Common fixes:")
        print("- Accept model terms at HF website")
        print("- Check token has correct permissions")
        print("- Verify model name format (org/model)")
        print("- Try again in 5 minutes (access may take time to propagate)")
        raise
    
    show_progress("optimizing", 40)
    model = apply_optimizations(model)
    
    show_progress("preparing_data", 60)
    tokenized_dataset = dataset.map(lambda x: tokenizer(x["text"], truncation=True), batched=True)
    
    show_progress("setting_up", 80)
    training_args = TrainingArguments(
        output_dir=output_dir,
        num_train_epochs=epochs,
        per_device_train_batch_size=batch_size,
        learning_rate=learning_rate,
        save_strategy="epoch",
        logging_dir='./logs',
    )
    
    show_progress("training", 90)
    trainer = Trainer(
        model=model,
        args=training_args,
        train_dataset=tokenized_dataset,
    )
    
    trainer.train()
    
    show_progress("saving", 95)
    model.save_pretrained(output_dir)
    tokenizer.save_pretrained(output_dir)
    
    show_progress("complete", 100)
    print("\n🎉 Fine-tuning completed successfully! 🎉\n")