from dataclasses import dataclass

from imap_processing.ccsds.ccsds_data import CcsdsData
from imap_processing.lo.l0.lol0 import LoL0
from imap_processing.lo.l0.loApid import LoAPID

@dataclass
class Autonomy(LoL0):
    """L1A Science Drect Events data.

    The Science Direct Events class handles the parsing and
    decompression of L0 to L1A data.

    Attributes
    ----------
    SHCOARSE : int
        Spacecraft time
    COUNT: int
        Number of direct events
    DATA: str
        Compressed TOF Direct Event time tagged data.
    TOF0: int
        Time of Flight 0 value for direct event.
    TOF1: int
        Time of Flight 1 value for direct event.
    TOF2: int
        Time of Flight 2 value for direct event.
    TOF3: int
        Time of Flight 3 value for direct event.
    TIME: int
        time tag for the direct event
        #TODO: Is this different than the SHCOARSE?
    ENERGY: int
        energy of the direct event ENA.
    POS: int
        Position of the direct event ENA
        #TODO: Is this the position on the final detector?
    CKSM: int
        #TODO: There's a checksum in the packet and another in
        the dedcompressed data? Are these different?

    Methods
    -------
    __init__(packet, software_vesion, packet_file_name):
        Constructor, uses the CCSDS packet, version of the software, and
        the name of the packet file to parse and store information about
        the Direct Event packet data.
    decompress_data():
        Decompresses the Science Direct Event TOF  data.

    """

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
    def __init__(self, packet, software_version: str, packet_file_name: str, apid:int):
        super().__init__(software_version, packet_file_name, CcsdsData(packet.header), LoAPID.ILO_AUTO)
        self.parse_data(packet)
