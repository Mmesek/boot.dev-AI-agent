"""
TODO
function_call_part is a types.FunctionCall that most importantly has:

    A .name property (the name of the function, a string)
    A .args property (a dictionary of named arguments to the function)

If verbose is specified, print the function name and args:

print(f"Calling function: {function_call_part.name}({function_call_part.args})")

Otherwise, just print the name:

print(f" - Calling function: {function_call_part.name}")

    Based on the name, actually call the function and capture the result.
        Be sure to manually add the "working_directory" argument to the dictionary of keyword arguments, because the LLM doesn't control that one. The working directory should be ./calculator.
        The syntax to pass a dictionary into a function using keyword arguments is some_function(**some_args)

I used a dictionary of function name (string) -> function to accomplish this.

    If the function name is invalid, return a types.Content that explains the error:

return types.Content(
    role="tool",
    parts=[
        types.Part.from_function_response(
            name=function_name,
            response={"error": f"Unknown function: {function_name}"},
        )
    ],
)

    Return types.Content with a from_function_response describing the result of the function call:

return types.Content(
    role="tool",
    parts=[
        types.Part.from_function_response(
            name=function_name,
            response={"result": function_result},
        )
    ],
)

Note that from_function_response requires the response to be a dictionary, so we just shove the string result into a "result" field.

    Back where you handle the response from the model generate_content, instead of simply printing the name of the function the LLM decides to call, use call_function.
        The types.Content that we return from call_function should have a .parts[0].function_response.response within.
        If it doesn't, raise a fatal exception of some sort.
        If it does, and verbose was set, print the result of the function call like this:
"""
from google.genai import types

from functions.get_file_content import get_file_content
from functions.get_files_info import get_files_info
from functions.run_python import run_python_file
from functions.write_file import write_file

available_functions = {
    "get_files_info": get_files_info,
    "get_file_content": get_file_content,
    "run_python_file": run_python_file,
    "write_file": write_file,
}


def call_function(function_call_part, verbose=False):
    ...
    function_name = function_call_part.name
    function_args = function_call_part.args

    if verbose:
        print(f"Calling function: {function_name}({dict(function_args)})")
    else:
        print(f" - Calling function: {function_name}")

    if function_name not in available_functions:
        return types.Content(
            role="tool",
            parts=[
                types.Part.from_function_response(
                    name=function_name,
                    response={"error": f"Unknown function: {function_name}"},
                )
            ],
        )

    function_to_call = available_functions[function_name]
    all_args = dict(function_args)
    all_args["working_directory"] = "./calculator"

    function_result = function_to_call(**all_args)

    return types.Content(
        role="tool",
        parts=[
            types.Part.from_function_response(
                name=function_name,
                response={"result": function_result},
            )
        ],
    )
