import requests
import os
from pydantic import BaseModel, Field
from typing import List
import instructor
from groq import Groq  # Ensure this import is correct

# Data structure to store topic details
class TopicDetails(BaseModel):
    title: str
    facts: List[str] = Field(..., description="A list of interesting facts about the given topic")

# Function to take user input
def prompt_user():
    return input("Enter a subject to explore (or type 'exit' to stop): ")

# Function to fetch information about a topic
def fetch_topic_info(topic):
    api_key = os.getenv("GROQ_API_KEY")  # More generic and flexible way to retrieve API key
    if not api_key:
        print("Error: API key is missing. Please set the 'GROQ_API_KEY' environment variable.")
        return

    try:
        # Initialize API client
        client = Groq(api_key=api_key)
        client = instructor.from_groq(client, mode=instructor.Mode.JSON)

        # Send request to AI model
        response = client.chat.completions.create(
            model="mixtral-8x7b-32768",
            messages=[{"role": "user", "content": f"Provide some insights on {topic}"}],
            response_model=TopicDetails  
        )

        # Output the formatted response
        print(response.model_dump_json(indent=2))  

    except Exception as error:
        print(f"Something went wrong: {error}")

# Main script execution
if _name_ == "_main_":
    while True:
        user_input = prompt_user()
        if user_input.strip().lower() == 'exit':
            print("Goodbye! Exiting the program.")
            break
        fetch_topic_info(user_input)
