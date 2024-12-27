"""
IOController RTCM settings
"""
from pyrtcm import RTCMReader
from ioc_trace import logger
import nav_common as nc
import nav_obs as no
import sdc_constellation as sc
import copy


# Signal ID Mapping according to RTCM3.3 Table 3.5-91 ~ Table 3.5-108
c_rtcm_gps_sig_map = {'1C': nc.GPS_L1, '1P': nc.GPS_L1, '1W': nc.GPS_L1,
                        '2C': nc.GPS_L2C, '2P': nc.GPS_L2C, '2W': nc.GPS_L2C,
                        '2S': nc.GPS_L2C, '2L': nc.GPS_L2C, '2X': nc.GPS_L2C,
                        '5I': nc.GPS_L5, '5Q': nc.GPS_L5, '5X': nc.GPS_L5,
                        '1S': 0xFF, '1L': 0xFF, '1X': 0xFF  # TBD: L1C
                      }
c_rtcm_glo_sig_map = {'1C': nc.GLO_G1, '1P': nc.GLO_G1, '2C': nc.GLO_G2, '2P': nc.GLO_G2}
c_rtcm_gal_sig_map = {'1C': nc.GAL_E1, '1A': nc.GAL_E1, '1B': nc.GAL_E1, '1X': nc.GAL_E1, '1Z': nc.GAL_E1,
                        '6C': nc.GAL_E6, '6A': nc.GAL_E6, '6B': nc.GAL_E6, '6X': nc.GAL_E6, '6Z': nc.GAL_E6,
                        '7I': nc.GAL_E5B, '7Q': nc.GAL_E5B, '7X': nc.GAL_E5B,
                        '8I': 0xFF, '8Q': 0xFF, '8X': 0xFF,  # TBD: E5(A+B)
                        '5I': nc.GAL_E5A, '5Q': nc.GAL_E5A, '5X': nc.GAL_E5A
                      }
c_rtcm_sbs_sig_map = {'1C': nc.SBS_L1, '5I': nc.SBS_L5, '5Q': nc.SBS_L5, '5X': nc.SBS_L5}
c_rtcm_qzs_sig_map = {'1C': nc.QZS_L1,
                        '6S': 0xFF, '6L': 0xFF, '6X': 0xFF,  # TBD: LEX, L-band Experimental signal
                        '2S': nc.QZS_L2C, '2L': nc.QZS_L2C, '2X': nc.QZS_L2C,
                        '5I': nc.QZS_L5, '5Q': nc.QZS_L5, '5X': nc.QZS_L5,
                        '1S': 0xFF, '1L': 0xFF, '1X': 0xFF  # TBD: L1C
                      }
c_rtcm_bds_sig_map = {'2I': nc.BDS_B1, '2Q': nc.BDS_B1, '2X': nc.BDS_B1,
                        '6I': nc.BDS_B3, '6Q': nc.BDS_B3, '6X': nc.BDS_B3,
                        '7I': nc.BDS_B2, '7Q': nc.BDS_B2, '7X': nc.BDS_B2,
                        '5I': nc.BDS_B2A, '5Q': nc.BDS_B2A, '5X': nc.BDS_B2A,  # Not list in RTCM3.3
                        '1I': nc.BDS_B1C, '1Q': nc.BDS_B1C, '1X': nc.BDS_B1C   # Not list in RTCM3.3
                      }


def conv_rtcm_sat_to_prn(sys, sat):
    """
    Convert RTCM MSM sat id to local PRN.
    :param sys: system id
    :param sat: msm sat id
    :return:
    """
    prn = 0
    if sys == nc.GPS:
        prn = int(sat) + nc.MIN_GPS_SAT_PRN - 1
    # TBD: other sys
    else:
        logger.debug('Convert rtcm sat to prn, unexpected sys {}, sat {}'.format(sys, sat))
    return prn


