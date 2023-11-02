from loApid import LoAPID

class DiagnosticCDH:
    def __init__(self):
        self.data_dict = dict()

    def parse_diagnostic_cdh(self, packet):
        if packet.header["PKT_APID"].derived_value == LoAPID.ILO_DIAG_CDH:
            for field in self.packet_cdf_fields:
                self.data_dict[field[1]].append(packet.data[field[0]].derived_value)

    def data(self):
        return self.data_dict
