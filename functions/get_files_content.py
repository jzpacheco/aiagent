import os

from google.genai import types

from config import MAX_CONTENT_SIZE


def get_file_content(working_directory, file_path):
    relative_path = os.path.join(working_directory, file_path)
    abs_path = os.path.abspath(relative_path)

    if not abs_path.startswith(os.path.abspath(working_directory)):
        return f'Error: Cannot read "{file_path}" as it is outside permitted working directory'
    
    if not os.path.isfile(abs_path):
        return f'Error: File not found or is not a regular file: "{file_path}"'

    try:
        with open(abs_path, 'r') as f:
            content = f.read(MAX_CONTENT_SIZE) 
            if os.path.getsize(abs_path) > MAX_CONTENT_SIZE:
                content+= (
                        f'[...File "{file_path}" truncated at {MAX_CHARS} characters]'
                    )

        return content
    except Exception as e:
        return f'Error reading file "{file_path}": {e}'

schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description="Get file content from a specified path, constrained to the working directory.",
    parameters= types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The path to the file that content will be read, relative to the working directory.",
            )
        }
    )
)
