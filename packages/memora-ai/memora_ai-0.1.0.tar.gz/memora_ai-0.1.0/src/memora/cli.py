import argparse
from pathlib import Path
from .tuner import fine_tune
from .utils import show_progress

def create_parser():
    parser = argparse.ArgumentParser(prog="memora", description="🧠 Memora - Train Smarter, Not Harder.")
    
    subparsers = parser.add_subparsers(dest='command', required=True)

    train_parser = subparsers.add_parser('train', help='Start fine-tuning')
    train_parser.add_argument('--model', required=True, help="Model name (e.g. 'llama3')")
    train_parser.add_argument('--dataset', required=True, help="Path to dataset JSON")
    train_parser.add_argument('--output', default="./outputs/model", help="Output directory")
    
    subparsers.add_parser('list', help='List available models')
    
    return parser

def main():
    parser = create_parser()
    args = parser.parse_args()
    
    if args.command == 'train':

        Path(args.output).mkdir(parents=True, exist_ok=True)
        
        show_progress("starting", 0)
        fine_tune(
            model_name=args.model,
            dataset_path=args.dataset,
            output_dir=args.output
        )
    elif args.command == 'list':
        print("Available models:")
        print("- llama3\n- mistral\n- gemma")

if __name__ == "__main__":
    main()