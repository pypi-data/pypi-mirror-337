
# Bandit

A lightweight Python library for debugging and logging, providing tools to retrieve script and function names dynamically. Ideal for quick insights into code execution without heavy dependencies.

## Installation

Install `bandit-log` from PyPI:

```bash
pip install bandit-log
```

## Features

- Retrieve the current script name and function name with simple static methods.
- Use a decorator to log execution details automatically.
- No external dependencies, pure Python.

## Usage

Here’s a quick example to get you started:

```python
from bandit_log.bandit import Bandit

# Decorate a function to log its name
@Bandit.universal_print(show_script=False)
def power_of_five(n):
    return 5 ** n

# Call the function
print(power_of_five(3))  # Outputs: "Func: power_of_five" followed by 125

# Get script and function names manually
script, func = Bandit.names()
print(f"Running in {script}, called from {func}")
```

### API Reference

#### `Bandit.universal_print(show_script=True, show_func=True)`
A decorator that prints the script name and/or function name before executing the function.

- **Arguments:**
  - `show_script` (bool): If `True`, prints the script name. Default: `True`.
  - `show_func` (bool): If `True`, prints the function name. Default: `True`.
- **Example:**
  ```python
  @Bandit.universal_print(show_script=False)
  def my_func():
      print("Hello!")
  my_func()  # Outputs: "Func: my_func" then "Hello!"
  ```

#### `Bandit.names()`
Returns a tuple of the current script name and the calling function name.

- **Returns:** `(script_name, function_name)`
- **Example:**
  ```python
  script, func = Bandit.names()
  print(script, func)  # e.g., "example.py some_function"
  ```

#### `Bandit.func_name()`
Returns the name of the calling function.

- **Returns:** `str`
- **Example:**
  ```python
  def test():
      print(Bandit.func_name())  # Outputs: "test"
  test()
  ```

#### `Bandit.script_name()`
Returns the name of the current script.

- **Returns:** `str`
- **Example:**
  ```python
  print(Bandit.script_name())  # e.g., "example.py"
  ```

## Requirements

- Python 3.7 or higher

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Contributing

Feel free to open issues or submit pull requests on [GitHub](https://github.com/somke/bandit-log).

---
Made with ❤️ by somke
```