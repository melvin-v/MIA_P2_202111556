import ctypes
import struct
from Tools.utilities import coding_str

const = '1s 1s i i i 16s'

class EBR(ctypes.Structure):
    _fields_ = [
        ('part_status', ctypes.c_char),
        ('part_fit', ctypes.c_char),
        ('start', ctypes.c_int),
        ('part_s', ctypes.c_int),
        ('next', ctypes.c_int),
        ('part_name', ctypes.c_char * 16)
    ]
    
    def __init__(self):
        self.part_status = b'0'
        self.part_fit = b'0'
        self.start = -1
        self.part_s = -1
        self.next = -1
        self.part_name = b'0'*16
    
    def setStatus(self, status):
        self.part_status = coding_str(status,1)
    
    def setFit(self, fit):
        self.part_fit = coding_str(fit, 1)
    
    def setStart(self, start):
        self.start = start
    
    def setS(self, s):
        self.part_s = s
    
    def setNext(self, next):
        self.next = next
        
    def setName(self, name):
        self.part_name = coding_str(name, 16)
    
    def set_infomation(self, status, fit, start, s, next, name):
        self.setStatus(status)
        self.setFit(fit)
        self.setStart(start)
        self.setS(s)
        self.setNext(next)
        self.setName(name)
    
    def doSerialize(self):
        return struct.pack(const, self.part_status, self.part_fit, self.start, self.part_s, self.next, self.part_name)
    
    def doDeserialize(self, data):
        self.part_status, self.part_fit, self.start, self.part_s, self.next, self.part_name = struct.unpack(const, data)