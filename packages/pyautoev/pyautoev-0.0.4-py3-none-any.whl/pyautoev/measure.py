import time
from dataclasses import dataclass

@dataclass
class MeasureResult:
    """定义测量结果的数据结构"""
    result: any
    elapsed_time: str

def measure_(func, *args, **kwargs):
    """用于测量某个函数的执行时间，并返回结果和耗时"""
    start_time = time.time()
    try:
        result = func(*args, **kwargs)
    except Exception as e:
        # 捕获异常并记录耗时
        end_time = time.time()
        elapsed_time = f"{end_time - start_time:.2f}"
        return MeasureResult(result=str(e), elapsed_time=elapsed_time)

    end_time = time.time()
    elapsed_time = f"{end_time - start_time:.2f}"
    return MeasureResult(result=result, elapsed_time=elapsed_time)

