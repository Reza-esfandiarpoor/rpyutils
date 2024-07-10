import sys
from pathlib import Path


def bump_version(version_str, increase):
    major, minor, patch = version_str.strip().split(".")
    if increase == "major":
        major = str(int(major) + 1)
        return f"{major}.0.0"
    elif increase == "minor":
        minor = str(int(minor) + 1)
        return f"{major}.{minor}.0"
    elif increase == "patch":
        patch = str(int(patch) + 1)
        return f"{major}.{minor}.{patch}"
    else:
        raise ValueError


def main():
    assert len(sys.argv) > 1
    assert sys.argv[1] in ["major", "minor", "patch"]

    increase = sys.argv[1]

    filepath = Path(__file__).parent.joinpath("pyproject.toml")
    new_lines = list()
    with filepath.open("r") as f:
        for line in f:
            if line.startswith('version = "'):
                v = line.strip().split('"')[-2]
                v = bump_version(v, increase)
                new_lines.append(f'version = "{v}"\n')
            else:
                new_lines.append(line)

    with filepath.open("w") as f:
        f.writelines(new_lines)

    filepath = Path(__file__).parent.joinpath("src/rpyutils/__init__.py")
    new_lines = list()
    with filepath.open("r") as f:
        for line in f:
            if line.startswith('__version__ = "'):
                v = line.strip().split('"')[-2]
                v = bump_version(v, increase)
                new_lines.append(f'__version__ = "{v}"\n')
            else:
                new_lines.append(line)

    with filepath.open("w") as f:
        f.writelines(new_lines)


if __name__ == "__main__":
    main()
