from dataclasses import dataclass

from imap_processing.ccsds.ccsds_data import CcsdsData
from imap_processing.lo.l0.lol0 import LoL0
from imap_processing.lo.l0.loApid import LoAPID

@dataclass
class RawDirectEvents(LoL0):
    SHCOARSE: int
    PAC_VM: int
    MCP_VM: int
    PKT_CNT: int
    # TODO: RAW_DE is binary from CCSDS. Need to add code to parse this in a method
    RAW_DE: str
    CHKSUM: int
    COUNT: int
    DE_TIME: int
    TOF0: int
    TOF2: int
    TOF3: int

    def __init__(self, packet, software_version: str, packet_file_name: str, apid:int):
        super().__init__(software_version, packet_file_name, CcsdsData(packet.header), LoAPID.ILO_RAW_DE)
        self.parse_data(packet)
