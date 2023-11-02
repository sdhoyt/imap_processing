from loApid import LoAPID


class Autonomy:
    def __init__(self):
        self.time = list()
        self.spare = list()
        self.power_cycle_req = list()
        self.power_off_req = list()
        self.heater_ctrl_en = list()
        self.heater_1_state = list()
        self.heater_2_state = list()

    # this should get a single autonomy packet that can be assumed to already
    # be in chronological order to the last time this method was called
    def parse_autonomy_data(self, packet):
        if packet.header["PKT_APID"].derived_value == LoAPID.ILO_AUTO:
            self.time.append(packet.data["SHOCOARSE"].derived_value)
            self.spare.append(packet.data["SPARE"].derived_value)
            self.power_cycle_req.append(packet.data["POWER_CYCLE_REQ"].derived_value)
            self.power_off_req.append(packet.data["POWER_OFF_REQ"].derived_value)
            self.heater_ctrl_en.append(packet.data["HEATER_CTRL_EN"].derived_value)
            self.heater_1_state.append(packet.data["HEATER_1_STATE"].derived_value)
            self.heater_2_state.append(packet.data["HEATER_2_STATE"].derived_value)
