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
        commands = ['python' ,abs_path]
        if args:
            commands.extend(args)
        result = subprocess.run(
            commands,
            cwd=base_path,
            timeout=30,
            text=True,
            capture_output=True,
        )
        output= []
        if result.stdout:
            output.append(f"STDOUT:\n{result.stdout}")
        if result.stderr:
            output.append(f"STDERR:\n{result.stderr}")

        if result.returncode != 0 :
            output.append(f"Process exited with code {result.returncode}")

        return "\n".join(output) if output else "No outpu produced."
    except Exception as e:
        return f'Error: executing Python file: {e}'


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