def conv_rtcm_sig_to_nav_sig(sys, code):
    """
    Convert RTCM MSM signal id to local Sig.
    :param sys: system id
    :param code: msm sig id
    :return:
    """
    if sys == nc.GPS:
        sig = c_rtcm_gps_sig_map.get(code)
    elif sys == nc.BDS:
        sig = c_rtcm_bds_sig_map.get(code)
    elif sys == nc.GLO:
        sig = c_rtcm_glo_sig_map.get(code)
    elif sys == nc.GAL:
        sig = c_rtcm_gal_sig_map.get(code)
    elif sys == nc.QZS:
        sig = c_rtcm_qzs_sig_map.get(code)
    elif sys == nc.SBS:
        sig = c_rtcm_sbs_sig_map.get(code)
    else:
        logger.debug('Convert rtcm sig to nav sig, unexpected sys {}, sig {}'.format(sys, code))
        sig = 0xFF
    if sig is None:
        logger.warning('Convert rtcm sig to nav sig, unexpected sys {}, sig {}'.format(sys, code))
        sig = 0xFF
    return sig


def process_sarp_msg(parsed_data, msg_id, flag_base):
    """
    Decode message of Stationary Antenna Reference Point w/ or w/o height information.
    :param parsed_data: parsed msm data
    :param msg_id: rtcm message id
    :param flag_base: flag of base or rover data
    :return:
    """
    flag_has_height = True if msg_id == '1006' else False
    if flag_has_height is True and len(parsed_data.payload) != 21:
        logger.debug('SARP {} decode, unexpected length {}'.format(msg_id, len(parsed_data.payload)))
        return
    if flag_has_height is False and len(parsed_data.payload) != 19:
        logger.debug('SARP {} decode, unexpected length {}'.format(msg_id, len(parsed_data.payload)))
        return
    station = nc.Station()
    station.id = parsed_data.DF003
    station.itrf_year = parsed_data.DF021
    station.gps_indi = parsed_data.DF022
    station.glo_indi = parsed_data.DF023
    station.gal_indi = parsed_data.DF024
    station.ref_indi = parsed_data.DF141  # Reference-Station Indicator, set 1 if virtual
    station.sro_indi = parsed_data.DF142  # Single Receiver Oscillator Indicator, set 1 if raw obs 1001-1004,
                                               # 1009-1012 at the same time
    station.qcy_indi = parsed_data.DF364  # Quarter Cycle Indicator, 00 Unspecified, 01 No quarter cycle in
                                               # phase, 10 May have quarter cycle in phase
    station.xyz[0] = parsed_data.DF025
    station.xyz[1] = parsed_data.DF026
    station.xyz[2] = parsed_data.DF027
    if flag_has_height is True:
        station.height = parsed_data.DF028
    # Determine base station type
    if station.ref_indi == 1:
        station.type = nc.NE_STA_TYPE_BASE_VRS
    else:
        station.type = nc.NE_STA_TYPE_BASE_FIX
    if flag_base is True:
        nc.set_base_station(station)
    # TBD: else set rover init position


