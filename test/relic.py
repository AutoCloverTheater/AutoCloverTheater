# 遗迹探索-【噩梦难度】【热砂】
from act.facades.Emulator.Emulator import ConnectEmulator
from act.facades.Runner.RelicRunner import beforeRelic, inRelic
from act.facades.Runner.layout.AdventureRunner import FindAdventure
from act.facades.Runner.layout.LoginRunner import Login

if __name__ == '__main__':
    ConnectEmulator()

    def run():
        Login()
        FindAdventure("hasRelicButton")
        beforeRelic()
        inRelic()

    for i in range(10):
        run()