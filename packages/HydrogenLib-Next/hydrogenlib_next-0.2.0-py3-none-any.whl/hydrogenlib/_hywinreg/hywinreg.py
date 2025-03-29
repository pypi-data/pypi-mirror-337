import os
import sys
from pathlib import Path

if sys.version not in {'3.12', '3.8', '3.7'}:
    import winreg

    reg_hkey = {
        "HKEY_CURRENT_USER": winreg.HKEY_CURRENT_USER,
        "HKEY_LOCAL_MACHINE": winreg.HKEY_LOCAL_MACHINE,
        "HEKY_CLASSES_ROOT": winreg.HKEY_CLASSES_ROOT,
        "HEKY_USERS": winreg.HKEY_USERS,
        "HEKY_CURRENT_CONFIG": winreg.HKEY_CURRENT_CONFIG
    }

    def name_to_const(name):
        reg = reg_hkey[str(name).upper()]
        return reg

    def root_to_const(reg_path):
        root = Path(reg_path).root
        reg = name_to_const(root)
        return reg

    def split_reg_path(reg_path):
        path = Path(reg_path)
        root = path.root

        reg = name_to_const(root)
        sub_path = path.relative_to(root)

        return reg, sub_path

    def touch(path: str):
        hkey, path = split_reg_path(path)
        handle = winreg.CreateKey(hkey, str(path))
        winreg.CloseKey(handle)


    class Handle:
        def __init__(self, handle):
            self._handle = handle

        def __setitem__(self, key, value):
            winreg.SetValueEx(self._handle, key, 0, pytype_to_regtype(value), value)


        def __enter__(self):
            return self

        def __del__(self):
            winreg.CloseKey(self._handle)


    class Registry:
        def __init__(self, path):
            self.hkey, self.path = split_reg_path(path)

        @property
        def name(self):
            return self.path.name


    # def add_to_startup(name, file_path=""):
    #     # By IvanHanloth
    #     if file_path == "":
    #         file_path = os.path.realpath(sys.argv[0])
    #     key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, r"Software\Microsoft\Windows\CurrentVersion\Run",
    #                          winreg.KEY_SET_VALUE,
    #                          winreg.KEY_ALL_ACCESS | winreg.KEY_WRITE | winreg.KEY_CREATE_SUB_KEY)  # By IvanHanloth
    #     winreg.SetValueEx(key, name, 0, winreg.REG_SZ, file_path)
    #     winreg.CloseKey(key)
    #
    #
    # def remove_from_startup(name):
    #     key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, r"Software\Microsoft\Windows\CurrentVersion\Run",
    #                          winreg.KEY_SET_VALUE,
    #                          winreg.KEY_ALL_ACCESS | winreg.KEY_WRITE | winreg.KEY_CREATE_SUB_KEY)  # By IvanHanloth
    #     try:
    #         winreg.DeleteValue(key, name)
    #
    #     except FileNotFoundError:
    #         print(f"{name} not found in startup.")
    #     else:
    #         print(f"{name} removed from startup.")
    #
    #     winreg.CloseKey(key)


    def get_all(reg_path: str):
        """
        sepstr be \\
        """
        d = {}

        reg = root_to_const(reg_path)

        try:
            key = winreg.OpenKey(reg, reg_path)
        except OSError:
            return d

        # 获取该键的所有键值，遍历枚举
        try:
            i = 0
            while 1:
                # EnumValue方法用来枚举键值，EnumKey用来枚举子键
                name, value, _type = winreg.EnumValue(key, i)
                d[name] = (name, value, _type)
                i += 1
        except OSError:
            pass

        return d


    def pytype_to_regtype(pyType: object, big_type: bool = False):
        if isinstance(pyType, int):  # pyType为int
            if big_type:
                return winreg.REG_QWORD
            else:
                return winreg.REG_DWORD
        elif isinstance(pyType, float):  # pyType = float
            return ValueError("REG types not have 'float'.")
        elif isinstance(pyType, str):
            if big_type:
                return winreg.REG_EXPAND_SZ
            else:
                return winreg.REG_SZ
        else:
            return ValueError(f"pyType '{pyType}' don't turn to 'REG_TYPE'.")


    def set_reg_key(reg_path: str, _type: int, value):
        path = Path(reg_path)
        r = root_to_const(reg_path)
        k = winreg.OpenKey(r, p, 0, winreg.KEY_SET_VALUE)
        winreg.SetValueEx(k, name, 0, _type, value)
