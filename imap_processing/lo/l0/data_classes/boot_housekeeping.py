from dataclasses import dataclass

from imap_processing.ccsds.ccsds_data import CcsdsData
from imap_processing.lo.l0.lol0 import LoL0
from imap_processing.lo.l0.utils.loApid import LoAPID


@dataclass
class BootHousekeeping(LoL0):
    SHCOARSE: int
    BOOT_VER: int
    BOOT_CNT: int
    BIST_STAT: int
    BIST_ABUS: int
    BIST_DBUS: int
    BIST_MEM_FF: int
    BIST_MEM_FL: int
    BIST_MEM_MAP: int
    BIST_MEM_CNT: int
    IMG_1_STAT: int
    IMG_2_STAT: int
    SPARE_0: int
    INSTR_ID: int
    SPARE_1: int
    FPGA_VER: int
    HV_LIM: int
    HV_DIS: int
    DOOR_DIS: int
    SPARE_2: int
    MDM25P_14_T: int
    MDM25P_15_T: int
    MDM25P_16_T: int
    LVPS_12V_T: int
    LVPS_5V_T: int
    LVPS_3P3V_T: int
    LVPS_3P3V: int
    LVPS_5V: int
    LVPS_N5V: int
    LVPS_12V: int
    LVPS_N12V: int
    LVPS_3P3V_I: int
    LVPS_5V_I: int
    LVPS_N5V_I: int
    LVPS_12V_I: int
    LVPS_N12V_I: int
    CDH_1P5V: int
    CDH_1P8V: int
    CDH_3P3V: int
    CDH_12V: int
    CDH_N12V: int
    CDH_5V: int
    CDH_5V_ADC: int
    CDH_PROCESSOR_T: int
    CDH_1P8V_LDO_T: int
    CDH_1P5V_LDO_T: int
    CDH_SDRAM_T: int
    OP_MODE: int
    CMD_ACC_CNT: int
    CMD_EXE_CNT: int
    CMD_REJ_CNT: int
    CMD_LAST_OPCODE: int
    CMD_RESULT: int
    ITF_ERR_CNT: int
    CHKSUM: int

    def __init__(self, packet, software_version: str, packet_file_name: str, apid: int):
        super().__init__(
            software_version,
            packet_file_name,
            CcsdsData(packet.header),
            LoAPID.ILO_BOOT_HK,
        )
        self.parse_data(packet)
