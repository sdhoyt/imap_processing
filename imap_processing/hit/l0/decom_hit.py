"""Decommutate HIT CCSDS data."""

from pathlib import Path

import xarray as xr

from imap_processing import imap_module_directory
from imap_processing.utils import packet_file_to_datasets


def parse_header(count_rates: str) -> None:
    """
    Parse science frame header fields.

    Parameters
    ----------
    count_rates : str
        Science frame binary for the first 6 packets.
    """
    # TODO need to figure out how this function should
    # return the header data
    # append(int(count_rates[0:2], 2))
    pass


# NOTES:
# use_derived_value boolean flag (default True) whether to use
# the derived value from the XTCE definition.
# True to get L1B housekeeping data with engineering units. False
# for L1A housekeeping data
# sc_tick is the time the packet was created
# Tweaked packet_file_to_datasets function to only return 40 packets
# (2 frames for testing)

packet_definition = (
    imap_module_directory / "hit/packet_definitions/hit_packet_definitions.xml"
)

# L0 file paths
# packet_file = Path(imap_module_directory / "tests/hit/test_data/hskp_sample.ccsds")
# packet_file = Path(imap_module_directory /
#                   "tests/hit/PREFLIGHT_raw_record_2023_256_15_59_04_apid1252.pkts")
packet_file = Path(imap_module_directory / "tests/hit/test_data/sci_sample.ccsds")


datasets_by_apid = packet_file_to_datasets(
    packet_file=packet_file,
    xtce_packet_definition=packet_definition,
)

print(datasets_by_apid)


# TODO: QUESTIONS:
#  Should we check if first packet has group flag = 1 and if not,
#  stop processing on the file? - Yes raise error so that failed job
#  makes it to the database
#  What epoch goes with each science frame? How do we handle this dimension?

# Group science packets into groups of 20. (Convert this into a function)
sci_dataset = datasets_by_apid[1252]

# Initialize a list to store valid science frames
count_rates_bin = []
pha_bin = []
# Iterate over the dataset in chunks of 20
for i in range(0, len(sci_dataset.epoch), 20):
    # Check if the slice length is exactly 20
    if i + 20 <= len(sci_dataset.epoch):
        seq_flgs_chunk = sci_dataset.seq_flgs[i : i + 20]
        science_data_chunk = sci_dataset.science_data[i : i + 20]
        # TODO:
        #  Add check for sequence counter to ensure it's incrementing by one
        #  (src_seq_ctr)
        #  Add handling for epoch values. Need to check with Grant and Eric

        # Check if the first packet is 1, the middle 18 packets are 0,
        # and the last packet is 2
        if (
            seq_flgs_chunk[0] == 1
            and all(seq_flgs_chunk[1:19] == 0)
            and seq_flgs_chunk[19] == 2
        ):
            # If the chunk is valid, append the science data to the list
            count_rates_bin.append("".join(science_data_chunk.data[0:6]))
            pha_bin.append("".join(science_data_chunk.data[6:]))
        else:
            # If the sequence doesn't match, you can either skip it or
            # raise a warning/error
            print(f"Invalid sequence found at index {i}")

# Convert the list to an xarray DataArray
count_rates_bin_data = xr.DataArray(
    count_rates_bin, dims=["group"], name="count_rates_bin"
)
pha_bin_data = xr.DataArray(pha_bin, dims=["group"], name="count_rates_bin")

# Now add this as a new data variable to the dataset
sci_dataset["count_rates_bin"] = count_rates_bin_data
sci_dataset["pha_bin"] = pha_bin_data

sci_dataset["hdr_unit_num"] = xr.DataArray([], name="hdr_unit_num")

count_rates_ints: list[int] = []
for count_rates in sci_dataset["count_rates_bin"].data:
    parse_header(count_rates)
    # parse rates, maybe break up into separate functions

print(sci_dataset)
