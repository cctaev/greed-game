from typing import Tuple


def sleeper(
        duration: int | Tuple[int, int],
        unit: str = 's', ) -> int:
    """
    休眠函数，支持随机休眠
    :param duration: 休眠时间，单位秒。如果是元组，则表示随机休眠时间范围
    :param unit: 单位，默认为秒。支持 'ms' 毫秒， 's' 秒
    :return:
    """
    import time
    import random
    # 计算修改时间
    if isinstance(duration, Tuple):
        duration = random.randint(duration[0], duration[1])
    if duration <= 0:
        return duration
    if unit == 's':
        time.sleep(duration)
    elif unit == 'ms':
        time.sleep(duration / 1000)
    else:
        raise ValueError(f"不支持的单位：{unit}")
    return duration
