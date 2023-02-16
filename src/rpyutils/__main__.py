"""Defining entry point for use in build tools to define command line use."""

import sys

from . import app


def main():
    app.run(sys.argv)


if __name__ == "__main__":
    main()
