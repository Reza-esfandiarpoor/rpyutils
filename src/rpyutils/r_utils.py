"""Simple python utilities that are used often

Generic utility functions
"""

import inspect
import json
import os
import pickle as pkl
import time
from contextlib import contextmanager
from pathlib import Path
from typing import Any, Iterable, List, Optional, Union

import psutil
import pyrootutils
from tqdm import tqdm


class JSONLinesWriter:
    def __init__(
        self, path: os.PathLike, chunk_size: Optional[int] = None, **kwargs
    ) -> None:
        """Open a json lines file for writing.

        Example:
            >>> with JSONLinesWriter('/path/to/file.jsonl') as writer:
            ...     writer.add([{'a': 1}, {'b': 2}])
            ...     writer.add_one({'c': 3})

        Args:
            path: file to open.
            chunk_size: flush the buffer every 'chunk_size' records.
            **kwargs: keyword arguments passed to 'json.dumps()'
        """
        Path(path).parent.mkdir(exist_ok=True, parents=True)
        self.fp = open(path, "w")
        self.json_kw = kwargs
        if chunk_size is None:
            self.chunk_size = 1_000
        else:
            self.chunk_size = chunk_size
        self.line_buffer = list()

    def __enter__(self):
        """Act as a context manager."""
        return self

    def __exit__(self, *args, **kwargs):
        """Cleanups before exiting the context."""
        self.close()

    def add(self, items: Iterable[Any]) -> None:
        """Write a list () of objects to file."""
        for item in items:
            self.line_buffer.append(json.dumps(item, **self.json_kw))
            if len(self.line_buffer) >= self.chunk_size:
                self.flush()

    def add_one(self, item: Any) -> None:
        """Write one object to file."""
        self.add([item])

    def flush(self) -> None:
        """Flush the content of the buffer to file."""
        if len(self.line_buffer) != 0:
            self.fp.write("\n".join(self.line_buffer) + "\n")
            self.line_buffer = list()

    def close(self) -> None:
        """Flush the buffer and close the file."""
        self.flush()
        self.fp.close()


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
    obj_list = list()
    with open(path, "r") as f:
        for line in tqdm(f, desc="read json lines from disk."):
            if line.strip() == "":
                continue
            obj_list.append(json.loads(line.strip(), **kwargs))
    return obj_list


def write_json_lines(obj_list, path, **kwargs):
    path = Path(path)
    path.parent.mkdir(exist_ok=True, parents=True)
    line_buffer = list()
    chunk_size = 1_000
    with open(path, "w") as f:
        for obj in tqdm(obj_list, desc="Writer Json Lines Records"):
            line_buffer.append(json.dumps(obj, **kwargs))
            if len(line_buffer) >= chunk_size:
                f.write("\n".join(line_buffer) + "\n")
                line_buffer = []
        if len(line_buffer):
            f.write("\n".join(line_buffer) + "\n")
            line_buffer = []


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
        str_size = tqdm.format_sizeof(mem_bytes, suffix="B", divisor=1024)

    if msg is not None:
        str_size = msg + ": " + str_size
    print(str_size)


@contextmanager
def timer(msg: Optional[str] = "Elapsed Time"):
    start = time.perf_counter()
    yield
    end = time.perf_counter()
    elapsed = end - start
    if elapsed < 1:
        t_fmt = f"{elapsed:.4f}"
    else:
        t_fmt = tqdm.format_interval(elapsed)
    if msg is not None:
        t_fmt = f"{msg}: {t_fmt}"
    print(t_fmt)


def format_bytes(
    num_bytes: int, msg: Optional[str] = None, echo: bool = True
) -> Optional[str]:
    """Format bytes into human readable units.

    Args:
        num_bytes: number of bytes to format with proper unit.
        msg: preffix result with this message.
        echo: if True, print the result. If False, return the result.

    Returns: number of bytes in human readable format.
    """
    s_fmt = tqdm.format_sizeof(num_bytes, suffix="B", divisor=1024)
    if msg is not None:
        s_fmt = f"{msg}: {s_fmt}"
    if echo:
        print(s_fmt)
    else:
        return s_fmt


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


def make_script_section_title(
    title: str, width: int = 100, fill_char: str = "#", output: str = "echo"
) -> Optional[Union[List[str], str]]:
    """Make a section title for simple scripts.

    Args:
        title: The text content of the title
        width: the width of title string
        fill_char: character to fill the width of the title and also draw two lines before and after the title.
        output: what to do with the output:
            - 'echo': print the title
            - 'return': return the title as a string
            - 'return_line': return a list of lines that make up the title

    Returns: None or the created title depending on the value of `output` argument.
    """
    assert output in ["return", "return_lines", "echo"]
    lines = list()
    lines.append("#" * width)
    lines.append("#" * width)
    lines.append("{:{}^{}s}".format(f" {title} ", fill_char, width))
    lines.append("#" * width)
    lines.append("#" * width)
    if output == "echo":
        title_fmt = "\n".join(lines)
        print(title_fmt)
    elif output == "return":
        title_fmt = "\n".join(lines)
        return title_fmt
    elif output == "return_lines":
        return lines
    else:
        raise ValueError
