import os
import sys

from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")

client = genai.Client(api_key=api_key)

def main():
    args = sys.argv
    verbose = False
    
    for arg in args:
        if arg == "--verbose":
            verbose = True

    if len(args)<2:
        print('You should inform a prompt when running.')
        sys.exit(1)

    prompt = args[1]

    messages =[
        types.Content(role="user", parts=[types.Part(text=prompt)])
    ]

    response = client.models.generate_content(
        model='gemini-2.0-flash-001',
        contents=messages
    )

    if verbose:
        meta_data=response.usage_metadata
        print('User prompt:',prompt)
        print('Prompt tokens:',meta_data.prompt_token_count)
        print('Response tokens:',meta_data.candidates_token_count)

if __name__ == "__main__":
    main()
