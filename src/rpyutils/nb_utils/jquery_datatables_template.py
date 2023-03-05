from string import Template

jquery_datatable_template_string = """
<!DOCTYPE html>
<html lang="en">

<head>
    <meta charset="UTF-8" />
    <meta http-equiv="X-UA-Compatible" content="IE=edge" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>${html_file_title_sub_key}</title>

    <link rel="stylesheet" href="https://cdn.datatables.net/1.12.1/css/jquery.dataTables.min.css" />
    <link rel="stylesheet" href="https://cdn.datatables.net/fixedheader/3.2.4/css/fixedHeader.dataTables.min.css" />
    <link rel="stylesheet" href="https://cdn.datatables.net/fixedcolumns/4.1.0/css/fixedColumns.dataTables.min.css" />
    <link rel="stylesheet" href="https://cdn.datatables.net/searchbuilder/1.3.4/css/searchBuilder.dataTables.min.css" />

    <script src="https://code.jquery.com/jquery-3.5.1.js"></script>
    <script src="https://cdn.datatables.net/1.12.1/js/jquery.dataTables.min.js"></script>
    <script
        src="https://cdn.jsdelivr.net/gh/jeffreydwalter/ColReorderWithResize@9ce30c640e394282c9e0df5787d54e5887bc8ecc/ColReorderWithResize.js"></script>
    <script src="https://cdn.datatables.net/fixedheader/3.2.4/js/dataTables.fixedHeader.min.js"></script>
    <script src="https://cdn.datatables.net/fixedcolumns/4.1.0/js/dataTables.fixedColumns.min.js"></script>
    <script src="https://cdn.datatables.net/searchbuilder/1.3.4/js/dataTables.searchBuilder.min.js"></script>

    <style>
        table.dataTable tbody tr:hover {
            background-color: #71d1eb !important;
        }

        body {
            background-color: #f7f2e9;
            font-size: 13px;
            font-family: system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI",
                Roboto, Oxygen, Ubuntu, Cantarell, "Open Sans", "Helvetica Neue",
                sans-serif;
        }

        th {
            background-color: #c6c6c6 !important;
        }

        .titlebar {
            text-align: center;
            text-transform: capitalize;
        }

        .rcaptioncls {
            text-align: center;
            border-radius: 6px;
            padding: 5px 10px 5px 10px;
        }
    </style>
</head>

<body>
    <script>
        $$(document).ready(function () {
            $$('#${table_id_sub_key}').DataTable({
                pageLength: ${max_rows_sub_key},
                autoWidth: false,
                dom: '${dom_sub_key}',
                scrollX: true,
                order: [],
                fixedHeader: true,
                fixedColumns: {
                left: ${fixed_columns_sub_key},
                  },
          });
                  ${toolbar_title_sub_key}
        const element = document.getElementById("rcaptionid");
        element.style.backgroundColor = "hsl(" + ${random_hue_sub_key} + ", 75%, 75%)";
      });
    </script>
    ${table_html_code_sub_key}
</body>

</html>

"""

jquery_datatable_template = Template(jquery_datatable_template_string)
