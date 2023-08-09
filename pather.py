import platform as ptf
import getpass

andoirdMachines = ["armv8l", "armv7l", "aarch64", "x86_64"]
_platform = ptf.system()
_machine = ptf.uname()[4]
_defaultPath = None
_userName = getpass.getuser()
s = None
if _platform == "Windows":
    _defaultPath = f"C:\\Users\\{_userName}\\"
    s = "\\"
elif _platform == "Darwin":
    _defaultPath = f"/Users/{_userName}/"
    s = "/" 
elif _platform == "Linux" and _machine not in andoirdMachines:
    _defaultPath = f"/home/{_userName}/"
    s = "/"
else:
    _platform = "Android"
    _defaultPath = "/storage/emulated/0"
    s = "/"