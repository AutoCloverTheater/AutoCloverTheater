# 每日素材本
from act.facades.Emulator.Emulator import ConnectEmulator
from act.facades.Runner.ItemCollectionRunner import ItemCollectionInBattleWaitResult, ItemCollectionRepSetting
from act.facades.Runner.layout.AdventureRunner import FindAdventure
from act.facades.Runner.layout.Back import backMain
from act.facades.Runner.layout.LoginRunner import Login

def run():
    ConnectEmulator()

    Login()
    FindAdventure("hasItemsCollectionButton")

    ItemCollectionRepSetting()

    # 自动战斗中，等待结束
    ItemCollectionInBattleWaitResult()

    # 返回主界面
    backMain()

if __name__ == '__main__':
    run()