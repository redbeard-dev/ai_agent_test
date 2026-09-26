import os

schema_get_files_info = {
    "type": "function",
    "function": {
        "name": "get_files_info",
        "description": "Lists files in a specified directory relative to the working directory, providing file size and directory status",
        "parameters": {
            "type": "object",
            "properties": {
                "directory": {
                    "type": "string",
                    "description": "Directory path to list files from, relative to the working directory (default is the working directory itself)",
                },
            },
        },
    },
}

def get_files_info(working_directory: str, directory: str = ".") -> str:
    try:
        working_dir_abs = os.path.abspath(working_directory)
        target_dir = os.path.normpath(os.path.join(working_dir_abs, directory))
        valid_target_dir = os.path.commonpath([working_dir_abs, target_dir]) == working_dir_abs
        files_string = "Result for current directory:" if directory == "." else f"Result for '{directory}' directory:"
        if not valid_target_dir:
            raise Exception(f'Cannot list "{directory}" as it is outside the permitted working directory')
        if not os.path.isdir(target_dir):
            raise Exception(f'"{directory}" is not a directory')
        with os.scandir(target_dir) as tdir:
            for file in tdir:
                files_string += f"\n- {file.name}: file_size={file.stat().st_size} bytes, is_dir={file.is_dir()}"
        return files_string
    except Exception as e:
        return files_string + f"\n    Error: {e}"
