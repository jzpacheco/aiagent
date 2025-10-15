import os
import subprocess

from google.genai import types


def run_python_file(working_directory, file_path, args=[]):
    base_path = os.path.abspath(working_directory)
    abs_path= os.path.abspath(os.path.join(base_path, file_path))

    if not abs_path.startswith(base_path):
        return f'Error: Cannot execute "{file_path}" as it is outside the permitedd working directory'

    if not os.path.exists(abs_path):
        return f'Error: File "{file_path}" not found.'

    if not file_path.endswith(".py"):
        return f'Error: "{file_path}" is not a Python file.'

    try:
        process = subprocess.run(
            cwd=base_path,
            timeout=30,
            capture_output=True,
            args=['python' ,abs_path]+ args,
        )
        output= process.stdout
        if not output:
            return 'No output produced'

        return_code = process.returncode
        formatted_output = f"STDOUT: {process.stdout}\n STDERR: {process.stderr}"
        if return_code != 0 :
            formatted_output += f"\nProcess exited with code {return_code}"

        return formatted_output

    except Exception as e:
        return f'Error: executing file: {e}'


schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Run a python file found in the specified file_path, constrained to the working directory.",
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
