from act.facades.Detect.Shop.ShopDetect import ShopDetect
from act.facades.Emulator.Emulator import Pipe, Click, Swipe


def getFreePackage():
    shopDetect = ShopDetect()
    pipe = Pipe()

    def clickThenSwap(res):
        Click(res['pot'])
        Swipe((0.5,0.5),(0.5,0.4))

    def getFreeReward(res):
        x,y = res['pot']
        Click(x, y+10)

    pipe.waitAndClick(shopDetect.manWindowShop).waitAndCallback(shopDetect.shopPackage, clickThenSwap).waitAndCallback(shopDetect.freePackage, getFreeReward)