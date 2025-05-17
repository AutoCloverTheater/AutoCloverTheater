# 神秘矿厂
from act.facades.Emulator.Emulator import ConnectEmulator
from act.facades.Runner.RefineryRunner import BeforeRefinery, InRefinery
from act.facades.Runner.layout.Back import backMain
from act.facades.Runner.layout.LoginRunner import Login

if __name__ == '__main__':
    ConnectEmulator()
    Login()
    BeforeRefinery()
    InRefinery()
    backMain()