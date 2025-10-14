from functions.get_files_info import get_files_info
from functions.run_python_file import run_python_file
from functions.write_file import write_file


def test():
    print(get_files_info("calculator", "."))
    print(get_files_info("calculator", "pkg"))
    print(get_files_info("calculator", "/bin"))
    print(get_files_info("calculator", "../"))

    # print(run_python_file("calculator", "tests.py"))
    # print(run_python_file("calculator", "../main.py"))
    # print(run_python_file("calculator", "nonexistent.py"))
    # print(run_python_file("calculator", "lorem.txt"))

if __name__ == "__main__":
    test()
