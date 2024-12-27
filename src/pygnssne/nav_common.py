"""
NAV Common Data, Constant values and global variables
"""
# import numpy as np
import math

# --------Constant Values--------
GPS = 0
BDS = 1
GLO = 2
GAL = 3
IRS = 4
QZS = 5
SBS = 6
BD2 = 7
SYS_MAX = 8
# GPS FREQ
L1 = 0
L2C = 1
L5 = 2
# BDS FREQ
B1 = 0
B1C = 1
B3 = 2
B2A = 3
B2B = 4
B2 = 5
# GAL FREQ
E1 = 0
E5A = 1
E5B = 2
E6 = 3
# GLO FREQ
G1 = 0
G2 = 1
# SIGNAL ID
GPS_L1 = GPS | (L1 << 3)
QZS_L1 = QZS | (L1 << 3)
SBS_L1 = SBS | (L1 << 3)
BDS_B1C = BDS | (B1C << 3)
BDS_B1 = BDS | (B1 << 3)
GAL_E1 = GAL | (E1 << 3)
GLO_G1 = GLO | (G1 << 3)
GPS_L2C = GPS | (L2C << 3)
QZS_L2C = QZS | (L2C << 3)
GLO_G2 = GLO | (G2 << 3)
BDS_B3 = BDS | (B3 << 3)
GPS_L5 = GPS | (L5 << 3)
QZS_L5 = QZS | (L5 << 3)
SBS_L5 = SBS | (L5 << 3)
IRS_L5 = IRS | (L5 << 3)
BDS_B2A = BDS | (B2A << 3)
GAL_E5A = GAL | (E5A << 3)
GAL_E5B = GAL | (E5B << 3)
BDS_B2B = BDS | (B2B << 3)
BDS_B2 = BDS | (B2 << 3)
GAL_E6 = GAL | (E6 << 3)

SYS_INVALID = 0xFF

SYSBM_INVALID = 0x0000
SYSBM_GPS = 1 << GPS
SYSBM_BDS = 1 << BDS
SYSBM_GLO = 1 << GLO
SYSBM_GAL = 1 << GAL
SYSBM_IRS = 1 << IRS
SYSBM_QZS = 1 << QZS
SYSBM_SBS = 1 << SBS
SYSBM_ALL = 0xFFFF
SYSBM_DEFAULT = 0x007F
FIDBM_DEFAULT = 0x0F

FREQ_L1A = 0  # GPS/SBS/QZS: L1, BDS: B1I or B1C, GAL: E1, GLO G1
FREQ_L5A = 1  # GPS/QZS/IRS: L5, BDS: B2a, GAL: E5a
FREQ_L5B = 2  # BDS: B2b, GAL: E5b
FREQ_L2A = 3  # GPS/QZS: L2C, BDS: B3I, GAL: E6, GLO G2
FREQ_L1B = 4  # BDS: B1C or B1I
FREQ_MAX_ID = 5

MIN_GPS_SAT_PRN = 1
MAX_GPS_SAT_PRN = 32
MIN_QZS_SAT_PRN = 33
MAX_QZS_SAT_PRN = 42
MIN_QZS_QZO_SAT_PRN = MIN_QZS_SAT_PRN
MAX_QZS_QZO_SAT_PRN = MIN_QZS_SAT_PRN + 4
MIN_QZS_GEO_SAT_PRN = MAX_QZS_QZO_SAT_PRN + 1
MAX_QZS_GEO_SAT_PRN = MAX_QZS_SAT_PRN
MIN_SBS_SAT_PRN = 141
MAX_SBS_SAT_PRN = 165
MIN_BDS_SAT_PRN = 191
MAX_BDS_SAT_PRN = 253
MIN_GLO_SAT_PRN = 65
MAX_GLO_SAT_PRN = 92
MIN_GAL_SAT_PRN = 95
MAX_GAL_SAT_PRN = 130
MIN_IRS_SAT_PRN = 170
MAX_IRS_SAT_PRN = 183

NE_OBSI_INVALID = 0xFF

NE_CFG_STAT_INIT = 0x01

