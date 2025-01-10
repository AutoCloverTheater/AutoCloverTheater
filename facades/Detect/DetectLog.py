from facades.Logx import Logx

def matchResult(func):
    res,ok, = func()
    Logx.info(f"识别到页面:{res['name']}")
    return res,ok