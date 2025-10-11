import os


def write_file(working_direcotry, file_path, content):
    base_path = os.path.abspath(working_direcotry)
    final_path = os.path.join(base_path,file_path)

    if not final_path.startswith(base_path):
        return f'Error: Cannot write to "{file_path}" as it is outside the permitted directory'

    dir_name = os.path.dirname(final_path)
    if not os.path.exists(dir_name):
        try:
            os.makedirs(dir_name)
        except Exception as e:
            return f'Error: {e}'


    try: 
        with open(final_path, 'w') as f:
            f.write(content)
    except Exception as e:
        return f'Error: {e}'

    return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'


