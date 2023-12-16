import os
import requests
from openai import OpenAI
import pandas as pd
import json

import warnings

warnings.warn("This function is deprecated and will be removed in the future.")

# Read the JSON data from a file
with open('pods.json', 'r') as file:
    json_data = json.load(file)

# Convert the JSON data to a pandas DataFrame
df = pd.DataFrame(json_data)

import datetime

current_time = datetime.datetime.now().time()

formatted_time = current_time.strftime("%Y-%m-%d %H:%M")


client = OpenAI()

# Define the color palette
colors = [
    "rgb(41,183,122,1)",
    "rgb(226,30,34,1)",
    "rgb(99,199,241,1)"
]

# Folder to save the generated images
output_folder = "icons"

# Create the output folder if it doesn't exist
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

# Loop over the array and generate an image for each team name with the specified color palette
for index, row in df.iterrows():
    if(index > 178 and index < 350):
        # You can access data in 'row' using column names
        print(f"Index: {index}, Data: {row['name']}")
        color = colors[index % len(colors)]  # Cycle through the color palette
        response = client.images.generate(
            model="dall-e-3",
            prompt=f"A abstract Team icon for a team called {row['name']}, no gender preference, round icon, and a solid white background use the following colours {color}. Only generate icon",
            n=1,
            size="1024x1024",
            style="vivid"

        )

        # Get the URL of the generated image
        image_url = response.data[0].url

        # Construct the image filename using the team name
        image_filename = os.path.join(output_folder, f"{row['teambook']}.png")

        # Download the image and save it with the team name as the filename
        with open(image_filename, 'wb') as img_file:
            img_file.write(requests.get(image_url).content)

        print(f"Generated image for {row['name']} saved as {row['teambook']}")
