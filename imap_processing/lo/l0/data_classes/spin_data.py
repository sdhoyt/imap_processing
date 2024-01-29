from dataclasses import dataclass

from imap_processing.ccsds.ccsds_data import CcsdsData
from imap_processing.lo.l0.utils.loApid import LoAPID
from imap_processing.lo.l0.lol0 import LoL0


@dataclass
class Spin(LoL0):
    SHCOARSE: int
    NUM_COMPLETED: int
    SPARE1: int
    ACQ_END_SEC: int
    ACQ_END_SUBSEC: int
    SPARE2: int
    # TODO: will probably need to read this whole chunk of data
    # as binary from the CCSDS and parse within the file since each
    # data index is a separate field
    SPIN_SECOND: list()
    SPIN_SUBSEC: list()
    ESA_P_DAC: list()
    ESA_N_DAC: list()
    VAL_PERIOD: list()
    VAL_SPIN: list()
    SOURCE: list()
    RESERVED: list()

    def __init__(self, packet, software_version: str, packet_file_name: str, apid: int):
        super().__init__(
            software_version,
            packet_file_name,
            CcsdsData(packet.header),
            LoAPID.ILO_SPIN,
        )
        self.parse_data(packet)
