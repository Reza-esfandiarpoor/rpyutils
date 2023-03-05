# Adapted from https://github.com/nicolaskruchten/jupyter_pivottablejs
import json
from pathlib import Path
from typing import Union
from uuid import uuid4

import pandas as pd
from IPython.display import HTML

from . import iframe_html_utils, pivottablejs_template


def pivot_ui(
    df: pd.DataFrame,
    caption: Union[str, None] = None,
    height: str = "600px",
    width: str = "100%",
    show: bool = True,
    file: Union[str, None] = None,
    save: Union[bool, None] = None,
    close: bool = False,
    **kwargs,
) -> Union[HTML, None]:
    """Crates a pivot table from the pandas dataframe with [pivottablejs](https://github.com/nicolaskruchten/pivottable)

    The output is either saved to an html file or returned in a jupyter notebook HTML object.

    Args:
        df (pd.DataFrame): Input dataframe.
        caption (Union[str, None], optional): Caption of the table. Defaults to None.
        height (str, optional): Height of the output in css format. Defaults to "600px".
        width (str, optional): Width of the output in css format. Defaults to "100%".
        show (bool, optional): Show the table (i.e. return an HTML object). Defaults to True.
        file (Union[str, None], optional): Output html file. Defaults to None.
        save (Union[bool, None], optional): Save the table in an html file. Can be True/False/None. Defaults to None.
            The table is saved to file if `(save == None and file != None) or save == True`
        close (bool, optional): If the detail tag should be closed initially. Defaults to False.

    Returns:
        Union[HTML, None]: The table either in an HTML object if show is True.
    """

    csv = df.to_csv(encoding="utf8")
    if hasattr(csv, "decode"):
        csv = csv.decode("utf8")
    main_html_code = pivottablejs_template.pivottablejs_template % dict(
        csv=csv, kwargs=json.dumps(kwargs)
    )

    if (save == None and file != None) or save == True:
        path = Path(file or "fancy_table.html")
        path.parent.mkdir(exist_ok=True, parents=True)
        with path.open("wt", encoding="utf8") as f:
            f.write(main_html_code)
        print(f"Saved to {path}")

    detail_summary_val = (caption or "Pivottable JS").title()

    if show:
        return iframe_html_utils.show_html(
            main_html_code,
            html_iframe_tag=True,
            wrap_in_detail=True,
            detail_summary=detail_summary_val,
            width=width,
            height=height,
            close=close,
            iframe_id=uuid4().hex,
        )
