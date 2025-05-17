from act.facades.Configs.Config import Config


class Mumu:
    def getConnectStr(self) -> str:
        return f'{Config("app.addr")}:{Config("app.serial")}'