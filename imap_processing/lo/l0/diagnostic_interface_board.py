from dataclasses import dataclass

from imap_processing.ccsds.ccsds_data import CcsdsData
from imap_processing.lo.l0.lol0 import LoL0


@dataclass
class DiagnosticInterfaceBoard(LoL0):
    SHCOARSE: int
    IF_CONTROL_SPARE1: int
    IF_CONTROL_CMD_ERR: int
    IF_CONTROL_SPARE2: int
    IF_CONTROL_EN: int
    REG_IF_SPARE1: int
    REG_IF_PKT_RCVD: int
    REG_IF_SPARE2: int
    REG_IF_TO_ERR: int
    REG_IF_ID_ERR: int
    REG_IF_FRM_ERR: int
    ADC_IF_STATUS_SPARE1: int
    ADC_IF_STATUS_SS_UN: int
    ADC_IF_STATUS_SS_OV: int
    ADC_IF_STATUS_SS_FF: int
    ADC_IF_STATUS_SS_HF: int
    ADC_IF_STATUS_SS_FE: int
    ADC_IF_STATUS_SPARE2: int
    ADC_IF_STATUS_PKT_RCVD: int
    ADC_IF_STATUS_SPARE3: int
    ADC_IF_STATUS_TO_ERR: int
    ADC_IF_STATUS_ID_ERR: int
    ADC_IF_STATUS_FRM_ERR: int
    FPGA_VERSION: int
    SPARE1: int
    HV_DISABLE: int
    HV_LIMIT: int
    BOARD_ID: int
    CMD_COUNT: int
    SPARE2: int
    ADC_AUX_MUX: int
    ADC_CLK_DIS: int
    OSCOPE_EN: int
    STAR_SYNC: int
    IFB_DATA_EN: int
    IFB_DATA_INTERVAL: int
    SYNC_CLK_MSB: int
    PAC_EN_MSB: int
    MCP_EN_MSB: int
    LV_EN_MSB: int
    SYNC_CLK_LSB: int
    PAC_EN_LSB: int
    MCP_EN_LSB: int
    LV_EN_LSB: int
    PAC_VSET: int
    PAC_OCP: int
    MCP_VSET: int
    MCP_OCP: int
    STAR_OFFSET_ADJUST: int
    OSCOPE_CHANNEL_1: int
    OSCOPE_CHANNEL_0: int
    STAR_BRIGHT: int
    IFB_TEMP1: int
    IFB_TEMP0: int
    IFB_V5P0_VM: int
    IFB_V3P3_VM: int
    IFB_V12P0_VM: int
    IFB_V12N0_VM: int
    LV_CM: int
    LV_VM: int
    LV_TEMP: int
    MCP_CM: int
    MCP_VM: int
    MCP_TEMP: int
    PAC_CM: int
    PAC_VM: int
    PAC_TEMP: int
    SPARE3: int
    CHKSUM: int

    def __init__(self, packet, software_version: str, packet_file_name: str):
        super().__init__(software_version, packet_file_name, CcsdsData(packet.header))
        self.parse_data(packet)
