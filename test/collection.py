# 每日高难副本
from act.facades.Detect.Items.ItemsDetect import ItemsDetect
from act.facades.Emulator.Emulator import ConnectEmulator, Pipe, Text, Click
from act.facades.Runner.ItemCollectionRunner import beforeTopLeverItemCollection, inTopLeverItemCollection
from act.facades.Runner.layout.AdventureRunner import FindAdventure
from act.facades.Runner.layout.Back import backMain
from act.facades.Runner.layout.LoginRunner import Login

def run():
    ConnectEmulator()

    Login()
    FindAdventure("hasItemsCollectionButton")

    def setInputCallBack():
        Text("99")
        Click((0.5,0.5))

    pic = Pipe()
    itemsDetect = ItemsDetect()
    (pic.waitAndClickThrough(itemsDetect.selectMap())
     .waitAndClickThrough(itemsDetect.goFormation)
     .waitUntil(itemsDetect.nowLoading, itemsDetect.openRepeatBattleWindow)
     .waitAndClick(itemsDetect.setLimit)
     .waitAndClickCallback(itemsDetect.setLimitInput,setInputCallBack)
     .waitAndClickThrough(itemsDetect.checkRepeatBattle))

    # backMain()

if __name__ == '__main__':
    run()