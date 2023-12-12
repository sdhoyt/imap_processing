from dataclasses import dataclass

from imap_processing.ccsds.ccsds_data import CcsdsData


@dataclass
class StarSensorData:
    SHCOARSE: int
    COUNT: int
    # TODO: need to update xtce to read this all in as binary
    # in the telem def each index is a separate field ie.
    # DATA_000, DATA_001, etc.
    DATA: list()

    def __init__(self, packet, software_version: str, packet_file_name: str):
        super().__init__(software_version, packet_file_name, CcsdsData(packet.header))
        self.parse_data(packet)
