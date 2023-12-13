from dataclasses import dataclass
from imap_processing.lo.l0.loApid import LoAPID

@dataclass
class LoL0Container:
    data: list()

    def append(self, data):
        self.data.append(data)

    def filter_data(self, apid):
        return list(filter(lambda item: item.APID == apid, self.data))
