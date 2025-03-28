import time
import sys

def timer(seconds):
    if not isinstance(seconds, int):
        raise ValueError("Error: Please enter an integer number of seconds. If you need fractional time, use the time library.")

    for i in range(seconds, 0, -1):
        print(f"{i} seconds remaining...")
        time.sleep(1)

    print("Time's up!")

def current_time(format="%Y-%m-%d %H:%M:%S"):
    return time.strftime(format, time.localtime())

def inputint(prompt="Enter a number: "):
    while True:
        user_input = input(prompt)
        if user_input.isdigit():  # Check if the input is an integer
            return int(user_input)
        else:
            print("Error: Please enter an integer.")

def start(name="Your project name", delay=0.25):
    frame = "-" * len(name) + "--"

    lines = [
        f"[{frame}]\n"
        f"[ {name} ]\n"
        f"[{frame}]\n"
    ]

    # Print the initial banner character by character
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

