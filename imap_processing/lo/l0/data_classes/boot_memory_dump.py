from dataclasses import dataclass

from imap_processing.ccsds.ccsds_data import CcsdsData
from imap_processing.lo.l0.lol0 import LoL0
from imap_processing.lo.l0.utils.loApid import LoAPID


@dataclass
class BootMemoryDump(LoL0):
    SHCOARSE: int
    ADDR: int
    LEN: int
    DATA: str
    CHKSUM: int

    def __init__(self, packet, software_version: str, packet_file_name: str, apid: int):
        super().__init__(
            software_version,
            packet_file_name,
            CcsdsData(packet.header),
            LoAPID.ILO_BOOT_MEMDMP,
        )
        self.parse_data(packet)
