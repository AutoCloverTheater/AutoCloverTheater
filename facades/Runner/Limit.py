executionQueue = []
max_executions = 10

def limit_executions():
    """
    装饰器：限制函数或方法的执行次数。
    当执行次数达到 max_executions 时，抛出异常。
    """
    def decorator(func):
        # 用于存储执行次数的字典
        execution_count = 0

        def wrapper(*args, **kwargs):
            nonlocal execution_count
            execution_count += 1

            # 如果执行次数超过限制，抛出异常
            unique_items = set(executionQueue)
            count = {item: executionQueue.count(item) for item in unique_items}
            if func.__name__ in count and count[f'{func.__name__}'] >= max_executions:
                raise RuntimeError(f"函数 {func.__name__} 已达到最大执行次数 {max_executions}")

            if len(executionQueue) >= 20:
                executionQueue.pop(0)
            executionQueue.append(func.__name__)

            # 调用原始函数
            return func(*args, **kwargs)

        return wrapper

    return decorator

# 使用示例
@limit_executions()
def my_function():
    print("函数执行中...\n")
    print(f"数组...{executionQueue}")

if __name__ == '__main__':
    # 测试
    for i in range(12):
        try:
            my_function()
        except RuntimeError as e:
            print(e)