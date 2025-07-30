import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types

from functions.call_function import call_function

schema_get_files_info = types.FunctionDeclaration(
    name="get_files_info",
    description="Lists files in the specified directory along with their sizes, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="The directory to list files from, relative to the working directory. If not provided, lists files in the working directory itself.",
            ),
        },
    ),
)
schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description="Reads and returns the content of a specified file.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The path to the file to read, relative to the working directory.",
            ),
        },
        required=["file_path"],
    ),
)
schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Executes a Python file with optional arguments and returns its output, including stdout, stderr, and exit code.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The path to the Python file to execute, relative to the working directory.",
            ),
            "args": types.Schema(
                type=types.Type.ARRAY,
                items=types.Schema(type=types.Type.STRING),
                description="A list of arguments to pass to the Python script.",
            ),
        },
        required=["file_path"],
    ),
)
schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Writes or overwrites content to a specified file within the working directory. Creates the file if it does not exist.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The path to the file to write to, relative to the working directory.",
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="The content to write to the file.",
            ),
        },
        required=["file_path", "content"],
    ),
)
available_functions = types.Tool(
    function_declarations=[
        schema_get_files_info,
        schema_get_file_content,
        schema_run_python_file,
        schema_write_file,
    ]
)
SYSTEM_PROMPT = '''You are a helpful AI coding agent.

When a user asks a question or makes a request, make a function call plan. You can perform the following operations:

- List files and directories
- Read file contents
- Execute Python files with optional arguments
- Write or overwrite files

All paths you provide should be relative to the working directory. You do not need to specify the working directory in your function calls as it is automatically injected for security reasons.'''

load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")
client = genai.Client(api_key=api_key)
PROMPT = "Why is Boot.dev such a great place to learn backend development? Use one paragraph maximum."
VERBOSE = False
if len(sys.argv) == 1:
    print("Error")
    exit(1)
if sys.argv[-1] == "--verbose":
    VERBOSE = True


def main():
    user_prompt = " ".join(sys.argv[1:])
    messages = [
        types.Content(role="user", parts=[types.Part(text=user_prompt)]),
    ]
    i = 0
    while i < 20:
        i += 1
        res = client.models.generate_content(
            model="gemini-2.0-flash-001", contents=messages, config=types.GenerateContentConfig(tools=[available_functions], system_instruction=SYSTEM_PROMPT))
        for candidate in res.candidates:
            messages.append(candidate.content)
        function_call_part = res.function_calls
        if res.text and not function_call_part:
            print(res.text)
            break
        fr = call_function(function_call_part[0])
        fr.parts[0].function_response.response
        messages.append(types.Content(parts=fr.parts, role="tool"))
        if VERBOSE:
            print(f"-> {fr.parts[0].function_response.response}")
    # print(res.text)
        if VERBOSE:
            print(f"User prompt: {user_prompt}")
            print(f"Prompt tokens: {res.usage_metadata.prompt_token_count}")
            print(
                f"Response tokens: {res.usage_metadata.candidates_token_count}")


if __name__ == "__main__":
    main()
