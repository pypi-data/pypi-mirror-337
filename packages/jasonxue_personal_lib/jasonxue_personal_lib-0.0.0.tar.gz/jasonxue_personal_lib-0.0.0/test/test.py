from jason_lib.printer import better_print_str


def test_better_print_str():
    test_str = """
 Hello, world!
 aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa
 """
    better_print_str(test_str)


if __name__ == "__main__":
    test_better_print_str()
