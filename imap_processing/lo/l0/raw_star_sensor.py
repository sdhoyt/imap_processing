
from imap_processing.ccsds.ccsds_data import CcsdsData


class RawStarSensor:
    SHCOARSE: int
    COUNT: int
    # TODO: I might want to read this in as binary from the CSSDS.
    # There aer multiple fields for this labeled "RAW_DATA_0000",
    # "RAW_DATA_0001", etc. Might be easier to parse that in this
    # file so I can utilize the super classes parsing method.
    RAW_DATA: list()

    def __init__(self, packet, software_version: str, packet_file_name: str):
        super().__init__(software_version, packet_file_name, CcsdsData(packet.header))
        self.parse_data(packet)
