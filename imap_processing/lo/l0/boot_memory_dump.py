from loApid import LoAPID
from dataclasses import dataclass

from imap_processing.ccsds.ccsds_data import CcsdsData
from imap_processing.lo.l0.lol0 import LoL0

@dataclass
class BootMemoryDump(LoL0):
    SHCOARSE: int
    ADDR: int
    LEN: int
    DATA: str
    CHKSUM: int

    def __init__(self, packet, software_version: str, packet_file_name: str):
        super().__init__(software_version, packet_file_name, CcsdsData(packet.header))
        self.parse_data(packet)
