class Bluestacks:
    def GetSerial(self) -> str:
        return "emulator-5554"
    def Devices(self)-> list:
        return ["emulator-5554"]

    def Activate(self, serial ="") -> bool:
        return True