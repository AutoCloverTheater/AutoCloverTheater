from facades.Configs.Config import Config


class Mumu:
    def searchAndOpenDevice(self)-> str:
        return Config("app.serial")