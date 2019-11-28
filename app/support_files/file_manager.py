"""
This module contains functions to work with files.
"""
from re import findall
from pathlib import Path

from app.support_files.exeptions import DirError, DirExistsError


def store_str_to_file(data: str, path: str, file_format: str, file_name: str = "feed") -> None:
    """
    Saves data to a folder at a given path to a file with a given name, to which the index is added, and the format.
    The file name is based on files with a specific file name format that are already in the folder.
    File indices go sequentially and a new file fills this sequence or is set to the end.
    """
    true_path = Path(path)
    if not true_path.exists():
        raise DirExistsError(f"This directory not exists: {true_path}")
    if not true_path.is_dir():
        raise DirError(f"Is not a directory: {true_path}")
    file_indexes = []
    for _dir in true_path.iterdir():
        if findall(fr"{file_name}\d+.{file_format}", _dir.name):
            file_indexes.append(int(findall(r"\d+", _dir.name)[0]))
    file_indexes = sorted(file_indexes)
    current_index = 1
    for index in file_indexes:
        if index - current_index > 1:
            break
        else:
            current_index += 1
    with open(true_path.joinpath("".join([file_name, str(current_index), ".", file_format])), "w") as file:
        file.write(data)


if __name__ == "__main__":
    print(Path(".").name)
