import os
import sys

from dotenv import load_dotenv
from google import genai

load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")

client = genai.Client(api_key=api_key)

def main():
    args = sys.argv
    if len(args)<2:
        print('You should inform a prompt when running.')
        sys.exit(1)

    prompt = args[1]
    response = client.models.generate_content(
        model='gemini-2.0-flash-001',
        contents=prompt
    )

    meta_data=response.usage_metadata
    print('Prompt tokens:',meta_data.prompt_token_count)
    print('Response tokens:',meta_data.candidates_token_count)

if __name__ == "__main__":
    main()
