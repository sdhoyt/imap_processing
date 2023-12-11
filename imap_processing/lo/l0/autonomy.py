from dataclasses import dataclass

from loApid import LoAPID

from imap_processing.ccsds.ccsds_data import CcsdsData
from imap_processing.lo.l0.lol0 import LoL0

@dataclass
class Autonomy(LoL0):
    SHCOARSE: int
    SPARE: int
    POWER_CYCLE_REQ: int
    POWER_OFF_REQ: int
    HEATER_CTRL_EN: int
    HEATER_1_STATE: int
    HEATER_2_STATE: int
    SPARE2: int
    CHKSUM: int

    # this should get a single autonomy packet that can be assumed to already
    # be in chronological order to the last time this method was called
    def __init__(self, packet, software_version: str, packet_file_name: str):
        super().__init__(software_version, packet_file_name, CcsdsData(packet.header))
        self.parse_data(packet)
