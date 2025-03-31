import json
import time
from datasets import load_dataset as hf_load_dataset

def load_dataset(file_path):
    """Load dataset from file or Hugging Face."""
    if file_path.endswith('.json'):
        with open(file_path, 'r') as f:
            return json.load(f)
    else:
        return hf_load_dataset(file_path)

def show_progress(stage, percentage):
    """Show ASCII animations for different stages."""
    animations = {
        "initializing": ["⚡ Initializing...", "🛠️  Setting up environment"],
        "loading_model": ["📦 Loading model...", "🤖 Preparing LLM"],
        "optimizing": ["⚙️ Applying optimizations...", "🚀 Boosting performance"],
        "preparing_data": ["📊 Loading dataset...", "✂️ Tokenizing data"],
        "setting_up": ["🔧 Configuring training...", "🎛️ Setting parameters"],
        "training": ["🏋️ Training model...", "🧠 Learning patterns"],
        "saving": ["💾 Saving model...", "📂 Creating checkpoints"],
        "complete": ["✅ Done!", "🎊 Process completed!"]
    }
    
    bar_length = 30
    filled = int(bar_length * percentage / 100)
    bar = '█' * filled + '-' * (bar_length - filled)
    
    frames = animations.get(stage, ["Working...", "Processing..."])
    frame = frames[int(time.time() * 2) % len(frames)]
    
    print(f"\r{frame} |{bar}| {percentage}%", end="", flush=True)
    
    if percentage == 100:
        print()