from typing import Union
from uuid import uuid4

from IPython.display import HTML

from . import misc_templates


def get_iframe_tag(
    html_str: str, width: str, height: str, iframe_id: Union[str, None] = None
) -> str:
    """Embed html string in an iframe tag.

    Args:
        html_str (str): The html string to embed
        width (str): Width of the iframe tag in css format
        height (str): Height of the iframe tag in css format
        iframe_id (Union[str, None], optional): The value for the id property of iframe tag. Defaults to None.

    Returns:
        str: the html code of the iframe tag with the embedded content.
    """

    sub_map = {
        "srcdoc_sub_key": html_str.replace('"', "&quot;"),
        "width_sub_key": width,
        "height_sub_key": height,
        "uuid_sub_key": iframe_id or uuid4().hex,
    }
    return misc_templates.iframe_tag_template.substitute(sub_map)


def wrap_in_detail_with_summary(
    content: str, summary: str, random_hue: Union[str, int], close: bool = False
) -> str:
    """Wraps html code in a a detail tag with summary

    Args:
        content (str): html code to embed in detail tag
        summary (str): content of the summary tag
        random_hue (Union[str, int]): the background color of the summary text. H value in HSI.
        close (bool, optional): if the detail tag should be closed initially. Defaults to False.

    Returns:
        str: the html code of the detail tag
    """

    random_hue = str(random_hue)
    sub_map = {
        "content_sub_key": content,
        "summary_sub_key": summary,
        "random_hue_sub_key": random_hue,
        "open_sub_key": " " if close else " open",
    }
    return misc_templates.detail_with_summary_template.substitute(sub_map)


def show_html(
    html_str: str,
    html_iframe_tag: bool = False,
    wrap_in_detail: bool = False,
    detail_summary: Union[str, None] = None,
    width: Union[str, None] = None,
    height: Union[str, None] = None,
    iframe_id: Union[str, None] = None,
    close: bool = False,
    random_hue: Union[str, int] = 100,
) -> HTML:
    """Create the appropriate HTML object to display the html code in a jupyter notebook

    Args:
        html_str (str): the html code to display
        html_iframe_tag (bool, optional): if the html code should be wrapped in an html iframe tag. Defaults to False.
        wrap_in_detail (bool, optional): if the html code (or the surrounding iframe tag) should be wrapped in a detail tag. Defaults to False.
        detail_summary (Union[str, None], optional): the content of the summary tag in a html detail tag. Defaults to None.
        width (Union[str, None], optional): Width of the iframe tag in css format. Defaults to None.
        height (Union[str, None], optional): Height of the iframe tag in css format. Defaults to None.
        iframe_id (Union[str, None], optional): The value for the id property of iframe tag. Defaults to None.
        close (bool, optional): if the detail tag should be closed initially. Defaults to False.
        random_hue (Union[str, int], optional): the background color of the summary text. H value in HSI. Defaults to 100.

    Returns:
        HTML: an instance of HTML class displaying the `html_str` code
    """

    assert not html_iframe_tag or (html_iframe_tag and width and height)

    if html_iframe_tag:
        html_str = get_iframe_tag(html_str, width, height, iframe_id)
    else:
        html_str = html_str.replace('"', "&quot;")

    if wrap_in_detail:
        detail_summary = "" if detail_summary is None else detail_summary
        html_str = wrap_in_detail_with_summary(
            html_str, detail_summary, random_hue, close
        )
    return HTML(html_str)


def rchange_details(close: bool) -> HTML:
    """close or open all the detail tags in the notebook

    Args:
        close (bool): the target state of the detail tag

    Returns:
        HTML: the necessary html code to close/open detail tags
    """

    close_tag = "false" if close else "true"
    html_str = f"""
    <script>
        document.querySelectorAll('.riframedetail').forEach(e => e.open = {close_tag});
    </script>
    """
    return HTML(html_str)
