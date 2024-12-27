import ioc_trace as trace
from ioc_trace import logger
import ioc_nmea as iocn
import ioc_rtcm as iocr
import ioc_json as iocj
import nav_common as nc
import nav_core as ncr
import sdc_constellation as sdcc


def ne_offline_init():
    """
    ne_offline_init: initialize offline file input and user settings.
    :return:
    """
    json_path = '..\\..\\tests\\NE_Config.json'
    json_cfg = iocj.JsonCfg(json_path)
    if json_cfg.read_config() is False:
        logger.error('NE Offline Read Config Failed！')
        return False
    nc.copy_json_cfg(json_cfg)
    rtcm_info = iocr.RTCMInfo()
    rtcm_info.fp_meas_rtcm = json_cfg.fp_meas_rtcm
    if rtcm_info.read_rtcm_file(False) is False:
        return False
    if json_cfg.flag_base_val is True:
        rtcm_info.fp_base_rtcm = json_cfg.fp_base_rtcm
        if rtcm_info.read_rtcm_file(True) is False:
            return False

    # TBD: read Ground Truth file

    return True


def core_init():
    """
    core_init: initialize all the global memory and setup configures.
    :return:
    """
    sdcc.global_init()
    nc.global_init()
    trace.trace_init()
    nmea_info = iocn.NMEAInfo()
    if ne_offline_init() is False:
        return False
    # ne_cfg_init()
    return True


def ne_run_offline():
    """
    ne_run_offline: main entrance to run an offline playback of navigation engine.
    :return:
    """
    if core_init() is False:
        logger.error('Core initialization failed!')
        return
    while ncr.ne_prepare_epoch() is True:
        # if (False == ne_process_epoch()):
        #     break
        # if (False == ne_postprocess_epoch()):
        #     break
        1


if __name__ == "__main__":
    ne_run_offline()
