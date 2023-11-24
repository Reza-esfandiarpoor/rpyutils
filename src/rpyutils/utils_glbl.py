"""Utils to be imported globally with star

Generic utility functions
"""

import json
import pickle as pkl
from pathlib import Path


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
