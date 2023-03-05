from string import Template


def sticky_borders_code(target_html, max_height=600, min_width=100, min_height=100):
    style_template = Template(
        """
    <style scoped>

        .dataframe-div .dataframe {
        overflow: unset;
        }

        .dataframe-div {
          max-height: ${max_height}px;
          overflow: auto;
          position: relative;
        }

        .dataframe thead th {
          position: -webkit-sticky; /* for Safari */
          position: sticky;
          top: 0;
          background: #E5E7E9;
          color: black;
          min-width: ${min_width}px;
          min-height: ${min_height}px;
        }

        .dataframe thead th:first-child {
          left: 0;
          z-index: 1;
        }

        .dataframe tbody tr th:only-of-type {
                vertical-align: middle;
            }

        .dataframe tbody tr th {
          position: -webkit-sticky; /* for Safari */
          position: sticky;
          left: 0;
          background: #E5E7E9;
          color: black;
          vertical-align: top;
          min-width: ${min_width}px;
        }
    </style>"""
    )

    style = style_template.substitute(
        {"max_height": max_height, "min_width": min_width, "min_height": min_height}
    )

    final_html = style + '<div class="dataframe-div">' + target_html + "\n</div>"
    return final_html


def sticky_borders_show_private(target_html):
    from IPython.display import HTML

    final_html = sticky_borders_code(target_html)
    return HTML(final_html)


def sticky_borders_show():
    # sticky_borders_show_private(target_html)
    raise NotImplementedError
