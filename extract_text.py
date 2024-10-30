import re
import json
import cv2
import pytesseract
pytesseract.pytesseract.tesseract_cmd = r'D:\Tesseract-OCR\tesseract.exe'
from PIL import Image
import numpy as np
import os

def extract_tweet_text(image_path):
    # Load the image
    image = Image.open(image_path)
    
    # Convert to grayscale to improve OCR results
    gray_image = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2GRAY)
    
    # Apply OCR to extract text
    text_output = pytesseract.image_to_string(gray_image)  # Default language (English)
    
    # Process the text to extract specific fields
    # Regex patterns to capture username, handle, and reply information
    username_pattern = re.search(r'^(.*?)\s*[@]', text_output)
    handle_pattern = re.search(r'@(\w+)', text_output)
    reply_to_pattern = re.search(r'Em resposta a @(\w+)', text_output)
    
    # Extract fields with fallback to None if not found
    username = username_pattern.group(1).strip() if username_pattern else None
    handle = f"@{handle_pattern.group(1).strip()}" if handle_pattern else None
    reply_to = f"@{reply_to_pattern.group(1).strip()}" if reply_to_pattern else None
    
    # Extract tweet content by skipping header lines
    text_lines = [line.strip() for line in text_output.splitlines() if line.strip()]
    tweet_content_lines = []
    header_ended = False
    for line in text_lines:
        if header_ended:
            tweet_content_lines.append(line)
        elif "Em resposta a @" in line or handle:
            # Start collecting tweet content after identifying header
            header_ended = True
    
    # Join tweet content lines
    tweet_content = " ".join(tweet_content_lines).strip()
    
    # Format the data as JSON
    tweet_data = {
        "username": username,
        "handle": handle,
        "reply_to": reply_to,
        "tweet_content": tweet_content
    }
    
    # Convert to JSON string with formatting
    json_output = json.dumps(tweet_data, indent=4, ensure_ascii=False)
    
    return json_output

# Define the path to the image file
image_path = os.path.join(os.getcwd(), 'teste.png')  # Assumes 'teste.png' is in the current directory

# Run the extraction function and print the result
print(extract_tweet_text(image_path))
