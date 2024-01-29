from dataclasses import dataclass

from imap_processing.ccsds.ccsds_data import CcsdsData
from imap_processing.lo.l0.utils.loApid import LoAPID
from imap_processing.lo.l0.lol0 import LoL0


@dataclass
class EventMessages(LoL0):
    SHCOARSE: int
    QMSG_CNT: int
    EVENT_TIME: int
    EVENT_TIME_SUBSEC: int
    EVENT_ID: int
    PARAM_1: int
    PARAM_2: int
    PARAM_3: int
    PARAM_4: int
    PARAM_5: int
    PARAM_6: int
    PARAM_7: int
    PARAM_8: int
    PARAM_9: int
    CHKSUM: int

    def __init__(self, packet, software_version: str, packet_file_name: str, apid: int):
        super().__init__(
            software_version,
            packet_file_name,
            CcsdsData(packet.header),
            LoAPID.ILO_EVTMSG,
        )
        self.parse_data(packet)
