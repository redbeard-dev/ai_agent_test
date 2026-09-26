import subprocess, os

schema_run_python_file = {
    "type": "function",
    "function": {
        "name": "run_python_file",
        "description": "Runs a specified python file (.py).",
        "parameters": {
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": "File path of python file to execute to including the file name itself, relative to the working directory (default is the working directory itself)",
                },
                "args": {
                    "type": "string",
                    "description": "Arguments that are supposed to be used when running the previously specified python file as a list of strings.",
                },
            },
        },
    },
}

def run_python_file(working_directory: str, file_path: str, args: list[str] | None = None) -> str:
    try:
        working_dir_abs = os.path.abspath(working_directory)
        target = os.path.normpath(os.path.join(working_dir_abs, file_path))
        valid_target_dir = os.path.commonpath([working_dir_abs, target]) == working_dir_abs
        if not valid_target_dir:
            raise Exception(f'Cannot execute "{file_path}" as it is outside the permitted working directory')
        if not os.path.isfile(target):
            raise Exception(f'"{file_path}" does not exist or is not a regular file')
        if not file_path.endswith(".py"):
              raise Exception(f'Error: "{file_path}" is not a Python file')
        command = ["python", target]
        if args:
            command.extend(args)
        result = subprocess.run(command, capture_output=True, timeout=30, text=True)
        result_text = f"Process exited with code {result.returncode}" if result.returncode != 0 else ""
        result_text += f"No output produced" if not result.stderr and not result.stdout else f"STDOUT: {result.stdout}\nSTDERR: {result.stderr}"
        return result_text
    except Exception as e:
                return f"Error: executing Python file: {e}"
