import openai
import requests
import json
import config
import os
from datetime import datetime
import prompt

prompt_ = prompt.text

# Define the API endpoint and your API key
api_url = "https://api.openai.com/v1/images/generations"
OPENAI_API_KEY= config.api_key
api_key = OPENAI_API_KEY


# Prepare the headers and payload for the API request
headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {api_key}"
}

data = {
    "model":"dall-e-3",
    "prompt": prompt_,
    "n": 1,
    "size":"1024x1024"
}

# Make the API request
response = requests.post(api_url, headers=headers, data=json.dumps(data))

# Handle the response and extract the generated image
if response.status_code == 200:
    response_data = response.json()
    image_url = response_data["data"][0]["url"]
    print("Generated image URL:", image_url)
else:
    print("Failed to generate image:", response.text)


# dowloand image and save prompt
def download_image_and_save_content(url, content, folder):
    # Create the folder if it doesn't exist
    if not os.path.exists(folder):
        os.makedirs(folder)

    # Get the current date and time
    now = datetime.now()

    # Format the date and time as a string
    timestamp = now.strftime("%Y%m%d_%H%M%S")

    # Get the image
    response = requests.get(url)

    # Check if the request is successful
    if response.status_code == 200:
        # Create the image file name
        image_file_name = f"{timestamp}.jpg"

        # Create the full image file path
        image_file_path = os.path.join(folder, image_file_name)

        # Write the image to a file
        with open(image_file_path, 'wb') as f:
            f.write(response.content)
        print(f"Image saved at {image_file_path}")
    else:
        print(f"Failed to download image from {url}")

    # Create the text file name
    text_file_name = f"{timestamp}.txt"

    # Create the full text file path
    text_file_path = os.path.join(folder, text_file_name)

    # Write the content to a file
    with open(text_file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"Content saved at {text_file_path}")

# Example usage
download_image_and_save_content(image_url, prompt_, 'images')
