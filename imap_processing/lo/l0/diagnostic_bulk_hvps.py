from dataclasses import dataclass

from imap_processing.ccsds.ccsds_data import CcsdsData
from imap_processing.lo.l0.loApid import LoAPID


@dataclass
class DiagnosticBulkHVPS:
    SHCOARSE: int
    VERSION: int
    STATUS: int
    GPO: int
    DAC0: int
    DAC1: int
    DAC2: int
    DAC3: int
    DAC4: int
    ADC_CTRL_STATUS: int
    ADC1_WAIT_CNT: int
    ADC2_WAIT_CNT: int
    HVPS_BULK_VMON: int
    U_NEG_VMON: int
    U_POS_VMON: int
    DEF_NEG_VMON: int
    DEF_POS_VMON: int
    PMT_VMON: int
    PMT_IMON: int
    BULK_IMON: int
    DEF_NEG_IMON: int
    DEF_POS_IMON: int
    ADC_REF1_VMON: int
    ADC_REF2_VMON: int
    P12P0_VMON: int
    N12P0_VMON: int
    P3P3_VMON: int
    P1P5_VMON: int
    CHKSUM: int

    def __init__(self, packet, software_version: str, packet_file_name: str, apid: int):
        super().__init__(
            software_version,
            packet_file_name,
            CcsdsData(packet.header),
            LoAPID.ILO_DIAG_BULK_HVPS,
        )
        self.parse_data(packet)
