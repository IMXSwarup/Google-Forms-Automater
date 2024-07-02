#YOU NEED TO REPLACE WITH TARGEET FORM URL
#File paths is used to point to required name, emails, etc wordlists.
#IMPORTANT: You need to replace each ENTRY FIELDS for all question in google form. (use Dev tools or Burpsuite etc to find out the ENTRY FIELDS values)
#Don't decreament the delay less than 5 seconds due to rate limit.
#The Cookie: S=spreadsheet_forms=... and fbzx parameters are chnaged every iteration to avoid detection of duplication/spamming of submission.

#Code by IMXSwarup , beware...


import requests
import json
import time
import random
from openpyxl import load_workbook

# Load candidate names from the Excel file
file_path = "list.xlsx"
workbook = load_workbook(file_path)
sheet = workbook.active
candidate_names = [cell.value for cell in sheet['A']]

# Shuffle candidate names to ensure they are used in a random order
random.shuffle(candidate_names)

# Function to generate a new fbzx value
def generate_fbzx():
    return str(random.randint(-999999999999999999, 999999999999999999))

# Function to generate a new Cookie value
def generate_cookie():
    return f"S=spreadsheet_forms={random.getrandbits(128)}"

# Function to log the submission details
def log_submission(details):
    with open("submission_log.txt", "a") as log_file:
        log_file.write(f"{details}\n")

# Set the Google Form URL and base payload
form_url = "https://docs.google.com/forms/x/x/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/formResponse"  #INSERT APPROPRIATE FORM URL
base_payload = {
    "entry.1759616638": "",  # Name
    "entry.1481013056": "",  # Stream
    "fvv": "1",
    "partialResponse": "[null,null,\"-431461670862370928\"]",
    "pageHistory": "0",
    "fbzx": "",
    "submissionTimestamp": ""
}

# Random selection options
streams = ["CSE A", "CSE B", "IT", "ECE", "BT"]
participation_options = ["DANCE", "MUSIC", "DRAMA", "ANCHORING", "VOLUNTEERS"]

# Delay between submissions
delay = 5  # Initial delay in seconds

# Main loop for form submissions
i = 0
while True:
    # Select a candidate name randomly
    candidate_name = random.choice(candidate_names)
    
    # Update payload
    base_payload["entry.1759616638"] = candidate_name
    base_payload["entry.1481013056"] = random.choice(streams)
    # Select one or more participation options
    selected_participation = random.sample(participation_options, random.randint(1, len(participation_options)))
    
    # Prepare the data payload
    payload = base_payload.copy()
    payload["fbzx"] = generate_fbzx()
    payload["submissionTimestamp"] = str(int(time.time() * 1000))
    
    # Add selected participation options
    participation_payload = [(f"entry.1143085508", option) for option in selected_participation]
    
    # Flatten payload for multiple participation
    data = {**payload, **dict(participation_payload)}
    
    # Update headers
    headers = {
        "Host": "docs.google.com",
        "Cookie": generate_cookie(),
        "Content-Length": str(len(json.dumps(payload))),
        "Cache-Control": "max-age=0",
        "Sec-Ch-Ua": '"Not/A)Brand";v="8", "Chromium";v="126"',
        "Sec-Ch-Ua-Mobile": "?0",
        "Sec-Ch-Ua-Platform": "Windows",
        "Accept-Language": "en-GB",
        "Upgrade-Insecure-Requests": "1",
        "Origin": "https://docs.google.com",
        "Content-Type": "application/x-www-form-urlencoded",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.6478.57 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
        "X-Client-Data": "CJr5ygE=",
        "Sec-Fetch-Site": "same-origin",
        "Sec-Fetch-Mode": "navigate",
        "Sec-Fetch-User": "?1",
        "Sec-Fetch-Dest": "document",
        "Referer": f"https://docs.google.com/forms/x/x/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/viewform?fbzx={payload['fbzx']}",    #INSERT APPROPRIATE FORM URL
        "Accept-Encoding": "gzip, deflate, br",
        "Priority": "u=0, i",
    }
    
    # Retry mechanism
    max_retries = 5
    retry_delay = delay
    for attempt in range(max_retries):
        try:
            # Submit the form
            response = requests.post(form_url, headers=headers, data=data)
            if response.status_code == 200:
                break
        except requests.exceptions.RequestException as e:
            print(f"Attempt {attempt + 1} failed: {e}")
            time.sleep(retry_delay)
            retry_delay *= 2  # Exponential backoff

    if response.status_code != 200:
        print(f"Failed to submit after {max_retries} attempts.")
        continue
    
    # Log the submission details
    submission_details = {
        "Iteration": i + 1,
        "Status Code": response.status_code,
        "Name": candidate_name,
        "Stream": payload["entry.1481013056"],
        "Participation": ", ".join(selected_participation),
        "Timestamp": payload["submissionTimestamp"]
    }
    log_submission(submission_details)
    
    print(f"Iteration {i + 1}: Status Code {response.status_code}")
    print(f"Used Name: {candidate_name}, Stream: {payload['entry.1481013056']}, Participation: {', '.join(selected_participation)}")
    
    # Increment the counter
    i += 1
    
    # Sleep for the specified delay
    time.sleep(delay)
