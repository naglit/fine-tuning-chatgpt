import openai
from openai import OpenAI
from src.pyutil.util import file_query_repository as repo
from src.configs import config

OPENAI_APIKEY = "openai_apikey"
FT_MODEL = "ft_model"
openai.api_key = repo.read_json(config.get_config_file_path())[OPENAI_APIKEY]

def upload_dataset(filepath = "./fine_tuning.jsonl") -> str:
    """
    Upload the dataset to OpenAI for fine-tuning using the new API.

    :param file_path: Path to the dataset file
    :return: The uploaded file ID
    """
    try:
        print(f"Upload {filepath}")

        # Open the file in binary mode and upload
        with open(filepath, 'rb') as f:
            response = openai.files.create(
                file=f,
                purpose='fine-tune'
            )
        
        # Since the response might not be subscriptable, check the attributes
        file_id = getattr(response, 'id', None)
        
        if file_id:
            return file_id
        else:
            return None
    
    except Exception as e:
        print(f"Error uploading file: {e}")
        return None

def start_finetune(file_id):
    """
    Start the fine-tuning process with the uploaded file.

    :param file_id: The file ID of the uploaded dataset
    :return: The fine-tuning job response
    """
    try:
        config_path = config.get_config_file_path()
        model = repo.read_json(config_path)[FT_MODEL]

        response = openai.fine_tuning.jobs.create(
            training_file=file_id,
            model=model
        )

        fine_tune_id = getattr(response, 'id', None)
        
        if fine_tune_id and response.error != "":
            print(f"Fine-tuning started successfully: {fine_tune_id}")
            return response
        else:
            print("Error: Could not retrieve the fine-tuning job ID from the response.")
            return None
    except Exception as e:
        print(f"Error starting fine-tuning: {e}")
        return None

def generate_response(content, model_id="fine-tuned-model-id", max_tokens=100):
    """
    This method takes a prompt and generates a response using the fine-tuned model.

    :param prompt: The input text or question to generate a response for
    :param model_id: The ID of the fine-tuned model to use
    :param max_tokens: The maximum number of tokens in the response
    :return: The generated response as a string
    """
    try:
        prompt = [
            {"role": "user", "content": content }
        ]
        # Create a completion request to OpenAI API
        response = openai.chat.completions.create(
            model=model_id,
            messages=prompt,
            max_tokens=max_tokens
        )
        
        # Return the generated text from the response
        return response.choices[0].message.content.strip()
    
    except Exception as e:
        return f"An error occurred: {e}"
    
def check_finetune_status(fine_tune_id):
    """
    Check the status of the fine-tuning job.

    :param fine_tune_id: The fine-tuning job ID
    :return: Status of the fine-tuning job
    """
    try:
        # Retrieve the fine-tuning job details
        response = openai.fine_tuning.jobs.retrieve(fine_tune_id)
        print(response)
        # Access the attributes using dot notation
        print(f"Fine-tuning status: {response.status}")
        
        if response.fine_tuned_model:
            print(f"Fine-tuned model ID: {response.fine_tuned_model}")
        else:
            print("The fine-tuning process has not completed yet.")
    except Exception as e:
        print(f"Error retrieving fine-tuning status: {e}")
