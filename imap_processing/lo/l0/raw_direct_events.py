from dataclasses import dataclass

from loApid import LoAPID

from imap_processing.ccsds.ccsds_data import CcsdsData
from imap_processing.lo.l0.lol0 import LoL0

@dataclass
class RawDirectEvents(LoL0):
    SHCOARSE: int
    PAC_VM: int
    MCP_VM: int
    PKT_CNT: int
    # TODO: RAW_DE not parsed from CCSDS. Need to add code to parse this
    RAW_DE: str
    CHKSUM: int
