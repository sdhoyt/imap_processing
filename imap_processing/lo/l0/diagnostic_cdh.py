from dataclasses import dataclass

from imap_processing.ccsds.ccsds_data import CcsdsData
from imap_processing.lo.l0.lol0 import LoL0
from imap_processing.lo.l0.loApid import LoAPID

@dataclass
class DiagnosticCDH(LoL0):
    SHCOARSE: int
    JUMPER_REG: int
    RESET_REG: int
    WATCHDOG_REG: int
    CTRL_STATUS_REG: int
    SCRATCHPAD_1_REG: int
    SCRATCHPAD_2_REG: int
    CPU_UART_CLOCK_BAUD_REG: int
    TICK_TIMER_CTRL_STATUS_REG: int
    TICK_TIMER_RELOAD_COUNT_REG: int
    TICK_TIMER_COUNTER_REG: int
    MET_CTRL_REG: int
    MET_STATUS_REG: int
    MET_COARSE_COUNTER_REG: int
    MET_FINE_COUNTER_REG: int
    MDM25P_14_T: int
    MDM25P_15_T: int
    MDM25P_16_T: int
    LO_T: int
    HVPS_T: int
    LVPS_12V_T: int
    LVPS_5V_T: int
    LVPS_3P3V_T: int
    LVPS_3P3V: int
    LVPS_5V: int
    LVPS_N5V: int
    LVPS_12V: int
    LVPS_N12V: int
    LVPS_3P3V_I: int
    LVPS_5V_I: int
    LVPS_N5V_I: int
    LVPS_12V_I: int
    LVPS_N12V_I: int
    CDH_1P5V: int
    CDH_1P8V: int
    CDH_3P3V: int
    CDH_12V: int
    CDH_N12V: int
    CDH_5V: int
    CDH_5V_ADC: int
    CDH_PROCESSOR_T: int
    CDH_1P8V_LDO_T: int
    CDH_1P5V_LDO_T: int
    CDH_SDRAM_T: int
    ADC_CTRL_STATUS_REG: int
    SC_CMD_FIFO_CTRL_STATUS_REG: int
    SC_TLM_FIFO_CTRL_STATUS_REG: int
    INTERRUPT_LEVEL_REG: int
    INTERRUPT_PENDING_REG: int
    INTERRUPT_ENABLE_REG: int
    SPIN_ENABLE_AND_STATUS_REG: int
    SPIN_BIN_PERIOD_REG: int
    SPIN_BIN_INDEX_REG: int
    SPIN_PERIOD_REG: int
    SPIN_PERIOD_TIMER_REG: int
    SPIN_PERIOD_TIMER_AT_NXT_PPS_REG: int
    SPIN_TIME_STAMP_SECONDS_REG: int
    SPIN_TIME_STAMP_SUBSECONDS_REG: int
    LOOPBACK_CTRL_REG: int
    LOOPBACK_STATUS_REG: int
    LOOPBACK_TX_REG: int
    LOOPBACK_RX_REG: int
    DISCRETE_IO_REG: int
    HEATER_CTRL_REG: int
    HEATER_STATUS_REG: int
    INSTR_PWR_CTRL_REG: int
    INSTR_PWR_STATUS_REG: int
    IFB_INTERFACE_CTRL_STATUS_REG: int
    IFB_INTERFACE_CMD_REG: int
    IFB_ADC_TLM_STATUS_REG: int
    IFB_REG_TLM_STATUS_REG: int
    TOF_INTERFACE_STATUS_REG: int
    DE_TIME_TAG_RESOLUTION_REG: int
    DE_TIME_TAG_CTRL_STATUS_REG: int
    DE_FIFO_CTRL_STATUS_REG: int
    FEE_RESET_STATUS_REG: int
    FEE_RESET_CMD_REG: int
    FEE_RESET_DURATION_REG: int
    SPIN_PULSE_DURATION_REG: int
    HVPS_CTRL_REG: int
    HVPS_STATUS_REG: int
    HVPS_CMD_REG: int
    PIVOT_INTERFACE_CTRL_REG: int
    PIVOT_INTERFACE_STATUS_REG: int
    PIVOT_CMD_DATA_REG: int
    PIVOT_CMD_OPCODE_REG: int
    CHKSUM: int

    def __init__(self, packet, software_version: str, packet_file_name: str, apid:int):
        super().__init__(software_version, packet_file_name, CcsdsData(packet.header), LoAPID.ILO_DIAG_CDH)
        self.parse_data(packet)
