import os
import pandas as pd
import tiktoken
from openai import OpenAI
from collections import defaultdict
import re

# Retrieve API key from environment variable
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    raise ValueError("Error: OPENAI_API_KEY environment variable not set.")

# Initialize OpenAI client
client = OpenAI(api_key=api_key)

def generate_prompt(placeholders, user_prompt, system_prompt):
    """Generate the full prompt for GPT queries."""
    # Include the expected response format in the system message
    default_system_message = "You are a helpful assistant. You're a professional data analysis scientist." 
    identifier_placeholder_system = re.findall(r"{(.*?)}", system_prompt)
    # system_message = f"{system_prompt.format_map({key: placeholders.get(key, f"{{{key}}}") for key in identifier_placeholder_system}) if system_prompt else default_system_message}"
    if system_prompt:
        mapping = {key: placeholders.get(key, f"{{{key}}}") for key in identifier_placeholder_system}
        system_message = system_prompt.format_map(mapping)
    else:
        system_message = default_system_message
    # Fill the user_prompt with provided placeholders
    identifier_placeholder_user = re.findall(r"{(.*?)}", user_prompt)
    user_message = user_prompt.format_map({key: placeholders.get(key, f"{{{key}}}") for key in identifier_placeholder_user})
    return system_message, user_message

def count_tokens(text):
    """Calculate the number of tokens in a text"""
    enc = tiktoken.encoding_for_model("gpt-4")
    return len(enc.encode(text))

def query_gpt(system_message, user_message):
    """Send a query to GPT and return the result"""
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": system_message},
            {"role": "user", "content": user_message}
        ]
    )
    return response.choices[0].message.content

def execute_prompt(placeholders, user_prompt, system_prompt):
    """Encapsulate GPT query to maintain uniform invocation"""
    system_message, user_message = generate_prompt(placeholders, user_prompt, system_prompt)
    return query_gpt(system_message, user_message)

def load_data(file_path):
    """Load CSV data"""
    try:
        water_data = pd.read_csv(file_path)
        print(f"Data loaded successfully! {water_data.shape[0]} rows, {water_data.shape[1]} columns.")
        return water_data
    except FileNotFoundError:
        print(f"Error: Data file not found at '{file_path}'. Ensure the file exists.")
        exit()
