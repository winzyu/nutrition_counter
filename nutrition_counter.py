from openai import OpenAI
# if using local api key (export OPENAI_API_KEY="your-api-key")
# from get_api_key import get_api_key
from dotenv import load_dotenv
import base64
import json
import sys

load_dotenv()
# if using local api key (export OPENAI_API_KEY="your-api-key")
# Initialize the OpenAI client with the API key
# client = OpenAI(api_key=get_api_key())

client = OpenAI()

def get_vals(image_path):
    with open(image_path, "rb") as image:
        base64_image = base64.b64encode(image.read()).decode("utf-8")

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {
                "role": "system",
                "content": """You're a nutritionist. A user sends you an image of a meal and you tell them the range of
                integer estimates for the number calories and grams of protein, carbohydrates, fat that are in it. 
                Use the following JSON format:
                {
                    "observation": "brief explanation of what you see in the image",
                    "reasoning": "reasoning for macronutrient and calorie estimates",
                    "food-items": [
                        "name": "food item name",
                        "calories" :[min, max],
                        "protein": [min, max],
                        "carb": [min, max],
                        "fat": [min, max]
                    ],
                    "meal": 
                    {
                        "name": "meal name",
                        "total-calories": [min, max],
                        "total-protein": [min, max],
                        "total-carb": [min, max],
                        "total-fat": [min, max]
                    }
                }"""
            },
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": "Tell me the caloric and macronutrient content of this meal."
                    },
                    {
                        "type": "image_url",
                        "image_url": { 
                            "url": f"data:image/jpeg;base64,{base64_image}", 
                        },
                    },
                ],
            }
        ],
        max_tokens=2000,
    )

    response_message = response.choices[0].message
    content = response_message.content

    return json.loads(content)