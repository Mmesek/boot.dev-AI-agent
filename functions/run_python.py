import os
import subprocess
import sys


def run_python_file(working_directory, file_path, args=[]):
    try:
        # 1. Security: Ensure the path is within the working directory
        abs_working_dir = os.path.abspath(working_directory)
        abs_file_path = os.path.abspath(
            os.path.join(abs_working_dir, file_path))

        if not abs_file_path.startswith(abs_working_dir):
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'

        # 2. Check if the file exists
        if not os.path.isfile(abs_file_path):
            return f'Error: File "{file_path}" not found.'

        # 3. Check if it's a Python file
        if not file_path.endswith(".py"):
            return f'Error: "{file_path}" is not a Python file.'

        # 4. Execute the Python file using subprocess
        command = [sys.executable, abs_file_path] + args
        completed_process = subprocess.run(
            command,
            cwd=abs_working_dir,
            capture_output=True,
            text=True,
            timeout=30,
        )

        # 5. Format the output
        output_parts = []
        stdout = completed_process.stdout.strip()
        stderr = completed_process.stderr.strip()

        if stdout:
            output_parts.append(f"STDOUT:\n{stdout}")

        if stderr:
            output_parts.append(f"STDERR:\n{stderr}")

        if not output_parts and completed_process.returncode == 0:
            return "No output produced."

        if completed_process.returncode != 0:
            output_parts.append(
                f"Process exited with code {completed_process.returncode}"
            )

        return "\n".join(output_parts)

    # 6. Handle exceptions
    except subprocess.TimeoutExpired:
        return f"Error: execution of '{file_path}' timed out after 30 seconds."
    except Exception as e:
        return f"Error: executing Python file: {e}"
