from dataclasses import dataclass, fields

from loApid import LoAPID


@dataclass
class BootHousekeeping:
    time: int
    boot_ver: int
    boot_cnt: int
    bist_stat: int
    bist_abus: int
    bist_dbus: int
    bist_mem_ff: int
    bist_mem_fl: int
    bist_mem_map: int
    bist_mem_cnt: int
    img_1_stat: int
    img_2_stat: int
    tab_1_stat: int
    tab_2_stat: int
    spare_0: int
    fsw_img_ver: int
    table_img_ver: int
    instr_id: int
    spare_1: int
    fpga_ver: int
    hv_lim: int
    hv_dis: int
    door_dis: int
    spare_2: int
    sys_temp_1: int
    sys_temp2: int
    sys_temp_3: int
    lvps_temp_1: int
    lvps_temp_2: int
    lvps_temp3: int
    lvps_v1: int
    lvps_v2: int
    lvps_v3: int
    lvps_v4: int
    lvps_v5: int
    lvps_l1: int
    lvps_l2: int
    lvps_l3: int
    lvps_l4: int
    lvps_l5: int
    cdh_1p5v: int
    cdh_1p8v: int
    cdh_3p3v: int
    cdh_n12v: int
    cdh_p12v: int
    cdh_5v: int
    cdh_ana_ref: int
    cdh_temp_1: int
    cdh_temp_2: int
    cdh_temp_3: int
    cdh_temp_4: int
    op_mode: int
    cdm_acc_cnt: int
    cmd_rej_cnt: int
    cmd_acc_opc: int
    cmd_rej_opc: int
    cmd_result: int
    itf_err_cnt: int

    def __init__(self, packet, software_version: str, packet_file_name: str):
        super().__init__(software_version, packet_file_name, CcsdsData(packet.header))
        attributes = [field.name for field in fields(self)]

        # For each item in packet, assign it to the matching attribute in the class.
        for key, item in packet.data.items():
            value = (
                item.derived_value if item.derived_value is not None else item.raw_value
            )
            if key in attributes:
                setattr(self, key, value)
            else:
                raise KeyError(
                    f"Did not find matching attribute in Histogram data class for "
                    f"{key}"
                )

    def parse_data(self, packet):
        if packet.header["PKT_APID"].derived_value == LoAPID.BOOT_HK:
            self.time.append(packet.data["SHOCOARSE"].derived_value)
            self.boot_ver.append(packet.data["BOOT_VER"].derived_value)
            self.boot_cnt.append(packet.data["BOOT_CNT"].derived_value)
            self.bist_stat.append(packet.data["BIST_STAT"].derived_value)
            self.bist_abus.append(packet.data["BIST_ABUS"].derived_value)
            self.bist_dbus.append(packet.data["BIST_DBUS"].derived_value)
            self.bist_mem_ff.append(packet.data["MEM_FF"].derived_value)
            self.bist_mem_fl.append(packet.data["MEM_FL"].derived_value)
            self.bist_mem_map.append(packet.data["MEM_MAP"].derived_value)
            self.bist_mem_cnt.append(packet.data["MEM_CNT"].derived_value)
            self.img_1_stat.append(packet.data["IMG_1_STAT"].derived_value)
            self.img_2_stat.append(packet.data["IMG_2_STAT"].derived_value)
            self.tab_1_stat.append(packet.data["TAB_1_STAT"].derived_value)
            self.tab_2_stat.append(packet.data["TAB_2_STAT"].derived_value)
            self.spare_0.append(packet.data["SPARE_0"].derived_value)
            self.fsw_img_ver.append(packet.data["FSW_IMG_VER"].derived_value)
            self.table_img_ver.append(packet.data["TABLE_IMG_VER"].derived_value)
            self.instr_id.append(packet.data["INSTR_ID"].derived_value)
            self.spare_1.append(packet.data["SPARE_1"].derived_value)
            self.fpga_ver.append(packet.data["FGPA_VER"].derived_value)
            self.hv_lim.append(packet.data["HV_LIM"].derived_value)
            self.hv_dis.append(packet.data["HV_DIS"].derived_value)
            self.door_dis.append(packet.data["DOOR_DIS"].derived_value)
            self.spare_2.append(packet.data["SPARE_2"].derived_value)
            self.sys_temp_1.append(packet.data["MDM25P_14_T"].derived_value)
            self.sys_temp2.append(packet.data["MDM25P_14_T"].derived_value)
            self.sys_temp_3.append(packet.data["MDM25P_14_T"].derived_value)
            self.lvps_temp_1.append(packet.data["LVPS_12V_T"].derived_value)
            self.lvps_temp_2.append(packet.data["LVPS_5V_T"].derived_value)
            self.lvps_temp3.append(packet.data["LVPS_3P3V_T"].derived_value)
            self.lvps_v1.append(packet.data["LVPS_3P3V"].derived_value)
            self.lvps_v2.append(packet.data["LVPS_5V"].derived_value)
            self.lvps_v3.append(packet.data["LVPS_N5V"].derived_value)
            self.lvps_v4.append(packet.data["LVPS_12V"].derived_value)
            self.lvps_v5.append(packet.data["LVPS_N12V"].derived_value)
            self.lvps_l1.append(packet.data["LVPS_3P3V_I"].derived_value)
            self.lvps_l2.append(packet.data["LVPS_5V_I"].derived_value)
            self.lvps_l3.append(packet.data["LVPS_N5V_I"].derived_value)
            self.lvps_l4.append(packet.data["LVPS_12V_I"].derived_value)
            self.lvps_l5.append(packet.data["LVPS_N12V_I"].derived_value)
            self.cdh_1p5v.append(packet.data["CDH_1P5V"].derived_value)
            self.cdh_1p8v.append(packet.data["CDH_1P8V"].derived_value)
            self.cdh_3p3v.append(packet.data["CDH_3P3V"].derived_value)
            self.cdh_n12v.append(packet.data["CDH_12V"].derived_value)
            self.cdh_p12v.append(packet.data["CDH_N12V"].derived_value)
            self.cdh_5v.append(packet.data["CDH_5V"].derived_value)
            self.cdh_ana_ref.append(packet.data["CDH_5V_ADC"].derived_value)
            self.cdh_temp_1.append(packet.data["CDH_PROCESSOR_T"].derived_value)
            self.cdh_temp_2.append(packet.data["CDH_1P8V_LDO_T"].derived_value)
            self.cdh_temp_3.append(packet.data["CDH_1P5V_LDO_T"].derived_value)
            self.cdh_temp_4.append(packet.data["CDH_SDRAM_T"].derived_value)
            self.op_mode.append(packet.data["OP_MODE"].derived_value)
            self.cdm_acc_cnt.append(packet.data["CMD_ACC_CNT"].derived_value)
            self.cmd_rej_cnt.append(packet.data["CMD_EXE_CNT"].derived_value)
            self.cmd_acc_opc.append(packet.data["CMD_REJ_CNT"].derived_value)
            self.cmd_rej_opc.append(packet.data["CMD_LAST_OPCODE"].derived_value)
            self.cmd_result.append(packet.data["CMD_RESULT"].derived_value)
            self.itf_err_cnt.append(packet.data["ITF_ERR_CNT"].derived_value)