# NE status bit mask
NE_STAT_INIT = 0x0001
NE_STAT_RCV1_OBSLO_UPDATED = 0x0002
NE_STAT_BASE_OBSLO_UPDATED = 0x0004
NE_STAT_BASE_VALID = 0x0008
NE_STAT_IS_MAIN_EPOCH = 0x0010
NE_STAT_IS_MMNI_EPOCH = 0x0020  # Mini-Mini Epoch in high rate RTK mode

# Positioning Mode, Enumeration
NE_PMODE_SOLU_TYPE = 0x0F
NE_PMODE_UNK = 0
NE_PMODE_SPS = 1
NE_PMODE_SBS = 2
NE_PMODE_RTD = 3
NE_PMODE_RTK = 4
NE_PMODE_PPP = 5
NE_PMODE_MIX = 6
NE_PMODE_DUA = 7

# RTK Ambiguity Resolution Method, Enumeration
NE_AMODE_UNKNOWN = 0
NE_AMODE_FLOAT = 1
NE_AMODE_FIX_RTK_NORMAL = 2
NE_AMODE_FIX_RTK_WIDE_LANE = 3
NE_AMODE_FIX_RTK_WL_TO_NC = 4
NE_AMODE_FIX_RTK_WL_TO_NL = 5
NE_AMODE_FIX_RTK_GREEDY = 6

# Receiver dynamic mode, Enumeration
NE_RMODE_AUTO = 0
NE_RMODE_STATIC_MODE = 1
NE_RMODE_LOW_DYNAMIC = 2
NE_RMODE_MID_DYNAMIC = 3
NE_RMODE_DRIVE_MODE = 4
NE_RMODE_TRAIN_MODE = 5
NE_RMODE_UAV_LOW_MODE = 6
NE_RMODE_UAV_MID_MODE = 7
NE_RMODE_FLIGHT_MODE = 8
NE_RMODE_CARD_MODE = 9
NE_RMODE_WEAR_MODE = 10
NE_RMODE_BIKE_MODE = 11
NE_RMODE_BASE_MODE = 12
NE_RMODE_MAX_MODE = NE_RMODE_BASE_MODE

# Base station type
NE_STA_TYPE_UNKNOWN = 0
NE_STA_TYPE_BASE_FIX = 1
NE_STA_TYPE_BASE_VRS = 2

# Lost Lock Indicator
NE_LLI_SLIP = 0x01  # LLI: cycle-slip
NE_LLI_HALFC = 0x02  # LLI: half-cycle not resolved
NE_LLI_INVALID = 0x03
NE_LLI_BOCTRK = 0x04  # LLI: boc tracking of mboc signal

# Constants
CLIGHT = 299792458.0  # speed of light (m/s)
CLIGHT_MS = 299792.4580  # speed of light (m/ms)

# Nominal wave length (m)
WAVEL_L1 = 0.19029367280  # L1/E1  wave length (m)
WAVEL_L2 = 0.24421021342  # L2     wave length (m)
WAVEL_L5 = 0.25482804879  # L5/E5a wave length (m)
WAVEL_E6 = 0.23444180489  # E6/LEX wave length (m)
WAVEL_E5B = 0.24834936958  # E5b    wave length (m)
WAVEL_E5 = 0.25154700095  # E5a+b  wave length (m)
WAVEL_B1 = 0.19203948631  # BeiDou B1 wave length (m)
WAVEL_B2 = 0.24834936958  # BeiDou B2 wave length (m)
WAVEL_B3 = 0.23633246460  # BeiDou B3 wave length (m)
WAVEL_G1 = 0.18713636579  # GLONASS G1 base wave length (m)
WAVEL_G2 = 0.24060389888  # GLONASS G2 base wave length (m)
WAVEL_G3 = 0.24940617541  # GLONASS G3 wave length (m)
WAVEL_NONE = 0.0

