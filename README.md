# FCPP

[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Imports: isort](https://img.shields.io/badge/%20imports-isort-%231674b1?style=flat&labelColor=ef8336)](https://pycqa.github.io/isort/)

A simple python project to learn and collect best practices for python package development and release.

See [Docs](https://dochosting.gitlab.io/shadowfcpp/) for details.

## TODO

- [ ] ~~[How to Publish an Open-Source Python Package to PyPI](https://realpython.com/pypi-publish-python-package/#get-to-know-python-packaging)~~
- [ ] Testing
  - [ ] [Getting Started With Testing in Python](https://realpython.com/python-testing)
  - [ ] [Configuring Tox for Your Dependencies](https://realpython.com/python-testing/#testing-in-multiple-environments)
  - [ ] [Effective Python Testing With Pytest](https://realpython.com/pytest-python-testing)
  - [ ] [Build a Hash Table in Python With TDD](https://realpython.com/python-hash-table/)
  - [ ] [Python Practice Problems: Parsing CSV Files](https://realpython.com/python-interview-problem-parsing-csv-files/)
- [x] ~~[Documentation](https://realpython.com/documenting-python-code/)~~
- [ ] ~~[`MANIFEST.in`](https://packaging.python.org/en/latest/guides/using-manifest-in/)~~
- [x] ~~Versioning~~
- [x] ~~command line entry point~~
- [ ] Linter

## Not Priority

- [Implementing an Interface in Python](https://realpython.com/python-interface/): it is talking about api interface.

## Notes

- When you run a package with `-m`, the file `__main__.py` within the package is executed.
- Adding & removing files to & from the source distribution is done by writing a `MANIFEST.in` file at the project root.
- According to PEP 8, comments should have a maximum length of 72 characters.

## Contributing

The repo uses [black](https://github.com/psf/black) and [isort](https://github.com/PyCQA/isort) for code formatting.  
Run the following to install the hooks using [pre-commit](https://pre-commit.com/).

```bash
pip install pre-commit
pre-commit install
```
