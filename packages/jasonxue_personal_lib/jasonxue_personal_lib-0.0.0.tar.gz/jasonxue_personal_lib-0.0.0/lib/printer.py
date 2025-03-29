import time


def better_print_str(s: str, delay: float = 0.1) -> None:
    """
    Prints the string character by character with a specified delay between each character.

    :param s: The string to print.
    :param delay: The delay in seconds between each character (default is 0.1 seconds).
    """
    for ch in s:
        print(ch, end="", flush=True)
        time.sleep(delay)
    print()  # Print a newline after printing the string
