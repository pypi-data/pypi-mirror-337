import time
import sys
from random import randint

# ANSI colors
COLORS = {
    "red": "\033[91m",
    "green": "\033[92m",
    "yellow": "\033[93m",
    "blue": "\033[94m",
    "magenta": "\033[95m",
    "cyan": "\033[96m",
    "white": "\033[97m",
    "reset": "\033[0m"
}


def timer(seconds):
    """
    Counts down the specified number of seconds and prints the remaining time every second.

    Args:
        seconds (int): The number of seconds to count down.

    Raises:
        ValueError: If seconds is not an integer.
    """
    if not isinstance(seconds, int):
        raise ValueError(
            "Error: Please enter an integer number of seconds. If you need fractional time, use the time library.")

    for i in range(seconds, 0, -1):
        print(f"{i} seconds remaining...")
        time.sleep(1)

    print("Time's up!")


def current_time(format="%Y-%m-%d %H:%M:%S"):
    """
    Returns the current local time formatted as specified.

    Args:
        format (str): The format in which to return the current time. Default is "%Y-%m-%d %H:%M:%S".

    Returns:
        str: The formatted current time.
    """
    return time.strftime(format, time.localtime())


def inputint(prompt="Enter a number: "):
    """
    Prompts the user to enter a valid integer and returns it.

    Args:
        prompt (str): The prompt message displayed to the user.

    Returns:
        int: The valid integer entered by the user.

    If the input is not an integer, the user is prompted again.
    """
    while True:
        user_input = input(prompt)
        if user_input.isdigit():
            return int(user_input)
        else:
            print("Error: Please enter an integer.")


def start(name="Your project name", delay=0.25):
    """
    Prints a decorative banner at the beginning of the program with customizable text and delay.

    Args:
        name (str): The name of your project displayed in the banner.
        delay (float): The delay in seconds between each character printed.
    """
    frame = "-" * len(name) + "--"

    lines = [
        f"[{frame}]\n"
        f"[ {name} ]\n"
        f"[{frame}]\n"
    ]

    for line in lines:
        for char in line:
            if char == " ":
                sys.stdout.write(char)
                sys.stdout.flush()
                continue
            elif char == "-":
                sys.stdout.write(char)
                sys.stdout.flush()
                time.sleep(delay / 3)
            else:
                sys.stdout.write(char)
                sys.stdout.flush()
                time.sleep(delay)
        print()


def end(end_text="End of code!", delay=0.25):
    """
    Prints a decorative end message with a banner.

    Args:
        end_text (str): The message to display at the end.
        delay (float): The delay in seconds between each character printed.
    """
    end_frame = "-" * len(end_text) + "--"

    sys.stdout.write("\n")
    lines = [
        f"[{end_frame}]\n"
        f"[ {end_text} ]\n"
        f"[{end_frame}]\n"
    ]
    for line in lines:
        for char in line:
            if char == " ":
                sys.stdout.write(char)
                sys.stdout.flush()
                continue
            elif char == "-":
                sys.stdout.write(char)
                sys.stdout.flush()
                time.sleep(delay / 5)
            else:
                sys.stdout.write(char)
                sys.stdout.flush()
                time.sleep(delay)
        print()


def crash(seconds=0):
    """
    Simulates a crash after a specified number of seconds with a countdown and "CRASHED" message.

    Args:
        seconds (int or float): The number of seconds until the crash.

    Raises:
        ValueError: If seconds is negative or not a valid number.
    """
    if not isinstance(seconds, (int, float)) or seconds < 0:
        raise ValueError("Seconds must be a non-negative number.")

    dot_pattern = [3, 2, 1]

    if seconds > 0:
        for i in range(seconds):
            remaining = seconds - i
            dots = "." * dot_pattern[i % 3]
            sys.stderr.write(f"\rCrashing in {remaining} seconds{dots}  ")
            sys.stderr.flush()
            time.sleep(1)

    sys.stderr.write("\r---------------------\n CRASHED BY COMMAND!\n---------------------\n")
    sys.stderr.flush()
    sys.exit(1)


def printedit(*args):
    """
    Dynamically updates the printed text in the same line, displaying elements sequentially.

    Args:
        First argument (optional) - text color (str).
        Remaining arguments - alternating list of text (str) and delay (float).

    If any error occurs, prints corresponding error message and continues.
    """
    try:
        color = ""
        start_index = 0

        if args[0] in COLORS:
            color = COLORS[args[0]]
            start_index = 1
        elif isinstance(args[0], str):
            print("Check your color")
            start_index = 1

        if (len(args) - start_index) % 2 != 0:
            print("Check your printedit")
            return

        for i in range(start_index, len(args), 2):
            text = args[i]
            delay = args[i + 1]

            if not isinstance(text, str) or not isinstance(delay, (int, float)):
                print("Check your printedit")
                return

            sys.stdout.write(f"\r{color}{text}{COLORS['reset']} ")
            sys.stdout.flush()
            time.sleep(delay)

        sys.stdout.write("\n")

    except Exception:
        print("Check your printedit")