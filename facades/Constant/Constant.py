import pathlib

ROOT_PATH = pathlib.Path.joinpath(pathlib.Path(__file__).parent.parent.parent)
APP_PATH = ROOT_PATH.joinpath("app")
CONFIG_PATH = ROOT_PATH.joinpath("config")
RUNTIME_PATH = ROOT_PATH.joinpath("runtime")


if __name__ == "__main__":
    print(ROOT_PATH)
    print(APP_PATH)
    print(CONFIG_PATH)
    print(RUNTIME_PATH)