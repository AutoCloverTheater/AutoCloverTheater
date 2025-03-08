from src.facades.Emulator.Emulator import ConnectEmulator
from src.facades.Runner.WorldTreeRunner import InWorldTree, BeforeInWorldTree
from src.facades.Runner.layout.AdventureRunner import FindAdventure
from src.facades.Runner.layout.LoginRunner import Login

if __name__ == '__main__':
    ConnectEmulator()
    Login()
    FindAdventure("hasWorldTreeButton")
    BeforeInWorldTree()
    InWorldTree()