def process_gps_eph_msg(parsed_data, flag_base):
    len_payload = len(parsed_data.payload)
    if len_payload != 61:
        logger.warning('Process GPS Eph Msg, unexpected payload length {}, Base {}'.format(len_payload, flag_base))
        return
    prn = parsed_data.DF009 + nc.MIN_GPS_SAT_PRN - 1
    if nc.check_prn(prn) is False or nc.is_gps_prn(prn) is False:
        logger.warning('Process GPS Eph Msg, invalid prn {}, Base {}'.format(prn, flag_base))
        return
    eph = sc.GpsEphT()
    eph.prn = prn
    toe = parsed_data.DF093
    wn = nc.resolve_full_gps_wn(parsed_data.DF076, toe, flag_base)
    # Ephemeris reference information
    eph.toe.wn = wn
    eph.toe.msow = toe * 1000
    eph.iode = parsed_data.DF071
    # Sanity check the CEI dataset
    eph.iodc = parsed_data.DF085
    toc = parsed_data.DF081
    if abs(toe - toc) > 1 or eph.iode != (eph.iodc & 0xFF):
        logger.warning('Process GPS Eph Msg, mismatch CEI, toe {}, toc {}'.format(toe, toc))
        return
    # Clock reference information
    eph.toc.wn = wn
    eph.toc.msow = toc * 1000
    # Check whether need update CEI data
    eph.fit = parsed_data.DF137
    fit_intv = 7200         # curve-fit interval is 4 hours
    if eph.fit == 1:
        fit_intv = 10800    # curve-fit is greater than 4 hours, >= 6 hours
    obsr = nc.navd.obsr
    if obsr.t.wn > 0:
        if abs(nc.calc_utime_diff_sec(obsr.t, eph.toe)) > fit_intv:
            logger.warning('Process GPS Eph Msg, outdated eph, toe {},{}, obs {},{}'.format(eph.toe.wn, eph.toe.msow,
                                                                                    obsr.t.wn, obsr.t.msow))
            return
    # Check existing eph data
    satm_ip1 = sc.get_sat_msg(prn, True)
    if satm_ip1 == 0:
        logger.error('Process GPS Eph Msg, allocate satMsg failed!')
        return
    satm_idx = satm_ip1 - 1
    cd = sc.cd
    satm = cd.satm_gps[satm_idx]
    # Update new msg_gps
    if len(sc.cd.msg_gps) < len(cd.satm_gps):
        cd.msg_gps.append(eph)
        msg_gps = cd.msg_gps[satm_idx]
    else:
        msg_gps = cd.msg_gps[satm_idx]
        if (satm.stat & sc.SDC_SATM_STAT_EPH_VALID) > 0:
            if msg_gps.toe.wn > 0:
                dt = nc.calc_utime_diff_sec(eph.toe, msg_gps.toe)
                if dt <= 1.0:
                    logger.debug('Process GPS Eph Msg, toe dt {} too old to update'.format(dt))
                    return
    eph.sva = parsed_data.DF077
    eph.code2 = parsed_data.DF078
    eph.idot = parsed_data.DF079
    eph.af[2] = parsed_data.DF082
    eph.af[1] = parsed_data.DF083
    eph.af[0] = parsed_data.DF084
    eph.crs = parsed_data.DF086
    eph.delta_n = parsed_data.DF087
    eph.m0 = parsed_data.DF088
    eph.cuc = parsed_data.DF089
    eph.ecc = parsed_data.DF090
    eph.cus = parsed_data.DF091
    eph.sqrt_a = parsed_data.DF092
    eph.cic = parsed_data.DF094
    eph.omega0 = parsed_data.DF095
    eph.cis = parsed_data.DF096
    eph.i0 = parsed_data.DF097
    eph.crc = parsed_data.DF098
    eph.omg = parsed_data.DF099
    eph.omg_dot = parsed_data.DF100
    eph.tgd = parsed_data.DF101
    eph.health = parsed_data.DF102
    eph.p_data2 = parsed_data.DF103
    msg_gps = copy.deepcopy(eph)
    sid, sys = nc.convert_prn_to_sid_sys(prn)
    cd.eph_val_gps |= (0x1 << (sid - 1))
    logger.debug('Process GPS Eph Msg, update Prn {}, toe {}, bitmask {}'.format(prn, toe, hex(cd.eph_val_gps)))
    return


def setup_msm_meas(flag_base):
    """
    Process RTCM measurement/ephemeris/station data according to message id.
    :param flag_base: flag of base or rover data
    :return:
    """
    navd = nc.navd
    if flag_base is False:
        len_parse = len(navd.obsr_parsed_raw_data)
        parsed_idx = navd.obsr_parsed_idx
        flag_epoch_end = nc.navd.flag_obsr_epoch_end
    else:
        len_parse = len(navd.obsb_parsed_raw_data)
        parsed_idx = navd.obsb_parsed_idx
        flag_epoch_end = nc.navd.flag_obsb_epoch_end
    for idx in range(parsed_idx, len_parse, 1):
        parsed_data = navd.obsr_parsed_raw_data[idx]
        msg_id = parsed_data.identity
        if msg_id == '1005' or msg_id == '1006':
            # Stationary Antenna Reference Point w/ or w/o height information.
            process_sarp_msg(parsed_data, msg_id, flag_base)
        elif msg_id == '1074' or msg_id == '1084' or msg_id == '1094' or msg_id == '1104' or msg_id == '1114'\
                or msg_id == '1124':
            # MSM4 measurement
            process_msm4_msg(parsed_data, msg_id, flag_base)
        elif msg_id == '1077' or msg_id == '1087' or msg_id == '1097' or msg_id == '1107' or msg_id == '1117'\
                or msg_id == '1127':
            # MSM7 measurement
            process_msm7_msg(parsed_data, msg_id, flag_base)
        elif msg_id == '1019':
            # GPS Ephemeris
            process_gps_eph_msg(parsed_data, flag_base)
        else:
            logger.debug('RTCM Rover Meas, unknown MSG_ID {}'.format(msg_id))
        # DEBUG CODE
        if flag_base is False and msg_id == '1077':
            flag_epoch_end = True
        # DEBUG CODE END
        # Detect epoch end and finish reading
        if flag_epoch_end is True:
            parsed_idx = idx
            flag_epoch_end = False
            break
        if flag_base is True and navd.flag_obsb_parse_pause is True:
            parsed_idx = idx
            navd.flag_obsb_parse_pause = False
            break
    return