# Nominal Radio Frequency (Hz)
RFREQ_L1 = 1.57542E9  # L1/E1  frequency (Hz) */
RFREQ_L2 = 1.22760E9  # L2     frequency (Hz) */
RFREQ_L5 = 1.17645E9  # L5/E5a frequency (Hz) */
RFREQ_E6 = 1.27875E9  # E6/LEX frequency (Hz) */
RFREQ_E5B = 1.20714E9  # E5b    frequency (Hz) */
RFREQ_E5 = 1.191795E9  # E5a+b  frequency (Hz) */
RFREQ_B1 = 1.561098E9  # BeiDou B1 frequency (Hz) */
RFREQ_B2 = 1.20714E9  # BeiDou B2 frequency (Hz) */
RFREQ_B3 = 1.26852E9  # BeiDou B3 frequency (Hz) */
RFREQ_G1 = 1.60200E9  # GLONASS G1 base frequency (Hz) */
DFREQ_G1 = 0.56250E6  # GLONASS G1 bias frequency (Hz/n) */
RFREQ_G2 = 1.24600E9  # GLONASS G2 base frequency (Hz) */
DFREQ_G2 = 0.43750E6  # GLONASS G2 bias frequency (Hz/n) */
RFREQ_G3 = 1.202025E9  # GLONASS G3 frequency (Hz) */
RFREQ_NONE = 0.0

# --------Global Variables--------
navd = 0
navc = 0
navi = 0


# --------Class and Functions--------
def global_init():
    global navd
    global navc
    global navi
    navd = NavData()
    obsb = navd.obsb
    obsb.nmax = 64
    obsb.nmax_frq = 400
    obsr = navd.obsr
    obsr.nmax = 64
    obsr.nmax_frq = 400
    navc = NavCfg()
    navc.stat |= NE_CFG_STAT_INIT
    navi = NavInfo()
    navi.stat |= NE_STAT_INIT


def copy_json_cfg(jsonc):
    navc.flag_base_val = jsonc.flag_base_val
    navc.fp_meas_rtcm = jsonc.fp_meas_rtcm
    navc.fp_base_rtcm = jsonc.fp_base_rtcm
    ut = conv_ctime2utime(jsonc.rtcm_date)
    navc.rtcm_wn = ut.wn
    navc.sys_enable = jsonc.sys_enable
    navc.dyna_mode = jsonc.dyna_mode


def set_base_station(station):
    if navi.en_base is False:
        return
    if navd.base.id != station.id and station.type != NE_STA_TYPE_UNKNOWN:
        # Base station switch issue
        navd.base.update(station)  # TBD: backup new station data
        navd.flag_base_switch = True
    else:
        # Save station data to nav data
        navd.base = station


class NavCfg:
    def __init__(self):
        self.fp_meas_rtcm = None
        self.flag_base_val = False
        self.fp_base_rtcm = None
        self.sys_enable = 0
        self.dyna_mode = 0
        self.rtcm_wn = 0
        self.stat = 0
        self.mode_pos = NE_PMODE_RTK
        self.mode_ar_rtk = NE_AMODE_FIX_RTK_WL_TO_NC
        self.mode_ar_ppp = NE_AMODE_FLOAT
        self.mode_ar_glo = NE_AMODE_FLOAT


class Station:
    def __init__(self):
        self.id = 0
        self.type = NE_STA_TYPE_UNKNOWN
        self.itrf_year = 0
        self.gps_indi = 0
        self.glo_indi = 0
        self.gal_indi = 0
        self.ref_indi = 0
        self.sro_indi = 0
        self.qcy_indi = 0
        self.xyz = [0] * 3
        self.height = 0

    def update(self, sta):
        self.id = sta.id
        self.type = sta.type
        self.itrf_year = sta.itrf_year
        self.gps_indi = sta.gps_indi
        self.glo_indi = sta.glo_indi
        self.gal_indi = sta.gal_indi
        self.ref_indi = sta.ref_indi
        self.sro_indi = sta.sro_indi
        self.qcy_indi = sta.qcy_indi
        self.xyz = sta.xyz
        self.height = sta.height


class NavObsDataT:
    def __init__(self):
        self.prn = 0
        self.sid = 0
        self.sys = 0
        self.fbm = 0  # Freq. bit mask
        self.fbm_upd = 0  # Freq. bit mask used to sync OBS_IN FREQ
        self.ip1_freq = [0] * FREQ_MAX_ID  # Index plus 1 to check freq data validity
        # For Rover OBS Database
        self.obsd_frq = []  # OBSD FREQ package
        # For Base OBS Database
        self.obsb_frq = []  # OBSD FREQ package


