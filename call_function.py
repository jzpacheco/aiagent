from google.genai import types

from functions.get_files_content import (get_file_content,
                                         schema_get_file_content)
from functions.get_files_info import get_files_info, schema_get_files_info
from functions.run_python_file import run_python_file, schema_run_python_file
from functions.write_file import schema_write_file, write_file

functions_list = [
    get_file_content,
    get_files_info,
    run_python_file,
    write_file
]

functions_to_call = {f'{f.__name__}': f for f in functions_list}
def call_function(function_call_part, verbose=False):
    func_name = function_call_part.name
    func_args = function_call_part.args

    if verbose:
        print(f"Calling function: {func_name}({func_args})")
    else:
        print(f" - Calling function: {func_name}")

    try:

        func = functions_to_call[func_name]
    except Exception:
        return types.Content(
            role="tool",
            parts=[
                types.Part.from_function_response(
                    name=func_name,
                    response={"error": f"Unknown function: {func_name}"}
                )
            ]
        )

    func_result = func(working_directory="./calculator",**func_args)
    print('f', func_result)
    return types.Content(
        role="tool",
        parts=[
            types.Part.from_function_response(
                name=func_name,
                response={"result":func_result}
            )
        ]
    )

schemas = [
        schema_get_files_info,
        schema_get_file_content,
        schema_run_python_file,
        schema_write_file,
    ]

available_functions = types.Tool(function_declarations=schemas)
