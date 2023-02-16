"""Defines some utilities for pretty printing stuff.

This file defines functions that use rich library to pretty print inputs to the terminal.
"""

from typing import Dict

import rich
from rich.pretty import pprint


def style(text: str, style: str) -> str:
    """Create styled string acceptable by rich.

    Applies the style to text. The styling is only applied to this text and is stopped at the last character of txt.

    Args:
        text (str): The text to print.
        style (str): The style to apply to text.

    Returns:
        str: Returns the stylized string.
    """
    return f"[{style}]{text}[/{style}]"


def pretty_key_value(mapping: Dict) -> None:
    """Print colored key value mappings.

    Pretty print key value mappings. It follows rich colors for json printing but without the brackets.

    Args:
        mapping (Dict): A json like mapping.
    """
    rich_json_styles = {
        "bool_true": "italic bright_green",
        "bool_false": "italic bright_red",
        "null": "italic magenta",
        "number": "bold italic cyan",
        "str": "bold italic green",
        "key": "bold blue",
    }
    lines = list()
    for key, value in mapping.items():
        if isinstance(value, bool):
            if value:
                value_style = rich_json_styles["bool_true"]
            else:
                value_style = rich_json_styles["bool_false"]
        elif value is None:
            value_style = rich_json_styles["null"]
        elif isinstance(value, int) or isinstance(value, float):
            value_style = rich_json_styles["number"]
        elif isinstance(value, str):
            value_style = rich_json_styles["str"]
        else:
            value_style = rich_json_styles["str"]
            value = str(value)
        lines.append(
            style(key, rich_json_styles["key"]) + ": " + style(value, value_style)
        )
    msg = "\n".join(lines)
    rich.print(msg)


def pretty_json(json_object: Dict) -> None:
    """Pretty prints json objects using rich library.

    Args:
        json_object (Dict): A json object.
    """
    pprint(json_object, expand_all=True, indent_guides=False)
