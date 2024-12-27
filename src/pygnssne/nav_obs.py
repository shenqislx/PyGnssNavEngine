"""
NAV Observation Controller. OBS database maintainer.
"""
import nav_common as nc
from ioc_trace import logger


def update_base_rtcm_time(t):
    """
    Update rtcm time for base OBS.
    :param t:
    :return:
    """
    if nc.navi.en_base is False:
        return False
    obsb = nc.navd.obsb
    if obsb.t.wn == 0 and obsb.t.msow == 0:
        obsb.t.update(t)
    else:
        dt = nc.calc_utime_diff_sec(t, obsb.t)
        if dt < -0.01:
            logger.debug('RTCM base time, unexpected dt {}'.format(dt))
            return False
        if dt > 0.01:
            obsb.t_prev.update(obsb.t)
            obsb.t.update(t)
    obsr = nc.navd.obsr
    dt = nc.calc_utime_diff_sec(obsr.t, obsb.t)
    if dt < 0:
        # Base obs in advance, stop reading and wait for rover obs update
        nc.navd.flag_obsb_parse_pause = True
        return False
    elif dt > 2.0:  # Exceed preset base delay, continue and read next epoch
        return False
    return True


def update_rover_rtcm_time(t):
    """
    Update rtcm time for rover OBS.
    :param t:
    :return:
    """
    obsr = nc.navd.obsr
    if obsr.t.wn == 0 and obsr.t.msow == 0:
        obsr.t.update(t)
    else:
        dt = nc.calc_utime_diff_sec(t, obsr.t)
        if dt < -0.01:
            logger.debug('RTCM rover time, unexpected dt {}'.format(dt))
            return False
        if dt > 0.01:
            obsr.t_prev.update(obsr.t)
            obsr.t.update(t)
    return True


def update_rtcm_obsd(obsd_frq, flag_base):
    """
    Update rtcm obsd for Rover/Base OBS database.
    :param obsd_frq: Input OBS_FRQ data
    :param flag_base: Base OBS or Rover OBS
    :return:
    """
    if flag_base is True:
        obsx = nc.navd.obsb
    else:
        obsx = nc.navd.obsr
    flag_insert = False
    obsi_idx = nc.NE_OBSI_INVALID
    if nc.check_prn(obsd_frq.prn) is False:
        return
    if nc.navi.en_base is False and flag_base is True:
        return
    # Check OBSR/OBSB corresponding sat
    sid, sys = nc.convert_prn_to_sid_sys(obsd_frq.prn)
    # if sys == nc.GLO and (obsx.sbm_glo_sat >> sid) & 0x1 == 0:
    #     return
    # if sys != nc.GLO and (obsx.sbm_sys[sys] >> sid) & 0x1 == 0:
    #     return
    if obsx.obsn == 0:
        obsi_idx = 0
        flag_insert = True
    else:
        for i in range(obsx.obsn):
            if obsx.obsd[i].prn == 0:
                logger.error('Updata RTCM Obs, unexpected obsi {}, flag_base {}'.format(i, flag_base))
                return
            if obsx.obsd[i].prn == obsd_frq.prn:
                obsi_idx = i
                break
            elif obsx.obsd[i].prn > obsd_frq.prn:
                obsi_idx = i
                flag_insert = True
                break
    if obsi_idx == nc.NE_OBSI_INVALID:
        if obsx.obsn >= obsx.nmax:
            logger.warning('Update RTCM Obs overflow, drop obs prn {} sig {}, flag_base {}'.format(obsd_frq.prn,
                                                                                            obsd_frq.sig, flag_base))
            return
        obsi_idx = obsx.obsn
        flag_insert = True
    if flag_insert is True and obsi_idx < obsx.nmax:
        if obsx.obsn >= obsx.nmax:
            logger.warning('Update Base Obs overflow, drop obs prn {} sig {}, flag_base {}'.format(obsd_frq.prn,
                                                                                            obsd_frq.sig, flag_base))
            return
    if flag_insert is True:
        # Save new OBSD
        obsd_temp = nc.NavObsDataT()
        obsd_temp.prn = obsd_frq.prn
        obsd_temp.sid = sid
        obsd_temp.sys = sys
        obsx.sbm_sys[sys] |= (1 << sid)
        obsx.obsd.insert(obsi_idx, obsd_temp)
        # Update OBSN
        obsx.obsn += 1
        obsx.nsys[sys] += 1
    # Set pointer to OBSD to update
    pobsd = obsx.obsd[obsi_idx]
    # Update OBSD_FRQ
    f = nc.conv_sig_to_fid(obsd_frq.sig)
    frqn = len(pobsd.obsd_frq)
    if pobsd.ip1_freq[f] == 0:
        # Add new OBSD_FRQ.
        if obsx.obsn_frq + 1 > obsx.nmax_frq:
            logger.warning('Update RTCM Obs, freq package overflow! Prn {}, f {}, frqn {}, nmax {}, flag_base {}'.format
                                                    (obsd_frq.prn, f, obsx.obsn_frq, obsx.nmax_frq, flag_base))
            return
        pobsd.ip1_freq[f] = frqn + 1
        pobsd.obsd_frq.append(obsd_frq)
        obsx.obsn_frq += 1
    else:
        frqi = pobsd.ip1_freq[f] - 1
        pobsd_frq = pobsd.obsd_frq[frqi]
        if (obsd_frq.lock == 0 and pobsd_frq.lock == 0) or (obsd_frq.lock < pobsd_frq.lock):
            obsd_frq.lli |= nc.NE_LLI_SLIP
        pobsd_frq.update(obsd_frq)
    pobsd.fbm |= (0x1 << f)
    return


