"""
NAV Core, routine of navigation engine.
"""
import nav_common as nc
import nav_obs as no
from ioc_trace import logger
import ioc_rtcm as iocr
import sdc_constellation as sc


def ne_prepare_epoch():
    """
    Prepare epoch data for NE fix, including OBSR preprocess, Sat data update and OBSB handling.
    :return:
    """
    navi = nc.navi
    navd = nc.navd
    navc = nc.navc
    if (navi.stat & nc.NE_STAT_INIT) == 0:
        logger.error('NE Prepare Epoch, NOT initialized!!!')
        return False
    navi.stat_prev = navi.stat
    navi.stat &= nc.NE_STAT_INIT
    navi.ep_cnt += 1
    # Load epoch data for OBSR
    iocr.setup_msm_meas(False)
    # Sanity check OBSR database
    if no.update_local_obs(False) is False:
        return True
    # Update NE status
    navi.stat |= nc.NE_STAT_RCV1_OBSLO_UPDATED
    # Update NE receiver time
    navi.time_prev = navi.time
    obsr = navd.obsr
    if navi.stat & nc.NE_STAT_RCV1_OBSLO_UPDATED > 0:
        navi.time = obsr.t
        navi.ct_gpst = nc.conv_utime2ctime(navi.time)
        utct = nc.conv_ut_gpst2utct(navi.time)
        utct.uniform_utime()
        navi.ct_utct = nc.conv_utime2ctime(utct)
    else:
        logger.warning('NE prepare epoch failed: OBSR not initialized!')
        return True
    # Load epoch data for OBSB
    if navc.flag_base_val is True:
        iocr.setup_msm_meas(True)
        # Sanity check OBSB database
        no.update_local_obs(True)
    # Calculate Satellite PVA
    sc.calc_sats_pos_vel_clk(obsr, False)
    if navi.en_base is True:
        # Select common obs btw Rover and Base
        3
        # Calculate Satellite PVA for Base
        4
    # OBSD quality control
    5
    return True