def process_msm7_msg(parsed_data, msg_id, flag_base):
    """
    Decode message of MSM7.
    :param parsed_data: parsed msm data
    :param msg_id: rtcm message id
    :param flag_base: flag of base or rover data
    :return:
    """
    len_payload = len(parsed_data.payload)
    if len_payload > 742:
        logger.debug('MSM7 {} decode, unexpected length {}'.format(msg_id, len_payload))
        return
    sys = nc.SYS_INVALID
    if msg_id == '1077':
        sys = nc.GPS
    elif msg_id == '1087':
        sys = nc.GLO
    elif msg_id == '1097':
        sys = nc.GAL
    elif msg_id == '1107':
        sys = nc.SBS
    elif msg_id == '1117':
        sys = nc.QZS
    elif msg_id == '1127':
        sys = nc.BDS
    else:
        logger.debug('MSM7 {} decode, unexpected sys'.format(msg_id))
        return
    head = MsmHeader()
    if process_msm_header(parsed_data, head, sys) == 0:
        return
    if flag_base is True:
        if no.update_base_rtcm_time(head.ep_time) is False:
            return
    else:
        if no.update_rover_rtcm_time(head.ep_time) is False:
            return
    # TBD: Handle base switch issue

    cell_idx = 0
    for sat in range(parsed_data.NSat):
        sat_vals = []
        for attr in ("PRN", "DF397", "DF398", "DF399", "ExtSatInfo"):
            sat_val = getattr(parsed_data, f"{attr}_{sat + 1:02d}")
            sat_vals.append(sat_val)
        for cell in range(cell_idx, parsed_data.NCell):
            cell_vals = []
            obsd_frq = nc.ObsDataFreqT()
            for attr1 in ("CELLPRN", "CELLSIG", "DF405", "DF406", "DF407", "DF408", "DF420", "DF404"):
                cell_val = getattr(parsed_data, f"{attr1}_{cell + 1:02d}")
                cell_vals.append(cell_val)
            if cell_vals[0] != sat_vals[0]:
                cell_idx = cell  # Update cell_idx to loop faster
                break
            obsd_frq.prn = conv_rtcm_sat_to_prn(sys, cell_vals[0])
            if obsd_frq.prn == 0:
                continue
            obsd_frq.sig = conv_rtcm_sig_to_nav_sig(sys, cell_vals[1])
            if obsd_frq.sig == 0xFF:
                continue
            if sys != nc.GLO:
                wave_len = nc.get_wave_len_by_sig(obsd_frq.sig)
            else:
                if sat_vals[4] >= 14:
                    logger.debug('Process MSM7 GLO, unexpected frequency number {}'.format(sat_vals[4]))
                    continue
                freq_number = sat_vals[4] - 7
                wave_len = nc.get_wave_len_glo_by_sig(obsd_frq.sig, freq_number)
            if wave_len <= 0:
                logger.debug('Process MSM7, unexpected waveLen {}, sys {}, prn {}, sig {}'.format(wave_len, sys,
                                                                                obsd_frq.prn, obsd_frq.sig))
                continue
            rr = sat_vals[1] + sat_vals[2]
            dt = cell_vals[2] + rr  # dt in ms
            obsd_frq.t_tx = nc.calc_utime_add_sec(head.ep_time, -dt * 0.001)
            obsd_frq.pr = dt * nc.CLIGHT_MS
            obsd_frq.cp = cell_vals[3] + rr
            obsd_frq.cp *= (nc.CLIGHT_MS / wave_len)
            obsd_frq.lock = cell_vals[4]
            obsd_frq.cnr = cell_vals[5]
            if cell_vals[6] == 1:
                obsd_frq.lli |= nc.NE_LLI_HALFC
            obsd_frq.dp = -(cell_vals[7] + sat_vals[3])
            obsd_frq.dp /= wave_len
            no.update_rtcm_obsd(obsd_frq, flag_base)
            logger.debug(obsd_frq.__dict__)
    if head.mmb == 0:
        if flag_base is False:
            nc.navd.flag_obsr_epoch_end = True
        else:
            nc.navd.flag_obsb_epoch_end = True
    return


