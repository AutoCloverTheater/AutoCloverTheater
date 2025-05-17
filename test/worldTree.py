from act.facades.Emulator.Emulator import ConnectEmulator
from act.facades.Runner.WorldTreeRunner import InWorldTree, BeforeInWorldTree
from act.facades.Runner.layout.AdventureRunner import FindAdventure
from act.facades.Runner.layout.LoginRunner import Login

if __name__ == '__main__':
    ConnectEmulator()
    Login()
    FindAdventure("hasWorldTreeButton")
    BeforeInWorldTree()
    InWorldTree()