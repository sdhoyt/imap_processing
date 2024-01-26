from dataclasses import dataclass


@dataclass
class LoL0Container:
    data: list()

    def append(self, data):
        self.data.append(data)

    def filter_data(self, apid):
        return list(filter(lambda item: item.APID == apid, self.data))
