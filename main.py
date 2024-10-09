import argparse
import os
from src import openai_service

def main():
    # Set up argument parser
    parser = argparse.ArgumentParser(description="OpenAI API Process Manager")
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # Upload dataset command
    upload_parser = subparsers.add_parser("upload", help="Upload a dataset file")
    upload_parser.add_argument("--file", type=str, help="Path to the dataset file (.jsonl)", required=False)

    # Fine-tune command
    finetune_parser = subparsers.add_parser("tune", help="Fine-tune a model with the dataset")
    finetune_parser.add_argument("file_id", type=str, help="File ID of the uploaded dataset")
    finetune_parser.add_argument("--model", type=str, default="gpt-4o-mini-2024-07-18", help="Base model to fine-tune (default: gpt-4o-mini-2024-07-18)")

    # Generate response command
    generate_parser = subparsers.add_parser("generate", help="Generate a response using a fine-tuned model")
    generate_parser.add_argument("prompt", type=str, help="Prompt or input text")
    generate_parser.add_argument("--model_id", type=str, default="fine-tuned-model-id", help="Fine-tuned model ID")
    generate_parser.add_argument("--max_tokens", type=int, default=500, help="Max tokens for the response (default: 500)")

    # Check fine-tuning status command
    check_parser = subparsers.add_parser("check", help="Check the status of a fine-tuning job")
    check_parser.add_argument("fine_tune_id", type=str, help="Fine-tuning job ID to check status")

    # Parse the arguments
    args = parser.parse_args()

    if args.command == "upload":
        # Upload dataset
        file_id = openai_service.upload_dataset()
        errMsg = "Error: Could not retrieve the file ID from the response."
        msg = f"Dataset uploaded successfully: {file_id}" if file_id != None else errMsg
        print(msg)

    elif args.command == "tune":
        # Start fine-tuning
        file_id = openai_service.start_finetune(args.file_id)
        print(file_id)

    elif args.command == "generate":
        # Generate response
        response = openai_service.generate_response(args.prompt, args.model_id, args.max_tokens)
        print(response)

    elif args.command == "check":
        # Check fine-tuning status
        openai_service.check_finetune_status(args.fine_tune_id)

    else:
        parser.print_help()

if __name__ == "__main__":
    main()