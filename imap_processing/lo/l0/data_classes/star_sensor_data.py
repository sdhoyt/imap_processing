from dataclasses import dataclass

from imap_processing.ccsds.ccsds_data import CcsdsData
from imap_processing.lo.l0.lol0 import LoL0
from imap_processing.lo.l0.utils.loApid import LoAPID


@dataclass
class StarSensor(LoL0):
    SHCOARSE: int
    COUNT: int
    # TODO: need to update xtce to read this all in as binary
    # in the telem def each index is a separate field ie.
    # DATA_000, DATA_001, etc.
    DATA: list()

    def __init__(self, packet, software_version: str, packet_file_name: str, apid: int):
        super().__init__(
            software_version,
            packet_file_name,
            CcsdsData(packet.header),
            LoAPID.ILO_STAR,
        )
        self.parse_data(packet)

    # TODO: Add decompression
