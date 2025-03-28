# PyTemplateCode

This is a simple Python template project for beginners. It includes some useful functions, including a timer, current time fetcher, input validation, and simple decorative print functions.

## Functions

### `timer(seconds)`
This function counts down from a specified number of seconds and prints the remaining time every second.
- `seconds` (int): The number of seconds to count down.
- Raises a `ValueError` if the input is not an integer.

### `current_time(format="%Y-%m-%d %H:%M:%S")`
This function returns the current time formatted according to the specified format.
- `format` (str): The format in which to return the current time. Default is "%Y-%m-%d %H:%M:%S".

### `inputint(prompt="Введите число: ")`
This function prompts the user to enter a valid integer and returns it. If the user enters a non-integer value, an error message is displayed.
- `prompt` (str): The prompt message displayed to the user.

### `start(name="Your project name", delay=0.25)`
This function displays a decorated banner at the beginning of the program with customizable text and delay time.
- `name` (str): The name of your project that will be displayed in the banner.
- `delay` (float): The delay in seconds between each character printed.

### `end(end_text="End of code!", delay=0.25)`
This function prints an end message with a decorated banner.
- `end_text` (str): The message to display at the end.
- `delay` (float): The delay in seconds between each character printed.

## Installation

You can install this package via `pip`:

```
pip install pytemplatecode
```

## Usage

Here is a quick example of how you can use the functions in this package:

```python
from pytemplatecode import timer, current_time, inputint, start, end

# Start the project with a banner
start(name="My Awesome Project")

# Display current time
print(f"Current time: {current_time()}")

# Prompt user for an integer
number = inputint("Enter a number: ")
print(f"You entered: {number}")

# Countdown timer
timer(5)

# End the project with a banner
end(end_text="Project Completed!")
```
