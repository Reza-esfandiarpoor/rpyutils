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
from subprocess import CalledProcessError, run
from typing import Any, Dict, Iterable, List, Optional, Union

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


def count_file_lines(path: os.PathLike) -> int:
    """Count number of lines in file using linux 'wc -l' command."""
    if not Path(path).exists():
        msg = f"Path does not exists: '{path}'"
        raise RuntimeError(msg)
    path = Path(path).absolute().resolve().as_posix()
    cmd_str = f"wc -l '{path}'"
    try:
        cmd_output = run(
            cmd_str, shell=True, capture_output=True, text=True, check=True
        )
    except CalledProcessError as e:
        print("---")
        print("Command stdout")
        print(e.stdout)
        print("Command stderr")
        print(e.stderr)
        print("---")
        raise e
    output = cmd_output.stdout
    # wc output is 'NUM_LINES FILENAME'. parse it to get num lines.
    num_lines = int(output.split(" ")[0])
    return num_lines


def _head_and_tail(
    cmd: str,
    path: os.PathLike,
    lines: Optional[int] = None,
    shell_opts: Optional[str] = None,
) -> List[str]:
    """Run head and tail commands on a file. See docstring for user facing commands for details on arguments."""
    if lines is None and shell_opts is None:
        msg = (
            "If you do not specify lines, you must specify the equivalent through 'shell_opts' argument."
            " Both are passed a value of 'None'."
        )
        raise ValueError(msg)
    if not Path(path).exists():
        msg = f"Path does not exists: '{path}'"
        raise RuntimeError(msg)

    path = Path(path).absolute().resolve().as_posix()
    cmd_str = cmd.strip()
    if lines is not None:
        cmd_str += f" -n {lines}"
    if shell_opts is not None:
        cmd_str += f" {shell_opts}"
    cmd_str += f" '{path}'"
    try:
        cmd_output = run(
            cmd_str, shell=True, capture_output=True, text=True, check=True
        )
    except CalledProcessError as e:
        print("---")
        print("Command stdout")
        print(e.stdout)
        print("Command stderr")
        print(e.stderr)
        print("---")
        raise e
    output = cmd_output.stdout
    if output.strip() == "":
        return []
    lines = output.strip().split("\n")
    return lines


def head(
    path: os.PathLike, lines: Optional[int] = 1, shell_opts: Optional[str] = None
) -> List[str]:
    """Run linux 'head' command on file.

    the command that will be run is like this: `head -n $LINES $SHELL_OPTS $path`
    arguments that are `None` are not added to the final command.


    Args:
        path: to to to pass to 'head' as an argument.
        lines: number of lines to show.
        shell_opts: string to concat to the shell command being executed.

    Returns: list of lines.
    """
    return _head_and_tail(cmd="head", path=path, lines=lines, shell_opts=shell_opts)


def tail(
    path: os.PathLike, lines: Optional[int] = 1, shell_opts: Optional[str] = None
) -> List[str]:
    """Run linux 'tail' command on file.

    the command that will be run is like this: `tail -n $LINES $SHELL_OPTS $path`
    arguments that are `None` are not added to the final command.


    Args:
        path: to to to pass to 'tail' as an argument.
        lines: number of lines to show.
        shell_opts: string to concat to the shell command being executed.

    Returns: list of lines.
    """
    return _head_and_tail(cmd="tail", path=path, lines=lines, shell_opts=shell_opts)


def head_json_lines(
    path: os.PathLike, lines: Optional[int] = 1, shell_opts: Optional[str] = None
) -> List[Dict]:
    """Run linux head command on file and parse the output lines as json objects.

    see docs for `head()` function for details.
    """
    lines = head(path=path, lines=lines, shell_opts=shell_opts)
    objs = [json.loads(l) for l in lines]
    return objs


def tail_json_lines(
    path: os.PathLike, lines: Optional[int] = 1, shell_opts: Optional[str] = None
) -> List[Dict]:
    """Run linux tail command on file and parse the output lines as json objects.

    see docs for `tail()` function for details.
    """
    lines = tail(path=path, lines=lines, shell_opts=shell_opts)
    objs = [json.loads(l) for l in lines]
    return objs


def echo_rule(char="-") -> None:
    """Draw a line filling the width of the terminal using the given character."""
    rule = char * os.terminal_size().columns
    print(rule)
