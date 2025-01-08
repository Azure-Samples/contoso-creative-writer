import logging
import httpx
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Get the API key and endpoint from environment variables
api_key = os.getenv('AZURE_OPENAI_API_KEY')
endpoint = os.getenv('AZURE_OPENAI_ENDPOINT')

def list_fine_tuning_jobs() -> dict:
    """List fine-tuning jobs.
    
    Returns:
        dict: The response from the API containing the list of fine-tuning jobs.
    """
    try:
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {api_key}"
        }
        response = httpx.get(f"{endpoint}/openai/fine-tunes", headers=headers)
        response.raise_for_status()
        return response.json()
    except httpx.HTTPStatusError as e:
        logging.error(f"Error listing fine-tuning jobs: {e.response.text}")
        return None
    except Exception as e:
        logging.error(f"Unexpected error: {e}")
        return None

def upload_file_for_fine_tuning(file_path: str) -> dict:
    """Upload a file for fine-tuning.
    
    Args:
        file_path (str): The path to the file to be uploaded.
    
    Returns:
        dict: The response from the API after uploading the file.
    """
    try:
        headers = {
            "Authorization": f"Bearer {api_key}"
        }
        with open(file_path, 'rb') as file:
            files = {'file': file}
            response = httpx.post(f"{endpoint}/openai/files", headers=headers, files=files)
        response.raise_for_status()
        return response.json()
    except httpx.HTTPStatusError as e:
        logging.error(f"Error uploading file for fine-tuning: {e.response.text}")
        return None
    except Exception as e:
        logging.error(f"Unexpected error: {e}")
        return None

def create_fine_tuning_job(training_file_id: str, model: str = "davinci") -> dict:
    """Create a fine-tuning job.
    
    Args:
        training_file_id (str): The ID of the training file.
        model (str): The model to be fine-tuned. Default is "davinci".
    
    Returns:
        dict: The response from the API after creating the fine-tuning job.
    """
    try:
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {api_key}"
        }
        payload = {
            "training_file": training_file_id,
            "model": model
        }
        response = httpx.post(f"{endpoint}/openai/fine-tunes", headers=headers, json=payload)
        response.raise_for_status()
        return response.json()
    except httpx.HTTPStatusError as e:
        logging.error(f"Error creating fine-tuning job: {e.response.text}")
        return None
    except Exception as e:
        logging.error(f"Unexpected error: {e}")
        return None

def make_post_request(url: str, data: dict, headers: dict) -> dict:
    """Make a POST request.
    
    Args:
        url (str): The URL to make the POST request to.
        data (dict): The data to be sent in the POST request.
        headers (dict): The headers to be sent in the POST request.
    
    Returns:
        dict: The response from the API after making the POST request.
    """
    try:
        response = httpx.post(url, json=data, headers=headers)
        response.raise_for_status()
        return response.json()
    except httpx.HTTPStatusError as e:
        logging.error(f"Error making POST request: {e.response.text}")
        return None
    except Exception as e:
        logging.error(f"Unexpected error: {e}")
        return None

def azure_chat_completion_request(messages: list, deployment_id: str) -> str:
    """Make a chat completion request to Azure OpenAI.
    
    Args:
        messages (list): The list of messages to be sent in the chat completion request.
        deployment_id (str): The deployment ID for the chat completion request.
    
    Returns:
        str: The response content from the chat completion request.
    """
    try:
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {api_key}"
        }
        payload = {
            "deployment_id": deployment_id,
            "messages": messages
        }
        response = httpx.post(f"{endpoint}/openai/deployments/{deployment_id}/chat/completions", headers=headers, json=payload)
        response.raise_for_status()
        return response.json()["choices"][0]["message"]["content"].strip()
    except httpx.HTTPStatusError as e:
        logging.error(f"Error making chat completion request: {e.response.text}")
        return None
    except Exception as e:
        logging.error(f"Unexpected error: {e}")
        return None