class NavObsPlusT:
    def __init__(self):
        self.prn = 0
        self.glo_sat = 0  # GLONASS SATID (+FW_PRN_GLO_MIN-1), decoded from GLO-NAV
        self.fbm_sel = 0  # Selected freq. bit mask
        self.fbm_cp_val = [0] * 2  # Carrier phase valid bit mask, [0]:current EP, [1]:previous EP
        self.obsi_b = 0  # Common OBSD's OBSI of BASE
        # For Rover OBS Database
        self.obsp_frq = []  # OBSP FREQ package


class NavSatDataT:
    def __init__(self):
        self.prn = 0
        self.stat = 0  # NE_SAT_STAT_XXX
        self.fbm = 0  # Freq. bit mask
        self.glo_frq = 0  # GLONASS frequency slot number
        self.azi = 0  # Azimuth angle in rad
        self.ele = 0  # Elevation angle in rad
        self.trop_delay = 0
        self.trop_var = 0
        self.iono_delay = 0  # Ionosphere Delay, Based On L1 Freq
        self.iono_var = 0  # Ionosphere Delay Variance, Based On L1 Freq
        # For Rover OBS Database
        self.satd_frq = []  # SATD FREQ package
        # For Base OBS Database
        self.satb_frq = []  # SATD FREQ package


class ObsDataFreqT:
    def __init__(self):
        self.prn = 0  # PRN number, used for cross-check
        self.sig = 0  # Signal type, ((fid<<4)|(sys))
        self.lli = 0  # Loss of lock indicator, 0: valid, 1: cycle-slip, 2: half cycle uncertainty
        self.lock = 0  # Lock Time indicater:
        # For DF402, refer to RTCM v3 Table 3.5-74.
        # 0: 0 < lock time < 32ms
        # 1: 32ms < lock time < 64ms
        # ...
        # 15: lock time > 524288ms
        # For DF407, refer to RTCM v3 Table 3.5-76
        # lock = df407 >> 2
        self.cnr = 0  # Carrier to noise ratio (0.01 dBxHz)
        self.dp = 0  # Observation data doppler frequency (Hz)
        self.cp = 0  # Observation data carrier-phase (cycle)
        self.pr = 0  # Observation data pseudorange (m)
        self.t_tx = UTime()  # Transmit time

    def update(self, obsd_frq):
        self.prn = obsd_frq.prn
        self.sig = obsd_frq.sig
        self.lli = obsd_frq.lli
        self.lock = obsd_frq.lock
        self.cnr = obsd_frq.cnr
        self.dp = obsd_frq.dp
        self.cp = obsd_frq.cp
        self.pr = obsd_frq.pr
        self.t_tx.update(obsd_frq.t_tx)


class NavObsT:
    def __init__(self):
        self.rcv_type = 0
        self.t = UTime()  # Receiver sampling time (GPST) of current  epoch
        self.t_prev = UTime()  # Receiver sampling time (GPST) of previous epoch
        self.obsd = []
        self.obsp = []
        self.satd = []
        self.obsn = 0  # OBSD number
        self.nsys = [0] * SYS_MAX  # OBSD number per SYS
        self.nmax = 0  # Max OBSD number
        self.ndel = 0  # OBSD number to be deleted
        # self.obsi = []                  # OBSD index
        self.nsatd = 0  # SATD number
        self.sbm_sys = [0] * SYS_MAX  # Sat Bit Mask per SYS, NO need -1
        self.sbm_glo_sat = 0  # Sat Bit Mask of GLO_SAT ID, NO need -1
        self.obsn_frq = 0  # OBSD freq data number
        self.nmax_frq = 0  # Max OBSD freq number


