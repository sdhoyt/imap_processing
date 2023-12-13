from dataclasses import dataclass

from imap_processing.ccsds.ccsds_data import CcsdsData
from imap_processing.lo.l0.lol0 import LoL0
from imap_processing.lo.l0.loApid import LoAPID

@dataclass
class DiagnosticPCC(LoL0):
    SHCOARSE: int
    COARSE_POT_PRI: int
    FINE_POT_PRI: int
    COARSE_POT_RED: int
    FINE_POT_RED: int
    ACTUATOR_TEMP: int
    PCC_BOARD_TEMP: int
    MOTOR_CURRENT_PRI: int
    MOTOR_CURRENT_RED: int
    CUMULATIVE_CNT_PRI: int
    CUMULATIVE_CNT_SGN_PRI: int
    CUMULATIVE_CNT_RED: int
    CUMULATIVE_CNT_SGN_RED: int
    CURRENT_STEP_CNT_PRI: int
    CURRENT_STEP_CNT_RED: int
    CURRENT_SETPT_PRI: int
    CURRENT_SETPT_RED: int
    STATUS: int
    SPARE: int
    CHKSUM: int

    def __init__(self, packet, software_version: str, packet_file_name: str, apid:int):
        super().__init__(software_version, packet_file_name, CcsdsData(packet.header), LoAPID.ILO_DIAG_PCC)
        self.parse_data(packet)
