"""Simple python utilities that are used often

Generic utility functions
"""

import inspect
import json
import pickle as pkl
from pathlib import Path

import psutil
import pyrootutils


def read_json(path, **kwargs):
    with open(path, "r") as f:
        obj = json.load(f, **kwargs)
    return obj


def write_json(obj, path, **kwargs):
    path = Path(path)
    path.parent.mkdir(exist_ok=True, parents=True)
    with path.open("w") as f:
        json.dump(obj, f, **kwargs)


def read_json_lines(path, **kwargs):
    with open(path, "r") as f:
        lines = f.readlines()
    obj_list = [
        json.loads(line.strip(), **kwargs) for line in lines if line.strip() != ""
    ]
    return obj_list


def write_json_lines(obj_list, path, **kwargs):
    path = Path(path)
    path.parent.mkdir(exist_ok=True, parents=True)
    line_list = [json.dumps(item, **kwargs) for item in obj_list]
    file_content = "\n".join(line_list)
    with open(path, "w") as f:
        f.write(file_content)


def read_pickle(path, **kwargs):
    with open(path, "rb") as f:
        obj = pkl.load(f, **kwargs)
    return obj


def write_pickle(obj, path, **kwargs):
    path = Path(path)
    path.parent.mkdir(exist_ok=True, parents=True)
    with open(path, "wb") as f:
        pkl.dump(obj, f, **kwargs)


def sizeof_fmt(num, suffix="B"):
    for unit in ("", "Ki", "Mi", "Gi", "Ti", "Pi", "Ei", "Zi"):
        if abs(num) < 1024.0:
            return f"{num:3.1f} {unit}{suffix}"
        num /= 1024.0
    return f"{num:.1f} Yi{suffix}"


def used_mem(msg=None, echo=True, echo_bytes=False):
    process = psutil.Process()
    mem_bytes = process.memory_info().rss
    if not echo:
        return mem_bytes

    str_size = f"{mem_bytes}"
    if not echo_bytes:
        str_size = sizeof_fmt(mem_bytes)

    if msg is not None:
        str_size = msg + ": " + str_size
    print(str_size)


def get_relative_file_path(path):
    try:
        root = Path(pyrootutils.find_root())
    except FileNotFoundError:
        root = Path.cwd()

    path = Path(path)
    try:
        rel_path = path.relative_to(root)
    except ValueError:
        rel_path = path
    rel_path_str = rel_path.as_posix()
    return rel_path_str


def current_file_and_line():
    frame_info_list = inspect.getouterframes(inspect.currentframe())
    if len(frame_info_list) > 1:
        frame_info = frame_info_list[1]
    else:
        frame_info = frame_info_list[0]

    filename = frame_info.filename
    lineno = frame_info.lineno
    rel_filename = get_relative_file_path(filename)

    print(f"{rel_filename}: {lineno}")

    return (rel_filename, lineno)
