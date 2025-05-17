class HumanHandleException(Exception):
    """用户主动接管"""
    def __init__(self, message):
        super().__init__(message)  # 初始化父类

    def __str__(self):
        # 自定义异常的输出格式
        return f"{super().__str__()}"