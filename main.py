from openai import OpenAI
# if using local api key (export OPENAI_API_KEY="your-api-key")
# from get_api_key import get_api_key
from dotenv import load_dotenv
from nutrition_counter import get_vals
import base64
import json
import sys

load_dotenv()

# if using local api key (export OPENAI_API_KEY="your-api-key")
# Initialize the OpenAI client with the API key
# client = OpenAI(api_key=get_api_key())

client = OpenAI()

if __name__ == "__main__":
    image_path = sys.argv[1]
    vals = get_vals(image_path)
    print(json.dumps(vals, indent=4))