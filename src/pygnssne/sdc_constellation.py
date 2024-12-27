"""
Satellite data controller, SATD database and related position/velocity calculation.
"""
import nav_common as ncm
from ioc_trace import logger


# --------Constant Values--------
# SDC SAT Message Status bit mask
SDC_SATM_STAT_INIT = 0x0001
SDC_SATM_STAT_EPH_VALID = 0x0002
SDC_SATM_STAT_ALM_VALID = 0x0004
SDC_SATM_STAT_EPH_FROM_RTCM = 0x0008


# --------Global Variables--------
cd = 0


# --------Class and Functions--------
def global_init():
    global cd
    cd = ConstellationData()


def calc_sats_pos_vel_clk(obs, flag_base):

    return


def get_sat_msg(prn, flag_add):
    """
    Get SAT Message by PRN.
    :param prn:
    :param flag_add:
    :return:
    """
    if ncm.check_prn(prn) is False:
        return 0
    sid, sys = ncm.convert_prn_to_sid_sys(prn)
    if sys == ncm.GPS:
        psatm = cd.satm_gps
        psatm_ip1 = cd.satm_ip1_gps
        nsatm = len(psatm)
    else:
        # TBD: other system
        return 0
    satm_ip1 = 0
    if psatm_ip1[sid - 1] != 0:
        satm_ip1 = psatm_ip1[sid - 1]
        satm_i = satm_ip1 - 1
        satm = psatm[satm_i]
        if satm.prn != prn or (satm.stat & SDC_SATM_STAT_INIT) == 0:
            logger.warning('SDC SatMsg PRN {}, {} Stat {} Error!'.format(satm.prn, prn, satm.stat))
            satm.init(prn)
    elif flag_add is True:
        satm_new = SatMsgT()
        satm_new.init(prn)
        psatm.append(satm_new)
        satm_ip1 = nsatm + 1
        psatm_ip1[sid - 1] = satm_ip1
    return satm_ip1


class SatMsgT:
    def __init__(self):
        self.prn = 0
        self.stat = 0

    def init(self, prn):
        self.prn = prn
        self.stat = SDC_SATM_STAT_INIT


class ConstellationData:
    def __init__(self):
        self.satm_gps = []              # Common SAT Message buffer for GPS
        self.msg_gps = []               # GPS LNAV-EPH messages
        self.satm_ip1_gps = [0] * 64    # Index plus 1 of GPS SATM
        self.eph_val_gps = 0            # Bit mask by SID - 1, indicate GPS LNAV EPH valid


class GpsEphT:
    def __init__(self):
        self.prn = 0
        self.toe = ncm.UTime()
        self.toc = ncm.UTime()
        self.sva = 0            # SV accuracy
        self.code2 = 0          # Code on L2, 00 - Reserved, 01 - P code on, 10 - C/A code on, 11 - L2C on
        self.idot = 0
        self.iode = 0
        self.af = [0] * 3
        self.iodc = 0
        self.crs = 0
        self.delta_n = 0        # DELTA n
        self.m0 = 0
        self.cuc = 0
        self.ecc = 0            # Eccentricity
        self.cus = 0
        self.sqrt_a = 0
        self.cic = 0
        self.omega0 = 0
        self.cis = 0
        self.i0 = 0
        self.crc = 0
        self.omg = 0            # Argument of Perigee
        self.omg_dot = 0        # Rate of Right Ascension
        self.tgd = 0
        self.health = 0
        self.p_data2 = 0        # L2 P data flag, 0 - L2 P-Code NAV data ON, 1 - L2 P-Code NAV data OFF
        self.fit = 0            # 0 - curve-fit interval is 4 hours, 1 - curve-fit is greater than 4 hour