class NavData:
    def __init__(self):
        self.obsr = NavObsT()               # Local OBS of Rover
        self.obsb = NavObsT()               # Local OBS of Base
        self.obsr_parsed_raw_data = []      # Parsed RTCM raw data for OBSR by using Pyrtcm lib
        self.obsr_parsed_idx = 0            # Index of processing parsed RTCM raw data for OBSR
        self.flag_obsr_epoch_end = False    # End of an epoch when process OBSR data
        self.obsb_parsed_raw_data = []      # Parsed RTCM raw data for OBSB by using Pyrtcm lib
        self.obsb_parsed_idx = 0            # Index of processing parsed RTCM raw data for OBSB
        self.flag_obsb_epoch_end = False    # End of an epoch when process OBSB data
        self.flag_obsb_parse_pause = False  # Parsed Base obs epoch earlier than rover obs
        self.obsn_cmn = 0                   # Common OBSD number between Rover and Base
        self.nsys_cmn = [0] * SYS_MAX       # Common OBSD number for every SysID
        self.sbm_cmn = [0] * SYS_MAX        # Common Sat bit mask for every SysID
        self.base = Station()
        self.flag_base_switch = False


class NavInfo:
    def __init__(self):
        self.stat = 0
        self.stat_prev = 0
        self.ep_cnt = 0
        self.en_base = True
        self.time = UTime()
        self.time_prev = UTime()
        self.ct_gpst = CTime()
        self.ct_utct = CTime()


# ---------Time conversion----------
s_leaps = [                     # leap seconds (y,m,d,h,m,s,utc-gpst)
    [2017, 1, 1, 0, 0, 0, -18],
    [2015, 7, 1, 0, 0, 0, -17],
    [2012, 7, 1, 0, 0, 0, -16],
    [2009, 1, 1, 0, 0, 0, -15],
    [2006, 1, 1, 0, 0, 0, -14],
    [1999, 1, 1, 0, 0, 0, -13],
    [1997, 7, 1, 0, 0, 0, -12],
    [1996, 1, 1, 0, 0, 0, -11],
    [1994, 7, 1, 0, 0, 0, -10],
    [1993, 7, 1, 0, 0, 0, -9],
    [1992, 7, 1, 0, 0, 0, -8],
    [1991, 1, 1, 0, 0, 0, -7],
    [1990, 1, 1, 0, 0, 0, -6],
    [1988, 1, 1, 0, 0, 0, -5],
    [1985, 7, 1, 0, 0, 0, -4],
    [1983, 7, 1, 0, 0, 0, -3],
    [1982, 7, 1, 0, 0, 0, -2],
    [1981, 7, 1, 0, 0, 0, -1]]


class UTime:
    # Unified Time Format
    def __init__(self, week=0, msow=0.0):
        self.wn = week
        self.msow = msow

    def uniform_utime(self):
        while self.msow >= 604800000:
            self.msow -= 604800000
            self.wn += 1
        while self.msow < 0:
            self.msow += 604800000
            self.wn -= 1

    def __add__(self, other):
        self.wn += other.wn
        self.msow += other.msow
        self.uniform_utime()

    def __sub__(self, other):
        self.wn -= other.wn
        self.msow -= other.msow
        self.uniform_utime()

    def update(self, ut):
        self.wn = ut.wn
        self.msow = ut.msow


def calc_utime_diff_sec(t1, t2):
    dt = (t1.wn - t2.wn) * 604800
    dt += (t1.msow - t2.msow) * 0.001
    return dt


def calc_utime_add_sec(ut_in, sec):
    ut_out = UTime()
    ut_out.wn = ut_in.wn
    ut_out.msow = ut_in.msow + sec * 1000.0
    ut_out.uniform_utime()
    return ut_out


class CTime:
    # Calendar Time Format
    def __init__(self):
        self.year = 0  # Year, 1901-2099
        self.mon = 0  # Month since January, 1-12
        self.day = 0  # Day of the month, 1-31
        self.hour = 0  # Hours since midnight, 0-23
        self.min = 0  # minutes after the hour, 0-59
        self.sec = 0  # Seconds of the minute


