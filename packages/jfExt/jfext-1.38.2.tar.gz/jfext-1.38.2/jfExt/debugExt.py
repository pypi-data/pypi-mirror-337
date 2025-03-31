# -*- coding: utf-8 -*-
"""
jf-ext.debugExt.py
~~~~~~~~~~~~~~~~~~

:copyright: (c) 2018-2022 by the Ji Fu, see AUTHORS for more details.
:license: MIT, see LICENSE for more details.
"""

import time
import sys
import inspect
from icecream import ic # noqa
from jfExt.PrintExt import *
from jfExt.CommonExt import get_latency_msg_for_millisecond, get_latency_str_for_millisecond


time_dict = {}

def debug_timeout_set_by_key(key):
    """
    >>> 调试: 延迟计算 - 设置起始点 by key
    :param {String} key:
    """
    time_dict[key] = time.time()


def debug_timeout_get_by_key(key):
    """
    >>> 调试: 延迟计算 - 获取 by key
    :param {String} key:
    """
    end_time = time.time()
    start_time = time_dict.get(key, None)
    # 未找到起始时间, 返货None
    if not start_time:
        return None
    proc_time = int((end_time - start_time) * 1000)
    msg = "🦞{}".format(get_latency_msg_for_millisecond(proc_time, key))
    print(msg)
    return msg


def debug_tracking_call_timeout(tag=None):
    """
    >>> 调试: 调用跟踪
    """
    tag_str = f"[{tag}]" if tag else ""
    # 获取调用位置
    stack = inspect.stack()[1]  # 获取上一层调用信息
    caller_filename = stack.filename.split("/")[-1]  # 获取文件名（去掉路径）
    caller_lineno = stack.lineno  # 获取行号

    if not hasattr(debug_tracking_call_timeout, "last_time"):
        debug_tracking_call_timeout.last_time = time.perf_counter()  # 初始化
        print_str = f"📌 > {tag_str} 首次调用（{caller_filename}:{caller_lineno}），开始计时..."
        print(get_color_text_by_type("*" * 80, bcolors.HLERROR))
        print(get_color_text_by_type(print_str, bcolors.HLERROR))
        print(get_color_text_by_type("*" * 80, bcolors.HLERROR))
        sys.stdout.flush()
        return

    current_time = time.perf_counter()
    elapsed_time_ms = (current_time - debug_tracking_call_timeout.last_time) * 1000  # 转换为毫秒
    debug_tracking_call_timeout.last_time = current_time  # 更新上次调用时间

    latency_str = get_latency_str_for_millisecond(elapsed_time_ms)
    print_str = f"⏳ > {tag_str} 距离上次调用({caller_filename}:{caller_lineno}) [{latency_str}]: {elapsed_time_ms:.2f} ms"
    print(get_color_text_by_type("*" * 80, bcolors.HLERROR))
    print(get_color_text_by_type(print_str, bcolors.HLERROR))
    print(get_color_text_by_type("*" * 80, bcolors.HLERROR))
    sys.stdout.flush()


if __name__ == '__main__':
    # debug_timeout_set_by_key("A")
    # time.sleep(1.1113)
    # debug_timeout_get_by_key("A")
    # 示例调用：
    debug_tracking_call_timeout('ABC')  # 首次调用
    time.sleep(0.2)
    debug_tracking_call_timeout("ABC")  # 1200+ ms
    time.sleep(0.3)
    debug_tracking_call_timeout()  # 300+ ms
    time.sleep(0.1)
    debug_tracking_call_timeout()  # 2000+ ms
