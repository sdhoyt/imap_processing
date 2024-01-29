from dataclasses import dataclass

from imap_processing.ccsds.ccsds_data import CcsdsData
from imap_processing.lo.l0.utils.loApid import LoAPID
from imap_processing.lo.l0.lol0 import LoL0


@dataclass
class StaticHousekeeping(LoL0):
    SHCOARSE: int
    BOARD_TYPE: int
    RESET_REASON_SOFT: int
    RESET_REASON_FPGA_WDOG: int
    RESET_REASON_CPU_WDOG: int
    RESET_REASON_PFO: int
    RESET_REASON_POR: int
    CPU_WDOG_STATE: int
    FPGA_WDOG_STATE: int
    WDOG_CNT: int
    INSTR_ID: int
    CDH_FPGA_VERSION: int
    IFB_FPGA_VERSION: int
    BULK_HVPS_VERSION: int
    FSW_VERSION: int
    ENG_LUT_VERSION: int
    SCI_LUT_VERSION: int
    SELECTED_IMG: int
    FSW_VERSION_STR: int
    ENG_LUT_VERSION_STR: int
    SCI_LUT_VERSION_STR: int
    SPARE: int
    CHKSUM: int

    def __init__(self, packet, software_version: str, packet_file_name: str, apid: int):
        super().__init__(
            software_version,
            packet_file_name,
            CcsdsData(packet.header),
            LoAPID.ILO_APP_SHK,
        )
        self.parse_data(packet)
