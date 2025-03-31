# -*- coding: utf-8 -*-
# @Project: 芒果测试平台
# @Description: 
# @Time   : 2025-02-26 11:46
# @Author : 毛鹏
import platform

system = platform.system().lower()
if system == "windows":
    from mangokit.mangos.pyarmor_runtime_windows.mango import Mango
elif system == "linux":
    from mangokit.mangos.pyarmor_runtime_linux.mango import Mango
elif system == "Darwin":  # macOS
    from mangokit.mangos.pyarmor_runtime_linux.mango import Mango
else:
    raise RuntimeError(f"Unsupported platform: {system}")
