import os

schema_write_file = {
    "type": "function",
    "function": {
        "name": "write_file",
        "description": "Writes a specified text into a specified file, overwriting its previous content.",
        "parameters": {
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": "File path of file to write to including the file name itself, relative to the working directory (default is the working directory itself)",
                },
                "content": {
                    "type": "string",
                    "description": "Content, i. e. text or code etc. to write into the file specified in the previous parameter.",
                },
            },
        },
    },
}

def write_file(working_directory: str, file_path: str, content: str) -> str:
    try:
        working_dir_abs = os.path.abspath(working_directory)
        target = os.path.normpath(os.path.join(working_dir_abs, file_path))
        valid_target_dir = os.path.commonpath([working_dir_abs, target]) == working_dir_abs
        if not valid_target_dir:
            raise Exception(f'Cannot write to "{file_path}" as it is outside the permitted working directory')
        if os.path.isdir(target):
            raise Exception(f'Cannot write to "{file_path}" as it is a directory')
        os.makedirs(os.path.dirname(target), exist_ok=True)
        with open(target, "w") as f:
            f.write(content)
        return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
    except Exception as e:
            return f"\n    Error: {e}"
