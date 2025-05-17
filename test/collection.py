# 每日高难副本
from act.facades.Emulator.Emulator import ConnectEmulator
from act.facades.Runner.ItemCollectionRunner import beforeTopLeverItemCollection, inTopLeverItemCollection
from act.facades.Runner.layout.AdventureRunner import FindAdventure
from act.facades.Runner.layout.Back import backMain
from act.facades.Runner.layout.LoginRunner import Login

if __name__ == '__main__':
    ConnectEmulator()

    Login()
    FindAdventure("hasItemsCollectionButton")

    for i in range(4):
        beforeTopLeverItemCollection()
        inTopLeverItemCollection()

    backMain()