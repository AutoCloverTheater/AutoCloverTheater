# 每日高难副本
from src.facades.Emulator.Emulator import ConnectEmulator
from src.facades.Runner.ItemCollectionRunner import beforeTopLeverItemCollection, inTopLeverItemCollection
from src.facades.Runner.layout.AdventureRunner import FindAdventure
from src.facades.Runner.layout.Back import backMain
from src.facades.Runner.layout.LoginRunner import Login

if __name__ == '__main__':
    ConnectEmulator()

    Login()
    FindAdventure("hasItemsCollectionButton")

    for i in range(4):
        beforeTopLeverItemCollection()
        inTopLeverItemCollection()

    backMain()