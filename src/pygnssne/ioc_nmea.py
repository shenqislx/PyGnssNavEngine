"""
IOController NMEA settings
"""
import nav_common as cfg
import numpy as np


class NMEAInfo:
    def __init__(self):
        self.sysid_bm = cfg.SYSBM_DEFAULT
        self.fid_bm = np.zeros(cfg.SYS_MAX, dtype=int)
        for i in range(cfg.SYS_MAX):
            self.fid_bm[i] = cfg.FIDBM_DEFAULT
