import os

# The TODO mentioned a config file, but for simplicity, we'll define the constant here.
MAX_FILE_READ_SIZE = 10000


def get_file_content(working_directory, file_path):
    try:
        # 1. Security: Ensure the path is within the working directory
        real_working_dir = os.path.realpath(working_directory)
        full_path = os.path.join(real_working_dir, file_path)
        real_full_path = os.path.realpath(full_path)

        if not real_full_path.startswith(real_working_dir):
            return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'

        # 2. Check if it's a file
        if not os.path.isfile(real_full_path):
            return f'Error: File not found or is not a regular file: "{file_path}"'

        # 3. Read the file content
        with open(real_full_path, "r", encoding="utf-8", errors="ignore") as f:
            content = f.read(MAX_FILE_READ_SIZE)

        return content

    # 4. Catch any other errors
    except Exception as e:
        return f"Error: {e}"
