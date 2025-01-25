from facades.Configs.Config import Config


class Mumu:
    def searchAndOpenDevice(self)-> str:
        return f'{Config("app.addr")}:{Config("app.serial")}'