from dataclasses import dataclass

from imap_processing.ccsds.ccsds_data import CcsdsData
from imap_processing.lo.l0.lol0 import LoL0
from imap_processing.lo.l0.utils.loApid import LoAPID


@dataclass
class RawCounts(LoL0):
    # TODO: Should the ACCUM_MS numbers be stored as arrays or kept as separate variables?
    SHCOARSE: int
    MET_SUB: int
    START_A: int
    START_C: int
    STOP_B0: int
    STOP_B3: int
    TOF0: int
    TOF1: int
    TOF2: int
    TOF3: int
    ACCUM_MS_0: int
    ACCUM_MS_1: int
    ACCUM_MS_2: int
    ACCUM_MS_3: int
    ACCUM_MS_4: int
    ACCUM_MS_5: int
    ACCUM_MS_6: int
    ACCUM_MS_7: int
    ACCUM_MS_8: int
    ACCUM_MS_9: int
    TOF0_TOF1_0: int
    TOF0_TOF1_1: int
    TOF0_TOF1_2: int
    TOF0_TOF1_3: int
    TOF0_TOF1_4: int
    TOF0_TOF1_5: int
    TOF0_TOF1_6: int
    TOF0_TOF1_7: int
    TOF0_TOF1_8: int
    TOF0_TOF1_9: int
    TOF0_TOF2_0: int
    TOF0_TOF2_1: int
    TOF0_TOF2_2: int
    TOF0_TOF2_3: int
    TOF0_TOF2_4: int
    TOF0_TOF2_5: int
    TOF0_TOF2_6: int
    TOF0_TOF2_7: int
    TOF0_TOF2_8: int
    TOF0_TOF2_9: int
    TOF1_TOF2_0: int
    TOF1_TOF2_1: int
    TOF1_TOF2_2: int
    TOF1_TOF2_3: int
    TOF1_TOF2_4: int
    TOF1_TOF2_5: int
    TOF1_TOF2_6: int
    TOF1_TOF2_7: int
    TOF1_TOF2_8: int
    TOF1_TOF2_9: int
    SILVER_TRIPLE_0: int
    SILVER_TRIPLE_1: int
    SILVER_TRIPLE_2: int
    SILVER_TRIPLE_3: int
    SILVER_TRIPLE_4: int
    SILVER_TRIPLE_5: int
    SILVER_TRIPLE_6: int
    SILVER_TRIPLE_7: int
    SILVER_TRIPLE_8: int
    SILVER_TRIPLE_9: int
    DISC_TOF0: int
    DISC_TOF1: int
    DISC_TOF2: int
    DISC_TOF3: int
    PAC_VM: int
    MCP_VM: int
    CHKSUM: int

    def __init__(self, packet, software_version: str, packet_file_name: str, apid: int):
        super().__init__(
            software_version,
            packet_file_name,
            CcsdsData(packet.header),
            LoAPID.ILO_RAW_CNT,
        )
        self.parse_data(packet)


# Add Decompression