def process_msm4_msg(parsed_data, msg_id, flag_base):
    """
    Decode message of MSM4.
    :param parsed_data: parsed msm data
    :param msg_id: rtcm message id
    :param flag_base: flag of base or rover data
    :return:
    """
    len_payload = len(parsed_data.payload)
    if len_payload > 450:
        logger.debug('MSM4 {} decode, unexpected length {}'.format(msg_id, len_payload))
        return

    return


def process_msm_header(msg, head, sys):
    """
    Process Header data of MSM message.
    :param msg: parsed msm data
    :param head: decoded msm header data
    :param sys: system id
    :return:
    """
    head.ref_sta_id = msg.DF003
    ut = nc.UTime()
    if sys == nc.GPS:
        ut.msow = msg.DF004
        ut.wn = nc.navc.rtcm_wn
    else:
        return 0  # TBD
    head.ep_time = ut
    head.mmb = msg.DF393
    head.iods = msg.DF409
    head.clk_str_flag = msg.DF411
    head.clk_ext_flag = msg.DF412
    head.smooth_flag = msg.DF417
    head.interval = msg.DF418
    # df394 = msg.DF394
    # for i in range(0, 64):
    #     if (1 << (63 - i)) & df394 > 0:
    #         head.nsat += 1
    #         head.sats.append(i + 1)
    # df395 = msg.DF395
    # for i in range(0, 32):
    #     if (1 << (31 - i)) & df395 > 0:
    #         head.nsig += 1
    #         head.sigs.append(i + 1)
    head.nsat = msg.NSat
    head.nsig = msg.NSig
    ncell = head.nsat * head.nsig
    if ncell > 64:
        logger.debug('RTCM header decode, unexpected ncell {}'.format(ncell))
        return 0
    # df396 = msg.DF396
    # vncell = 0
    # for i in range(0, ncell):
    #     if (1 << (ncell - 1 - i)) & df396 > 0:
    #         vncell += 1
    #         head.cells.append(i + 1)
    return msg.NCell


class MsmHeader:
    def __init__(self):
        self.mmb = 0                # Multiple Message Bit, 1 means more msm follows, 0 means the last msm
        self.iods = 0               # Issue Of Data Station
        self.clk_str_flag = 0       # Clock steering Indicator
        self.clk_ext_flag = 0       # External Clock Indicator
        self.smooth_flag = 0        # GNSS Divergence-free Smoothing Indicator
        self.interval = 0           # GNSS Smoothing Interval
        self.nsat = 0               # Number of GNSS Satellite
        self.nsig = 0               # Number of GNSS Signal
        self.ref_sta_id = 0         # Reference Station ID
        self.ep_time = nc.UTime()   # Epoch time


class RTCMInfo:
    def __init__(self):
        self.en_sys_bm = 0                  # TBD: not support RTCM output
        self.fp_meas_rtcm = None
        self.fp_base_rtcm = None

    def read_rtcm_file(self, flag_base):
        """
        Read and parse RTCM file.
        :param flag_base: flag of base or rover data
        :return:
        """
        file = self.fp_meas_rtcm if flag_base is False else self.fp_base_rtcm
        try:
            with open(file, 'rb') as stream:
                rtr = RTCMReader(stream)
                for raw_data, parsed_data in rtr:
                    if str(parsed_data.identity) != str(parsed_data.DF002):
                        logger.debug('Parse RTCM file unexpected identity {}, {}'.format(parsed_data.identity,
                                                                                         parsed_data.DF002))
                        continue
                    if flag_base is False:
                        nc.navd.obsr_parsed_raw_data.append(parsed_data)
                        # DEBUG CODE
                        if len(nc.navd.obsr_parsed_raw_data) > 1000:
                            break
                        # DEBUG CODE END
                    else:
                        nc.navd.obsb_parsed_raw_data.append(parsed_data)
                        # DEBUG CODE
                        if len(nc.navd.obsb_parsed_raw_data) > 1000:
                            break
                        # DEBUG CODE END
                # TEST: print raw and parsed data in rtr
                # for raw_data, parsed_data in rtr:
                #     print(parsed_data)
        except Exception as e:
            logger.error('Read RTCM File Failed! E={}, Flag_base={}'.format(e, flag_base))
            return False
        return True
