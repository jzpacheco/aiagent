import os


def _get_file_data(file_path:str):
    return os.path.getsize(file_path), os.path.isdir(file_path) 

def get_files_info(working_directory:str, directory:str="."):
    path_working_dir = os.path.abspath(working_directory)
    path_dir = os.path.join(path_working_dir,directory)
    abs_path_dir = os.path.abspath(path_dir) 

    if not abs_path_dir.startswith(path_working_dir):
        return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'

    if not os.path.isdir(path_dir):
        return f'Error: "{directory}" is not a directory'

    files_info=[]
    for content in os.listdir(path_dir):
        data = _get_file_data(os.path.join(abs_path_dir,content))
        files_info.append(f'- {content}: file_size={data[0]}, is_dir={data[1]}')

    return "\n".join(files_info)
