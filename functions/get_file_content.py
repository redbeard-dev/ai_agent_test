import os

schema_get_file_content = {
    "type": "function",
    "function": {
        "name": "get_file_content",
        "description": "Returns the content of a specified file, i. e. reading the first 10000 characters from that file and returning it as text.",
        "parameters": {
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": "File path of file to read including the file itself, relative to the working directory (default is the working directory itself)",
                },
            },
        },
    },
}

def get_file_content(working_directory: str, file_path: str) -> str:
    try:
        MAX_CHARS = 10000
        working_dir_abs = os.path.abspath(working_directory)
        target = os.path.normpath(os.path.join(working_dir_abs, file_path))
        valid_target_dir = os.path.commonpath([working_dir_abs, target]) == working_dir_abs
        if not valid_target_dir:
            raise Exception(f'Cannot read "{file_path}" as it is outside the permitted working directory')
        if not os.path.isfile(target):
            raise Exception(f'File not found or is not a regular file: "{file_path}"')
        with open(target, "r") as f:
            content = f.read(MAX_CHARS)
            # After reading the first MAX_CHARS...
            if f.read(1):
                content += f'[...File "{file_path}" truncated at {MAX_CHARS} characters]'
        return content
    except Exception as e:
        return f"\n    Error: {e}"