def update_local_obs(flag_base):
    """
    Update local OBSR/OBSB database and delete the unmatched or stale observation.
    :return:
    """
    if flag_base is False:
        obsx = nc.navd.obsr
    else:
        obsx = nc.navd.obsb
    if obsx.obsn != len(obsx.obsd):
        logger.error('Update Local OBS, Unmatched OBSN {} and obsd length {} ! Base {}'.format(obsx.obsn,
                                                                                        len(obsx.obsd), flag_base))
        obsx.obsn = len(obsx.obsd)
    # Do NOT delete list element during iteration, or the indices would be messed up!
    del_list = []
    for obsi, obsd in enumerate(obsx.obsd):
        # Check invalid OBSD
        if nc.check_prn(obsd.prn) is False or obsd.fbm == 0:
            logger.error('Update Local OBS, unexpected OBSD! Prn {}, Fbm {}, Base {}'.format(obsd.prn, obsd.fbm,
                                                                                             flag_base))
            # Mark OBSD to delete
            obsd.prn = 0
            del_list.append(obsi)
    if len(del_list) > 0:
        # Iterate in reverse order to ensure the correctness of indices after deleting list elements
        for del_i in range(len(del_list) - 1, -1, -1):
            del obsx.obsd[del_list[del_i]]
        obsx.obsn = len(obsx.obsd)
    obsn_frq = 0
    for obsd in obsx.obsd:
        del_list.clear()
        for frqi, obsd_frq in enumerate(obsd.obsd_frq):
            if obsd_frq.prn != obsd.prn is False or obsd_frq.sig == 0xFF:
                logger.error('Update Local OBS, unexpected OBSD_FRQ! Prn {}, Sig {}, Base {}'.format(obsd_frq.prn,
                                                                                            obsd_frq.sig, flag_base))
                # Mark OBSD to delete
                obsd_frq.prn = 0
                del_list.append(frqi)
            elif nc.calc_utime_diff_sec(obsx.t, obsd_frq.t_tx) > 0.15:  # GEO orbit height 35786km, apprx. 120ms
                logger.debug('Update Local OBS, delete stale obs_frq Prn {}, Sig {}, Base {}'.format(obsd_frq.prn,
                                                                                            obsd_frq.sig, flag_base))
                # Mark OBSD to delete
                obsd_frq.prn = 0
                del_list.append(frqi)
            else:
                obsn_frq += 1
        if len(del_list) > 0:
            # Iterate in reverse order to ensure the correctness of indices after deleting list elements
            for del_i in range(len(del_list) - 1, -1, -1):
                del obsd.obsd_frq[del_list[del_i]]
    if obsn_frq != obsx.obsn_frq:
        logger.error('Update Local OBS, Unmatched OBSN_FRQ {} and obsd_frq length {} ! Base {}'.format(obsn_frq,
                                                                                            obsx.obsn_frq, flag_base))
        obsx.obsn_frq = obsn_frq
    if flag_base is False:
        if obsx.obsn_frq == 0 or obsx.obsn == 0:
            return False
    return True