def conv_ctime2utime(ct):
    """
    Convert system time from CTime format to UTime format.
    :param ct: system time in CTime format
    :return:
    """
    doy = [1, 32, 60, 91, 121, 152, 182, 213, 244, 274, 305, 335]
    ut = UTime()
    year = ct.year
    mon = ct.mon
    day = ct.day
    if year < 1970 or 2099 < year or mon < 1 or 12 < mon:
        return ut
    # leap year if year%4==0 in 1901-2099
    if (year % 4) == 0 and mon >= 3:
        leap_y = 1
    else:
        leap_y = 0
    days = (year - 1980) * 365 + (year - 1977) / 4 + doy[mon - 1] + day - 7 + leap_y
    ut.wn = int(days / 7)
    sec = int(math.floor(ct.sec))
    ut.msow = (ct.sec - sec) * 1000.0
    ut.msow += ((days % 7) * 86400 + ct.hour * 3600 + ct.min * 60 + sec) * 1000
    ut.uniform_utime()
    return ut


def conv_utime2ctime(ut):
    """
    Convert system time from UTime format to CTime format.
    :param ut: system time in UTime format
    :return:
    """
    days_in_month = [31, 29, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31,  # 1st Year (1980) is leap year!!
                     31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31,
                     31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31,
                     31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
    ct = CTime()
    sow = int(ut.msow / 1000)
    time = ut.wn * 604800 + sow
    days = int(time / 86400)
    sec = time - days * 86400
    # Calculate month in four years and day in month
    # Add five days to convert first day of UTIME from 1980.1.6 to 1980.1.1
    day = (days + 5) % 1461  # Days of four years
    for mon in range(48):  # Months of four years
        mday = days_in_month[mon]
        if day >= mday:
            day -= mday
        else:
            break
    ct.year = 1980 + int((days + 5) / 1461) * 4 + int(mon / 12)
    ct.mon = mon % 12 + 1
    ct.day = day + 1
    ct.hour = int(sec / 3600)
    ct.min = int((sec % 3600) / 60)
    ct.sec = sec % 60 + ut.msow / 1000.0 - sow
    return ct


def conv_ut_gpst2utct(gpst):
    """
    Convert from GPST to UTCT in UTime format.
    :param gpst: GPST in UTime format
    :return:
    """
    i = 0
    while i < len(s_leaps) and s_leaps[i][0] > 0:
        utct = calc_utime_add_sec(gpst, s_leaps[i][6])
        ct = CTime()
        ct.year = s_leaps[i][0]
        ct.mon = s_leaps[i][1]
        ct.day = s_leaps[i][2]
        ut = conv_ctime2utime(ct)
        if calc_utime_diff_sec(utct, ut) >= 0.0:
            return utct
        i += 1
    return gpst


def resolve_full_gps_wn(wn, sow, flag_base):
    """
    Resolve GPS week number roll-over issue.
    :param wn: decoded 10-bit week
    :param sow: decoded second of week referring to wn
    :param flag_base: flag of base or rover data
    :return:
    """
    if flag_base is False:
        t = navd.obsr.t
    else:
        t = navd.obsb.t
    rollover = 0
    if t.wn > 0:
        obs_sec = t.msow / 1000
        rollover = int(t.wn / 1024)
        if obs_sec > 453600 and sow < 151200:
            # Week mismatch: OBST in previous week
            rollover += 1
        elif obs_sec < 151200 and sow > 453600:
            # Week mismatch: input time in previous week
            rollover -= 1
    return wn + rollover * 1024


# --------------Utility Function---------------
def conv_sig_to_sys(sig):
    return sig & 0x0F


def conv_sig_to_fid(sig):
    return sig >> 4


s_wavel_lut = [[WAVEL_L1, WAVEL_L5, WAVEL_NONE, WAVEL_L2, WAVEL_NONE],  # GPS
               [WAVEL_B1, WAVEL_L5, WAVEL_E5B, WAVEL_B3, WAVEL_L1],  # BDS
               [WAVEL_G1, WAVEL_NONE, WAVEL_NONE, WAVEL_G2, WAVEL_NONE],  # GLO
               [WAVEL_L1, WAVEL_L5, WAVEL_E5B, WAVEL_E6, WAVEL_NONE],  # GAL
               [WAVEL_NONE, WAVEL_L5, WAVEL_NONE, WAVEL_NONE, WAVEL_NONE],  # IRS
               [WAVEL_L1, WAVEL_L5, WAVEL_NONE, WAVEL_L2, WAVEL_NONE],  # QZS
               [WAVEL_L1, WAVEL_NONE, WAVEL_NONE, WAVEL_NONE, WAVEL_NONE]  # SBS
               ]
s_rfreq_lut = [[RFREQ_L1, RFREQ_L5, RFREQ_NONE, RFREQ_L2, RFREQ_NONE],  # GPS
               [RFREQ_B1, RFREQ_L5, RFREQ_E5B, RFREQ_B3, RFREQ_L1],  # BDS
               [RFREQ_G1, RFREQ_NONE, RFREQ_NONE, RFREQ_G2, RFREQ_NONE],  # GLO
               [RFREQ_L1, RFREQ_L5, RFREQ_E5B, RFREQ_E6, RFREQ_NONE],  # GAL
               [RFREQ_NONE, RFREQ_L5, RFREQ_NONE, RFREQ_NONE, RFREQ_NONE],  # IRS
               [RFREQ_L1, RFREQ_L5, RFREQ_NONE, RFREQ_L2, RFREQ_NONE],  # QZS
               [RFREQ_L1, RFREQ_NONE, RFREQ_NONE, RFREQ_NONE, RFREQ_NONE]  # SBS
               ]


def get_wave_len_by_sig(sig):
    sys = conv_sig_to_sys(sig)
    f = conv_sig_to_fid(sig)
    if sys < SYS_MAX and f < FREQ_MAX_ID:
        wave_len = s_wavel_lut[sys][f]
    else:
        wave_len = WAVEL_L1
    return wave_len


def get_radio_frq_glo_by_sig(sig, frq):
    sys = conv_sig_to_sys(sig)
    f = conv_sig_to_fid(sig)
    if sys < SYS_MAX and f < FREQ_MAX_ID:
        rf = s_rfreq_lut[sys][f]
    else:
        rf = RFREQ_G1
    if f == 0:
        df = DFREQ_G1
    else:
        df = DFREQ_G2
    return rf + frq * df


def get_wave_len_glo_by_sig(sig, frq):
    return CLIGHT / get_radio_frq_glo_by_sig(sig, frq)


def check_prn(prn):
    if prn != 0:
        flag = True
    else:
        flag = False
    return flag


def is_gps_prn(prn):
    if MIN_GPS_SAT_PRN <= prn <= MAX_GPS_SAT_PRN:
        return True
    else:
        return False


def is_bds_prn(prn):
    if MIN_BDS_SAT_PRN <= prn <= MAX_BDS_SAT_PRN:
        return True
    else:
        return False


def is_glo_prn(prn):
    if MIN_GLO_SAT_PRN <= prn <= MAX_GLO_SAT_PRN:
        return True
    else:
        return False


def is_gal_prn(prn):
    if MIN_GAL_SAT_PRN <= prn <= MAX_GAL_SAT_PRN:
        return True
    else:
        return False


def is_qzs_prn(prn):
    if MIN_QZS_SAT_PRN <= prn <= MAX_QZS_SAT_PRN:
        return True
    else:
        return False


def is_sbs_prn(prn):
    if MIN_SBS_SAT_PRN <= prn <= MAX_SBS_SAT_PRN:
        return True
    else:
        return False


def is_irs_prn(prn):
    if MIN_IRS_SAT_PRN <= prn <= MAX_IRS_SAT_PRN:
        return True
    else:
        return False


def convert_prn_to_sid_sys(prn):
    sid = 0
    sys = SYS_INVALID
    if prn != 0:
        if is_gps_prn(prn):
            sid = prn - MIN_GPS_SAT_PRN
            sys = GPS
        elif is_bds_prn(prn):
            sid = prn - MIN_BDS_SAT_PRN
            sys = BDS
        elif is_glo_prn(prn):
            sid = prn - MIN_GLO_SAT_PRN
            sys = GLO
        elif is_gal_prn(prn):
            sid = prn - MIN_GAL_SAT_PRN
            sys = GAL
        elif is_qzs_prn(prn):
            sid = prn - MIN_QZS_SAT_PRN
            sys = QZS
        elif is_sbs_prn(prn):
            sid = prn - MIN_SBS_SAT_PRN
            sys = SBS
        elif is_irs_prn(prn):
            sid = prn - MIN_IRS_SAT_PRN
            sys = IRS
    return sid, sys
