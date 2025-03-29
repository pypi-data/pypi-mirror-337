import lib


def test_better_print_str():
    test_str = """
 Hello, world!
 aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa
 """
    lib.printer.better_print_str(test_str)


def test_print_table():
    data = [
        ["姓名", "年龄", "城市"],
        ["Alice", 24, "New York"],
        ["Bob", 30, "San Francisco"],
        ["Charlie", 22, "北京"],
    ]
    lib.printer.print_table(data)


if __name__ == "__main__":
    test_print_table()
