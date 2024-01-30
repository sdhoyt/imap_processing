"""IMAP-Lo L0 Decommutation."""
import logging
from pathlib import Path

import xarray as xr
from science_direct_events import ScienceDirectEvents

from imap_processing import decom
from imap_processing.lo import version
from imap_processing.lo.l0.utils.lo_l0_container import LoL0Container
from imap_processing.lo.l0.utils.loApid import LoAPID

logging.basicConfig(level=logging.INFO)


def decom_lo_packets(packet_file: str, xtce: str):
    """
    Unpack and decode Lo packets using CCSDS format and XTCE packet definitions.

    Parameters
    ----------
    packet_file : str
        Path to the CCSDS data packet file.
    xtce : str
        Path to the XTCE packet definition file.

    Returns
    -------
    dict
        A dictionary containing xr.Dataset for each APID. each dataset in the
        dictionary will be converted to a CDF.
    """
    # TODO: XTCE Files need to be combined
    logging.info(f"Unpacking {packet_file} using xtce definitions in {xtce}")
    packets = decom.decom_packets(packet_file, xtce)
    logging.info(f"{packet_file} unpacked")

    # packet_list=[]
    # for packet in packets:
    #     apid = packet.header["PKT_APID"].derived_value
    #     if apid not in packet_list:
    #         packet_list.append(apid)

    # remove any empty packets

    print(packets[0])
    filtered_packets = list(filter(lambda x: len(x.data) != 0, packets))
    # sort all the packets in the list by their spacecraft time
    sorted_packets = sorted(
        filtered_packets, key=lambda x: x.data["SHCOARSE"].derived_value
    )
    filename = Path(packet_file).name
    l0_data = LoL0Container()

    for packet in sorted_packets:
        apid = packet.header["PKT_APID"].derived_value
        if apid == LoAPID.ILO_SCI_DE:
            l0_data.append(ScienceDirectEvents(packet, version, filename))
        else:
            raise Exception(f"lo_l0_decom.py - The APID {apid} is not valid for Lo")

    sci_de = l0_data.filter_data(LoAPID.ILO_SCI_DE)
    if sci_de:
        sci_de_count = xr.DataArray(
            name="count",
            data=[sci_de_data.COUNT for sci_de_data in sci_de],
        )
        sci_de_checksum = xr.DataArray(
            name="checksum", data=[sci_de_data.CKSM for sci_de_data in sci_de]
        )
        sci_de_tof0 = xr.DataArray(
            name="tof0", data=[sci_de_data.TOF0 for sci_de_data in sci_de]
        )
        sci_de_tof1 = xr.DataArray(
            name="tof1", data=[sci_de_data.TOF1 for sci_de_data in sci_de]
        )
        sci_de_tof2 = xr.DataArray(
            name="tof2", data=[sci_de_data.TOF2 for sci_de_data in sci_de]
        )
        sci_de_tof3 = xr.DataArray(
            name="tof3", data=[sci_de_data.TOF3 for sci_de_data in sci_de]
        )
        sci_de_energy = xr.DataArray(
            name="energy", data=[sci_de_data.ENERGY for sci_de_data in sci_de]
        )
        sci_de_pos = xr.DataArray(
            name="pos", data=[sci_de_data.POS for sci_de_data in sci_de]
        )

        sci_de_dataset = xr.Dataset(
            data_vars={
                "count": sci_de_count,
                "checksum": sci_de_checksum,
                "tof0": sci_de_tof0,
                "tof1": sci_de_tof1,
                "tof2": sci_de_tof2,
                "tof3": sci_de_tof3,
                "energy": sci_de_energy,
                "pos": sci_de_pos,
            }
        )
