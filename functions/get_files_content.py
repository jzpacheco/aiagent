import os

from config import config


def get_file_content(working_directory, file_path):
    relative_path = os.path.join(working_directory, file_path)
    abs_path = os.path.abspath(relative_path)

    if not abs_path.startswith(os.path.abspath(working_directory)):
        return f'Error: Cannot read "{file_path}" as it is outside permitted working directory'
    
    if not os.path.isfile(abs_path):
        return f'Error: File not found or is not a regular file: "{file_path}"'

    MAX_CONTENT_SIZE = config['MAX_TEXT_CHARACTERS']
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
