import pathlib

ROOT = pathlib.Path.joinpath(pathlib.Path(__file__).parent.parent)


if __name__ == "__main__":
    print(pathlib.Path(__file__))
    print(ROOT)