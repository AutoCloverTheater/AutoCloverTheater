import logging

from mac.emulator.mumu import Mumu

from src.facades.Configs.Config import Config


def testSearchAndOpenDevice():
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
    mumu = Mumu()
    mumu.searchAndOpenDevice(Config.get("app").get("adbPort"))

if __name__ == "__main__":
    testSearchAndOpenDevice()