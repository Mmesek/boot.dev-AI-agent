import os


def get_files_info(working_directory, directory="."):
    try:
        # Use realpath to resolve symlinks and prevent path traversal.
        real_working_dir = os.path.realpath(working_directory)

        # Create the full path to the target directory.
        full_path = os.path.join(real_working_dir, directory)
        real_full_path = os.path.realpath(full_path)

        if not real_full_path.startswith(real_working_dir):
            return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'

        if not os.path.isdir(real_full_path):
            return f'Error: "{directory}" is not a directory'

        output_lines = []
        for item_name in sorted(os.listdir(real_full_path)):
            item_path = os.path.join(real_full_path, item_name)
            is_dir = os.path.isdir(item_path)
            file_size = os.path.getsize(item_path)
            output_lines.append(
                f"- {item_name}: file_size={file_size} bytes, is_dir={is_dir}"
            )

        return "\n".join(output_lines)
    except Exception as e:
        return f"Error: {e}"
