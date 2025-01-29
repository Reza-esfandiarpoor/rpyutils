import random
from pathlib import Path
from typing import Union
from uuid import uuid4

import pandas as pd
from IPython.display import HTML

from . import iframe_html_utils, jquery_datatables_template


def fancy_table(
    data: Union[str, pd.DataFrame],
    fixed_columns: int = 1,
    searchable: bool = False,
    max_rows: int = 10,
    caption: Union[str, None] = None,
    height: str = "600px",
    width: str = "100%",
    show: bool = True,
    file: Union[str, None] = None,
    save: Union[bool, None] = None,
    close: bool = False,
    html_escape=False,
    html_float_fmt="{:.2f}",
    silent=False,
) -> Union[HTML, None]:
    """Displays the input with [jQuery DataTables](https://datatables.net).

    The output is either saved to an html file or returned in a jupyter notebook HTML object.

    Args:
        data (Union[str, pd.DataFrame]): The input data. It can be a pd.DataFrame or
                the html code of a table (e.g. the output of `df.to_html()`).
        fixed_columns (int, optional): The number of frozen columns on the left when scrolling. Defaults to 1.
        searchable (bool, optional): Enable the more complex search builder. Defaults to False.
        max_rows (int, optional): Number of rows in each page. Defaults to 10.
        caption (Union[str, None], optional): Caption of the table. Defaults to None.
        height (str, optional): Height of the output in css format. Defaults to "600px".
        width (str, optional): Width of the output in css format. Defaults to "100%".
        show (bool, optional): Show the table (i.e. return an HTML object). Defaults to True.
        file (Union[str, None], optional): Output html file. Defaults to None.
        save (Union[bool, None], optional): Save the table in an html file. Can be True/False/None. Defaults to None.
            The table is saved to file if `(save == None and file != None) or save == True`
        close (bool, optional): if the detail tag should be closed initially. Defaults to False.
        silent: If True, do not print info messages.

    Returns:
        Union[HTML, None]: The table either in an HTML object if show is True.
    """

    if isinstance(data, str):
        orig_table_html_code = data
    elif isinstance(data, pd.DataFrame):
        orig_table_html_code = data.to_html(
            escape=html_escape, float_format=lambda x: html_float_fmt.format(x)
        )
    else:
        raise ValueError
    uuid_ = uuid4().hex
    table_html_code = orig_table_html_code.replace(
        "<table ", f'<table id="{uuid_}" '
    ).replace('class="', 'class="display compact ')

    dom = "Rlfrtip"
    if searchable:
        dom = "Q" + dom

    if caption is not None:
        provided_caption = caption
    elif file is not None:
        provided_caption = file.split("/")[-1].split(".")[0]
    else:
        provided_caption = ""

    if provided_caption == "":
        table_colored_title = ""
        detail_tag_summary = "fancy table"
        html_file_title = "fancy table".title()
    else:
        detail_tag_summary = provided_caption
        html_file_title = provided_caption.title()
        dom = dom.replace("t", '<"titlebar">t')

        colored_span_tag = (
            '<span id="rcaptionid" class="rcaptioncls">'
            f"<b>{provided_caption}</b></span>"
        )
        table_colored_title = f"$('div.titlebar').html('{colored_span_tag} ');"

    random_hue = str(random.randrange(0, 360, 20))

    substitute_mapping = {
        "table_html_code_sub_key": table_html_code,
        "max_rows_sub_key": max_rows,
        "table_id_sub_key": uuid_,
        "dom_sub_key": dom,
        "fixed_columns_sub_key": fixed_columns,
        "toolbar_title_sub_key": table_colored_title,
        "html_file_title_sub_key": html_file_title,
        "random_hue_sub_key": random_hue,
    }

    main_html_code = jquery_datatables_template.jquery_datatable_template.substitute(
        substitute_mapping
    )

    main_html_code = main_html_code.replace("<th></th>", "<th>idx</th>")

    if (save == None and file != None) or save == True:
        path = Path(file or "fancy_table.html")
        path.parent.mkdir(exist_ok=True, parents=True)
        with path.open("wt", encoding="utf8") as f:
            f.write(main_html_code)
        if not silent:
            print(f"Saved to {path}")

    if show:
        return iframe_html_utils.show_html(
            main_html_code,
            html_iframe_tag=True,
            wrap_in_detail=True,
            detail_summary=detail_tag_summary,
            width=width,
            height=height,
            close=close,
            random_hue=random_hue,
            iframe_id=uuid4().hex,
        )
