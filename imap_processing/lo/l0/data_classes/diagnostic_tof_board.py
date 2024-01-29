from dataclasses import dataclass

from imap_processing.ccsds.ccsds_data import CcsdsData
from imap_processing.lo.l0.utils.loApid import LoAPID
from imap_processing.lo.l0.lol0 import LoL0


@dataclass
class DiagnosticTOFBoard(LoL0):
    SHCOARSE: int
    TOF_IF_STATUS_SPARE1: int
    TOF_IF_STATUS_PKT_RCVD: int
    TOF_IF_STATUS_ADC_PKT: int
    TOF_IF_STATUS_REG_PKT: int
    TOF_IF_STATUS_CNT_PKT: int
    TOF_IF_STATUS_DE_PKT: int
    TOF_IF_STATUS_SPARE2: int
    TOF_IF_STATUS_TO_ERR: int
    TOF_IF_STATUS_ID_ERR: int
    TOF_IF_STATUS_FRM_ERR: int
    CMD_ERROR: int
    CFD_VM: int
    PRE_TM: int
    REG_TM: int
    MCP_CM: int
    MCP_VM: int
    CM: int
    P5_VM: int
    P6_VM: int
    AN_A_THR: int
    AN_B0_THR: int
    AN_B3_THR: int
    AN_C_THR: int
    TOF_BD_TLM_EN: int
    DIRECT_EVENT_TLM_EN: int
    SPARE1: int
    TOF3_REQUIRED: int
    TOF2_REQUIRED: int
    TOF1_REQUIRED: int
    TOF0_REQUIRED: int
    STIM_ANODE_C_EN: int
    STIM_ANODE_C_SRC: int
    STIM_ANODE_B3_EN: int
    STIM_ANODE_B3_SRC: int
    STIM_ANODE_B0_EN: int
    STIM_ANODE_B0_SRC: int
    STIM_ANODE_A_EN: int
    STIM_ANODE_A_SRC: int
    STIM_FREQ: int
    STIM_DELAY: int
    TOF3_THR: int
    TOF2_THR: int
    TOF1_THR: int
    TOF0_THR: int
    SPARE2: int
    TOF3_VETO: int
    TOF2_VETO: int
    TOF1_VETO: int
    TOF0_VETO: int
    CHKSUM: int

    def __init__(self, packet, software_version: str, packet_file_name: str, apid: int):
        super().__init__(
            software_version,
            packet_file_name,
            CcsdsData(packet.header),
            LoAPID.ILO_DIAG_TOF_BD,
        )
        self.parse_data(packet)
