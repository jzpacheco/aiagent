import os
import sys

from dotenv import load_dotenv
from google import genai
from google.genai import types

from call_function import available_functions
from system_prompt import system_prompt

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
        contents=messages,
        config=types.GenerateContentConfig(tools=[available_functions], system_instruction=system_prompt),
    )


    func_calls = response.function_calls
    if not func_calls:
        return response.text
    
    if func_calls:
        for call in func_calls:
            print(f"Calling function: {call.name}({call.args})")
    else:
        print(response.text)

    if verbose:
        meta_data=response.usage_metadata
        print('User prompt:',prompt)
        print('Prompt tokens:',meta_data.prompt_token_count)
        print('Response tokens:',meta_data.candidates_token_count)

if __name__ == "__main__":
    main()
