# 神秘矿厂
from src.facades.Emulator.Emulator import ConnectEmulator
from src.facades.Runner.RefineryRunner import BeforeRefinery, InRefinery
from src.facades.Runner.layout.Back import backMain
from src.facades.Runner.layout.LoginRunner import Login

if __name__ == '__main__':
    ConnectEmulator()
    Login()
    BeforeRefinery()
    InRefinery()
    backMain()