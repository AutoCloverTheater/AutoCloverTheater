from act import ROOT

ROOT_PATH = ROOT
APP_PATH = ROOT_PATH.joinpath("act/app")
CONFIG_PATH = ROOT_PATH.joinpath("act/config")
RUNTIME_PATH = ROOT_PATH.joinpath("runtime")
IMG_PATH = ROOT_PATH.joinpath("img")
ENV_PATH = ROOT_PATH.joinpath("etc/env.yaml")


if __name__ == "__main__":
    print(ROOT_PATH)
    print(APP_PATH)
    print(CONFIG_PATH)
    print(RUNTIME_PATH)
    print(IMG_PATH)