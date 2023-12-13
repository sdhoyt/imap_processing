import logging
from pathlib import Path

from imap_processing import decom

from autonomy import Autonomy
from boot_housekeeping import BootHousekeeping
from boot_memory_dump import BootMemoryDump
from diagnostic_bulk_hvps import DiagnosticBulkHVPS
from diagnostic_cdh import DiagnosticCDH
from diagnostic_interface_board import DiagnosticInterfaceBoard
from diagnostic_pcc import DiagnosticPCC
from diagnostic_tof_board import DiagnosticTOFBoard
from event_messages import EventMessages
from memory_dump import MemoryDump
from nominal_housekeeping import NominalHousekeeping
from raw_counts import RawCounts
from raw_direct_events import RawDirectEvents
from raw_star_sensor import RawStarSensor
from science_counts import ScienceCounts
from spin_data import Spin
from star_sensor_data import StarSensor
from static_housekeeping import StaticHousekeeping

from imap_processing.lo.l0.lo_l0_container import LoL0Container
from imap_processing.lo import version
from imap_processing.lo.l0.boot_housekeeping import BootHousekeeping
from imap_processing.lo.l0.loApid import LoAPID

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
        if apid == LoAPID.ILO_BOOT_HK:
            l0_data.append(BootHousekeeping(packet, version, filename))
        elif apid == LoAPID.ILO_BOOT_MEMDMP:
            l0_data.append(BootMemoryDump(packet, version, filename))
        elif apid == LoAPID.ILO_APP_NHK:
            l0_data.append(NominalHousekeeping(packet, version, filename))
        elif apid == LoAPID.ILO_APP_SHK:
            l0_data.append(StaticHousekeeping(packet, version, filename))
        elif apid == LoAPID.ILO_AUTO:
           l0_data.append(Autonomy(packet, version, filename))
        elif apid == LoAPID.ILO_DIAG_BULK_HVPS:
           l0_data.append(DiagnosticBulkHVPS(packet, version, filename))
        elif apid == LoAPID.ILO_DIAG_CDH:
            l0_data.append(DiagnosticCDH(packet, version, filename))
        elif apid == LoAPID.ILO_DIAG_IFB:
            l0_data.append(DiagnosticInterfaceBoard(packet, version, filename))
        elif apid == LoAPID.ILO_DIAG_PCC:
            l0_data.append(DiagnosticPCC(packet, version, filename))
        elif apid == LoAPID.ILO_DIAG_TOF_BD:
            l0_data.append(DiagnosticTOFBoard(packet, version, filename))
        elif apid == LoAPID.ILO_EVTMSG:
            l0_data.append(EventMessages(packet, version, filename))
        elif apid == LoAPID.ILO_MEMDMP:
            l0_data.append(MemoryDump(packet, version, filename))
        elif apid == LoAPID.ILO_RAW_CNT:
            l0_data.append(RawCounts(packet, version, filename))
        elif apid == LoAPID.ILO_RAW_DE:
           l0_data.append(RawDirectEvents(packet, version, filename))
        elif apid == LoAPID.ILO_RAW_STAR:
            l0_data.append(RawStarSensor(packet, version, filename))
        elif apid == LoAPID.ILO_SCI_CNT:
            l0_data.append(ScienceCounts(packet, version, filename))
        elif apid == LoAPID.ILO_SCI_DE:
            #TODO: The SCI DE class will be added in a separate PR specifically
            # for SCI DE compression
            pass
        elif apid == LoAPID.ILO_SPIN:
            l0_data.append(Spin(packet, version, filename))
        elif apid == LoAPID.ILO_STAR:
            l0_data.append(StarSensor(packet, version, filename))
        else:
            raise Exception(f"lo_l1a_decom.py - The APID {apid} is not valid for Lo")
        
        #TODO: orgnaize data in dataclasses into CDFs