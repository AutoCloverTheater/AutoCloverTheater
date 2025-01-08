from airtest.core.api import connect_device

from facades.Emulator.Emulator import ConnectEmulator


def test_emulator():
    res = ConnectEmulator()
