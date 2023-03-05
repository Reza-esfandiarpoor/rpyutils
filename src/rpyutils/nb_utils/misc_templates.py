from string import Template

iframe_tag_template_string = """
<iframe srcdoc="${srcdoc_sub_key}" style="width: ${width_sub_key}; height: ${height_sub_key}; border: none"
    id="${uuid_sub_key}"></iframe>
"""

detail_with_summary_template_string = """
<style>
    .rsummarycls {
        border-radius: 6px;
        padding: 5px 10px 5px 10px;
        margin: 0px 0px 10px 0px;
        color: black;
        font-size: 13px;
        font-family: system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI",
            Roboto, Oxygen, Ubuntu, Cantarell, "Open Sans", "Helvetica Neue",
            sans-serif;
    }

    .rspancls {
        padding: 5px 10px 5px 10px;
        text-transform: capitalize;
    }
</style>
<details ${open_sub_key} class="riframedetail">
    <summary class="rsummarycls" style="background-color: hsl(${random_hue_sub_key}, 75%, 75%)">
        <span class="rspancls"><b>${summary_sub_key}</b></span>
    </summary>
    ${content_sub_key}
</details>
"""

iframe_tag_template = Template(iframe_tag_template_string)
detail_with_summary_template = Template(detail_with_summary_template_string)
