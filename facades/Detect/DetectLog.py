from facades.Logx.Logx import logx


def matchResult(func):
    def wrapper(self, *args, **kwargs):

        # 调用原始方法
        result,ok = func(self, *args, **kwargs)
        if ok :
            logx.info(f"识别到页面:{result['name']}")

        return result,ok

    return wrapper