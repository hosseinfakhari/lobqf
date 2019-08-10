import os
import ctypes
from ctypes import cdll

# TODO: Make library loading process conditionaly by os type
lib_name = "liblobq.so"
lib_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "libs") + os.path.sep + lib_name
lib = cdll.LoadLibrary(lib_path)


class Row(ctypes.Structure):
    _fields_ = [('_time', ctypes.POINTER(ctypes.c_int)),
                ('_bid_price', ctypes.POINTER(ctypes.c_float)),
                ('_ask_price', ctypes.POINTER(ctypes.c_float)),
                ('_bid_volume', ctypes.POINTER(ctypes.c_float)),
                ('_ask_volume', ctypes.POINTER(ctypes.c_float))]


class LobQueue(object):
    def __init__(self, size):
        self._size = size
        self.obj = lib.fastQueue_new(size)
    
    def append(self, time, bid_pr, ask_pr, bid_vol, ask_vol):
        _bid_pr = (ctypes.c_float * len(bid_pr))(*bid_pr)
        _ask_pr = (ctypes.c_float * len(ask_pr))(*ask_pr)
        _bid_vol = (ctypes.c_float * len(bid_vol))(*bid_vol)
        _ask_vol = (ctypes.c_float * len(ask_vol))(*ask_vol)
        lib.fastQueue_append(self.obj, time, _bid_pr, _ask_pr, _bid_vol, _ask_vol)

    def peek(self, time):
        return lib.fastQueue_peek(self.obj, time)

    def __getitem(self, index):
        return lib.fastQueue_getItem(self.obj, index)

    def len(self):
        return lib.fastQueue_len(self.obj)

    def __len__(self):
        return lib.fastQueue_len(self.obj)
