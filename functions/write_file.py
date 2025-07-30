import os


def write_file(working_directory, file_path, content):
    try:
        # 1. Security: Ensure the path is within the working directory
        abs_working_dir = os.path.abspath(working_directory)
        abs_file_path = os.path.abspath(
            os.path.join(abs_working_dir, file_path))

        if not abs_file_path.startswith(abs_working_dir):
            return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'

        # 2. Ensure parent directory exists, then create/overwrite the file
        parent_dir = os.path.dirname(abs_file_path)
        os.makedirs(parent_dir, exist_ok=True)

        # 3. Overwrite the contents of the file
        with open(abs_file_path, "w", encoding="utf-8") as f:
            f.write(content)

        # 4. Return success message
        return (
            f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
        )

    except Exception as e:
        return f"Error: {e}"
