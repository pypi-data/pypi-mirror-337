"""
Use:
    from ctypes import c_int
    dll = HyDll(<dll_name>, STDCALL | C)

    @dll.function
    def AnyFunction(a: c_int, b: c_int) -> None: ...

    @dll.function
    def ... ( ... ) -> ... : ...
"""

from .dll import HyDll
from .universality import HyStructure
