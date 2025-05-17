from act import ROOT

ROOT_PATH = ROOT
APP_PATH = ROOT_PATH.joinpath("src/app")
CONFIG_PATH = ROOT_PATH.joinpath("src/config")
RUNTIME_PATH = ROOT_PATH.joinpath("runtime")
IMG_PATH = ROOT_PATH.joinpath("img")


if __name__ == "__main__":
    print(ROOT_PATH)
    print(APP_PATH)
    print(CONFIG_PATH)
    print(RUNTIME_PATH)
    print(IMG_PATH)