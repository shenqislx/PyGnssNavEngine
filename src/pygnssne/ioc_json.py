"""
IOController JSON loading module
"""
import json
from ioc_trace import logger
import nav_common as cfg
import nav_common as nc


class JsonCfg:
    def __init__(self, file):
        self.file_contents = None
        self.fp_meas_rtcm = None
        self.fp_navi_rinex = None
        self.fp_base_rtcm = None
        self.flag_base_val = False
        self.flag_rtcm_file = False
        self.rtcm_date = nc.CTime()
        self.sys_enable = cfg.SYSBM_DEFAULT
        self.dyna_mode = cfg.NE_RMODE_AUTO
        self.json_file = file

    def read_config(self):
        try:
            with open(self.json_file) as cfg_file:
                self.file_contents = cfg_file.read()
        except IOError as e:
            logger.error('JSON file invalid!')
            return False
        parsed_json = json.loads(self.file_contents)

        if isinstance(parsed_json["fmea_rtcm_path"], str):
            try:
                with open(parsed_json["fmea_rtcm_path"]) as meas_file:
                    self.fp_meas_rtcm = parsed_json["fmea_rtcm_path"]
                    self.flag_rtcm_file = True
            except IOError as e:
                logger.error('JSON file invalid fmea_rtcm_path.')
                return False
        if isinstance(parsed_json["fnavi_rinex_path"], str):
            try:
                with open(parsed_json["fnavi_rinex_path"]) as navi_file:
                    self.fp_navi_rinex = parsed_json["fnavi_rinex_path"]
            except IOError as e:
                logger.warning('JSON file invalid fnavi_rinex_path.')
                # return False
        if isinstance(parsed_json["fbase_rtcm_path"], str):
            try:
                with open(parsed_json["fbase_rtcm_path"]) as base_file:
                    self.fp_base_rtcm = parsed_json["fbase_rtcm_path"]
                    self.flag_base_val = True
                    self.flag_rtcm_file = True
            except IOError as e:
                logger.warning('JSON file invalid fbase_rtcm_path.')

        if self.flag_rtcm_file is True:
            if isinstance(parsed_json["rtcm_date"], str):
                date_str = parsed_json["rtcm_date"]
                self.rtcm_date.year = int(date_str[0:4])
                self.rtcm_date.mon = int(date_str[4:6])
                self.rtcm_date.day = int(date_str[6:8])

        # TBD: read Ground Truth file

        if isinstance(parsed_json["sys_enable"], str):
            self.sys_enable = parsed_json["sys_enable"]
        if isinstance(parsed_json["dyna_mode"], int):
            self.dyna_mode = parsed_json["dyna_mode"]
        if self.dyna_mode > cfg.NE_RMODE_MAX_MODE:
            self.dyna_mode = cfg.NE_RMODE_AUTO
        logger.debug('Decoded JSON config items list as:')
        logger.debug(json.dumps(parsed_json, sort_keys=False, indent=4))
        return True
