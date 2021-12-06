from os.path import dirname, basename, splitext
from typing import Generator


def get_input_data_filepath(script_path: str) -> str:
    data_dir = dirname(script_path) + '/input_data'
    data_file = splitext(basename(script_path))[0] + '.txt'
    return f"{data_dir}/{data_file}"


def read_integer_file(file_path: str) -> Generator[int, None, None]:
    with open(file_path) as fp:
        for line in fp:
            if not line.strip().isnumeric():
                print(f"Line {line} is not numeric")
                continue

            yield int(line.strip())
