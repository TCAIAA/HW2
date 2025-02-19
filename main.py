import os
from pydantic import BaseModel, Field
from typing import List
from groq import Groq
import instructor

# Optional: Define a Pydantic model to structure the response from the API.
# This is just an example. Adjust fields based on the structure you expect 
from Groq.
class APIResponse(BaseModel):
    answer: str = Field(..., description="The answer provided by the Groq 
API")

# Retrieve the Groq API key from the environment variable.
groq_api_key = os.environ.get('GROQ_API_KEY')
if not groq_api_key:
    print("Error: GROQ_API_KEY is not set in your environment.")
    exit(1)

# Initialize the Groq client with your API key.
client = Groq(api_key=groq_api_key)

# Enhance the client using instructor to use TOOLS mode.
client = instructor.from_groq(client, mode=instructor.Mode.TOOLS)

def ask_groq(question: str):
    """
    Sends the provided question to the Groq API and returns the response.
    """
    response = client.chat.completions.create(
        model="mixtral-8x7b-32768",  # Example model
        messages=[
            {"role": "user", "content": question}
        ],
        # If you want to validate the response with a Pydantic model, 
uncomment:
        # response_model=APIResponse,
    )
    return response

def main():
    print("Welcome to the Groq Chat!")
    print("Type your question below, or type 'quit' to exit.")

    while True:
        user_input = input("Your question: ").strip()
        if user_input.lower() == "quit":
            print("Goodbye!")
            break

        try:
            # Get the response from the Groq API.
            response = ask_groq(user_input)
            print("Response from Groq API:")
            # Print the full JSON response with indentation.
            print(response.model_dump_json(indent=2))
        except Exception as e:
            print(f"An error occurred while processing your request: {e}")

if __name__ == '__main__':
    main()

