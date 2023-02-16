# Documentation with Sphinx

## Google Style Documentation & Examples

[The sphinx napoleon extension for Google and NumPy style docstrings](https://www.sphinx-doc.org/en/master/usage/extensions/napoleon.html#module-sphinx.ext.napoleon).

## Doc Generation

Run the following from repository root:

```bash
sphinx-apidoc -f -o docs/source/reference/ src/fcpp -e -M
cd docs
make html
```

Render source files to html with:

```bash
cd docs
make html
```

Delete build artifacts with:

```bash
cd docs
make clean
```

## sphinx-apidoc

Create complete API reference for a package from docstrings.
[Documentation](https://www.sphinx-doc.org/en/master/man/sphinx-apidoc.html)

```bash
# sphinx-apidoc [OPTIONS] -o <OUTPUT_PATH> <MODULE_PATH> [EXCLUDE_PATTERN …]
sphinx-apidoc -f -o source/dest/path path/to/python/module -e -M
```

Use `./docs/source/reference` for destination path.

Above options:

- `-f`: Force overwriting of any existing generated files.
- `-o`: Directory to place the output files. If it does not exist, it is created.
- `-e`: Put documentation for each module on its own page.
- `-M`: Put module documentation before submodule documentation.

## sphinx-autogen

sphinx-autogen is a tool for automatic generation of Sphinx sources that, using the autodoc extension, document items included in autosummary listing(s).
