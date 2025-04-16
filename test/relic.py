# 遗迹探索-【噩梦难度】【热砂】
from src.facades.Emulator.Emulator import ConnectEmulator
from src.facades.Runner.RelicRunner import beforeRelic, inRelic
from src.facades.Runner.layout.AdventureRunner import FindAdventure
from src.facades.Runner.layout.LoginRunner import Login

if __name__ == '__main__':
    ConnectEmulator()

    def run():
        Login()
        FindAdventure("hasRelicButton")
        beforeRelic()
        inRelic()

    for i in range(10):
        run()