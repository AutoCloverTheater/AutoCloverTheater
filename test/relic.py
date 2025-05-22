# 遗迹探索-【噩梦难度】【热砂】
from act.facades.Emulator.Emulator import ConnectEmulator
from act.facades.Runner.RelicRunner import beforeRelic, inRelic
from act.facades.Runner.layout.AdventureRunner import FindAdventure
from act.facades.Runner.layout.LoginRunner import Login


def run():
    while True:
        ConnectEmulator()
        Login()
        FindAdventure("hasRelicButton")
        beforeRelic()
        inRelic()

if __name__ == '__main__':
        run()