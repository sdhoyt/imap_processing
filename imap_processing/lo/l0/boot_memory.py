from loApid import LoAPID

class BootMemory:
    def __init__(self):
        self.time = list()
        self.addr = list()
        self.len = list()
        self.data = list()
    def parse_boot_memory(self, packet):
        if packet.header["PKT_APID"].derived_value == LoAPID.BOOT_MEMDMP:
            self.time.append(packet.data['SHOCOARSE'].derived_value)
            self.addr.append(packet.data['ADDR'].derived_value)
            self.len.append(packet.data['LEN'].derived_value)
            self.data.append(packet.data['DATA'].raw)
