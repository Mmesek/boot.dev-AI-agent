"""
TODO
1. `get_files_info("calculator", "."):`
```
Result for current directory:
 - main.py: file_size=576 bytes, is_dir=False
 - tests.py: file_size=1343 bytes, is_dir=False
 - pkg: file_size=92 bytes, is_dir=True
```

2. `get_files_info("calculator", "pkg"):`
```
Result for 'pkg' directory:
 - calculator.py: file_size=1739 bytes, is_dir=False
 - render.py: file_size=768 bytes, is_dir=False
```

3. `get_files_info("calculator", "/bin"):`
```
Result for '/bin' directory:
    Error: Cannot list "/bin" as it is outside the permitted working directory
```

4. `get_files_info("calculator", "../"):`
```
Result for '../' directory:
    Error: Cannot list "../" as it is outside the permitted working directory
```
"""

from functions.run_python import run_python_file


def test_calculator():
    expected_output = (
        "Result for current directory:"
        " - main.py: file_size=576 bytes, is_dir=False",
        " - tests.py: file_size=1343 bytes, is_dir=False",
        " - pkg: file_size=92 bytes, is_dir=True"
    )
    result = run_python_file("calculator", "main.py")
    print(" " + result)
    # self.assertEqual(result, expected_output)


def test_calculator_pkg():
    expected_output = (
        "Result for 'pkg' directory:"
        " - calculator.py: file_size=1739 bytes, is_dir=False",
        " - render.py: file_size=768 bytes, is_dir=False",
    )
    result = run_python_file("calculator", "main.py", ["3 + 5"])
    print(" " + result)
    # self.assertEqual(result, expected_output)


def test_list_outside_working_directory_absolute():
    directory_to_list = "/bin"
    expected_error = f'Error: Cannot list "{directory_to_list}" as it is outside the permitted working directory'
    result = run_python_file("calculator", "tests.py")
    print("    ", result)

    # self.assertEqual(result, expected_error)


def test_list_outside_working_directory_relative():
    directory_to_list = "../"
    expected_error = f'Error: Cannot list "{directory_to_list}" as it is outside the permitted working directory'
    result = run_python_file("calculator", "../main.py")
    print("    ", result)

    # self.assertEqual(result, expected_error)


test_calculator()
test_calculator_pkg()
test_list_outside_working_directory_absolute()
test_list_outside_working_directory_relative()
print(run_python_file("calculator", "nonexistent.py"))
