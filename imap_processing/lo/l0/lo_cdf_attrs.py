#TODO: Need to add version to init
from imap_processing.lo import __version__
from imap_processing.cdf.defaults import GlobalConstants
from imap_processing.cdf.global_attrs import (
    AttrBase,
    GlobalDataLevelAttrs,
    GlobalInstrumentAttrs,
    ScienceAttrs,
    StringAttrs
)
descriptor = "IMAP-Lo>Interstellar Mapping and Acceleration Probe Low"
lo_description_text = {
    "IMAP-Lo is a single-pixel neutral atom imager that delivers "
    "energy and position measurements of low-energy Interstellar "
    "Neutral (ISN) atoms tracked over the ecliptic longitude >180° "
    "and global maps of energetic neutral atoms (ENAs). Mounted on a "
    "pivot platform, IMAP-Lo tracks the flow of these ions through the "
    "local interstellar medium (LISM) to precisely determine the "
    "species-dependent flow speed, temperature, and direction of the "
    "LISM that surrounds, interacts with, and determines the outer "
    "boundaries of the global heliosphere. IMAP-Lo uses the pivoting "
    "field of view (FOV) to view variable angles out to 90° from the "
    "spin axis. This assists IMAP-Lo to pinpoint the intersection between "
    "the ISN inflow speed and longitude to uniquely determine the LISM flow "
    "vector. Data from IMAP-Lo will help us be able to see from inside the "
    "heliosphere what it is like just outside the solar system, our local "
    "neighborhood."
}

lo_base = GlobalInstrumentAttrs(
    version=__version__, descriptor=descriptor, text=lo_description_text
)

lo_l1a_global_attrs = GlobalDataLevelAttrs(
    data_type="L1A->Level-1A",
    logical_source="imap_lo_l1a_scide",
    logical_source_desc="IMAP Mission IMAP-Lo Instrument Level-1A Data",
    instrument_base=lo_base
)

lo_l1b_global_attrs = GlobalDataLevelAttrs(
    data_type="L1B->Level-1B",
    logical_source="imap_lo_l1b",
    logical_source_desc="IMAP Mission IMAP-Lo Instrument Level-1B Data",
    instrument_base=lo_base
)

lo_l1c_global_attrs = GlobalDataLevelAttrs(
    data_type="L1C->Level-1C",
    logical_source="imap_lo_l1c",
    logical_source_desc="IMAP Mission IMAP-Lo Instrument Level-1C Data",
    instrument_base=lo_base
)

lo_tof_attrs = ScienceAttrs(
    validmin=0,
    validmax=GlobalConstants.INT_MAXVAL,
    catdesc="Time of Flight",
    # TODO: Not sure if depend_0 and display type are right
    depend_0="epoch",
    display_type="time_series",
    fill_val=GlobalConstants.INT_FILLVAL,
    format="I12",
    var_type="data",
    units="seconds"
)