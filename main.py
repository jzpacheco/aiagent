import os
import sys

from dotenv import load_dotenv
from google import genai
from google.genai import types

from call_function import available_functions, call_function
from config import MAX_AGENT_ITERATIONS
from prompts import system_prompt

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

    for _ in range(MAX_AGENT_ITERATIONS):
        try:
            final_response = generate_content(client, messages, verbose)
            if final_response:
                print('Final Response:\n', final_response)
                break
            
        except Exception as e:
            print(f"Error in generate_content: {e}")

def generate_content(client, messages, verbose):
    response = client.models.generate_content(
        model='gemini-2.0-flash-001',
        contents=messages,
        config=types.GenerateContentConfig(tools=[available_functions], system_instruction=system_prompt),
    )
    if verbose:
        meta_data=response.usage_metadata
        print('Prompt tokens:',meta_data.prompt_token_count)
        print('Response tokens:',meta_data.candidates_token_count)

    if response.candidates:
        for candidate in response.candidates:
            messages.append(candidate.content)

    func_calls = response.function_calls
    if not func_calls:
        return response.text

    function_responses = []
    for call in func_calls:
        function_call_result = call_function(function_call_part=call,verbose=verbose)
        func_response = function_call_result.parts[0].function_response

        if not func_response or not function_call_result.parts:
            raise Exception("No response  for function found!!")

        if verbose:
            print(f"-> {func_response.response}")
        function_responses.append(function_call_result.parts[0])

    if not function_responses:
        raise Exception("no function responses generated, exiting.")

    messages.append(
        types.Content(parts=function_responses, role='user')
    )
if __name__ == "__main__":
    main()
