import os

def read_api_key(file_path):
    with open(file_path, "r") as file:
        return file.read().strip()

def get_api_key():

    # Get the directory of the current script
    current_dir = os.path.dirname(os.path.abspath(__file__))

    # Construct the path to the API key file
    api_key_path = os.path.join(os.path.dirname(current_dir), 'OPENAI_API_KEY')

    # Read the API key
    api_key = read_api_key(api_key_path)

    return api_key