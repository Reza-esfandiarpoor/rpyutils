"""This file defines the entry point of the commandline app.

This file provides the app function which shows a sample output of the program at its current state.
"""

from typing import List, Union

from .utils import prettifier


def run(argv: Union[List, None] = None) -> None:
    """The entry point for the commandline use.

    You can see :py:func:`fcpp.utils.calculator.add_two` in the link.

    Args:
        argv (Union[List, None]): List of commandline arguments.
    """
    if argv is None or len(argv) <= 1:
        print("An example of key value pretty printing is shown below.")
        sample_mapping = {
            "string": "This is a sample string",
            "false boolean": False,
            "true boolean": True,
            "integer": 12345,
            "float": 12.34,
        }
        prettifier.pretty_key_value(sample_mapping)
        print("\nAn example of json pretty printing by rich library.")
        prettifier.pretty_json(sample_mapping)
    else:
        print("I am not ready for custom input now. The input is shown below.")
        for a in argv[1:]:
            print(a)
