from airtest.core.api import touch, swipe, text


class BaseDetect:
    def click(self, pso : tuple):
        touch(pso)
        return self

    def swip(self,form : tuple, to : tuple):
        swipe(form, to)
        return self

    def input(self, inputStr:str):
        text(inputStr, paste=True)
        return self