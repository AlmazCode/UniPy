import platform as ptf
import getpass
import sys

_platform = ptf.system()
_machine = ptf.uname()[4]
_defaultPath = None
_userName = getpass.getuser()
s = "/"
if _platform == "Windows":
    _defaultPath = f"C:\\Users\\{_userName}\\"
    s = "\\"
elif _platform == "Darwin":
    _defaultPath = f"/Users/{_userName}/"
elif _platform == "Linux" and not hasattr(sys, 'getandroidapilevel'):
    _defaultPath = f"/home/{_userName}/"
else:
    _platform = "Android"
    _defaultPath = "/storage/emulated/0"