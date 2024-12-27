import logging

from facades.Configs.Config import Config
from mac.emulator.mumu import Mumu


def testSearchAndOpenDevice():
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
    mumu = Mumu()
    mumu.searchAndOpenDevice(Config.get("app").get("adbPort"))

if __name__ == "__main__":
    testSearchAndOpenDevice()