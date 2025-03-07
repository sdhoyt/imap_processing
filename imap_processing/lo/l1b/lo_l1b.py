"""IMAP-Lo L1B Data Processing."""

from dataclasses import Field
from pathlib import Path

import numpy as np
import xarray as xr

from imap_processing.cdf.imap_cdf_manager import ImapCdfAttributes
from imap_processing.lo.l1b.lo_conversions import (
    TOF0_CONV,
    TOF1_CONV,
    TOF2_CONV,
    TOF3_CONV,
)
from imap_processing.spice.time import met_to_ttj2000ns


def lo_l1b(dependencies: dict, data_version: str) -> list[Path]:
    """
    Will process IMAP-Lo L1A data into L1B CDF data products.

    Parameters
    ----------
    dependencies : dict
        Dictionary of datasets needed for L1B data product creation in xarray Datasets.
    data_version : str
        Version of the data product being created.

    Returns
    -------
    created_file_paths : list[pathlib.Path]
        Location of created CDF files.
    """
    # create the attribute manager for this data level
    attr_mgr_l1b = ImapCdfAttributes()
    attr_mgr_l1b.add_instrument_global_attrs(instrument="lo")
    attr_mgr_l1b.add_instrument_variable_attrs(instrument="lo", level="l1b")
    attr_mgr_l1b.add_global_attribute("Data_version", data_version)

    attr_mgr_l1a = ImapCdfAttributes()
    attr_mgr_l1a.add_instrument_variable_attrs(instrument="lo", level="l1a")

    # if the dependencies are used to create Annotated Direct Events
    if "imap_lo_l1a_de" in dependencies and "imap_lo_l1a_spin" in dependencies:
        logical_source = "imap_lo_l1b_de"
        spin_data = dependencies["imap_lo_l1a_spin"]
        l1a_de = dependencies["imap_lo_l1a_de"]
        l1b_de = xr.Dataset(
            attrs=attr_mgr_l1b.get_global_attributes(logical_source),
        )
        # Get the start and end times for each spin epoch
        acq_start, acq_end = convert_start_end_times(spin_data)
        # Get the average spin durations for each epoch
        avg_spin_durations = get_avg_spin_durations(acq_start, acq_end)
        # get spin phase for each DE
        spin_phase = get_spin_phase(l1a_de, avg_spin_durations)
        # calculate and set the spin bin based on the spin phase
        # spin bins are 0 - 60 bins
        l1b_de = set_spin_bin(l1b_de, spin_phase)
        # calculate and set the pointing bin based on the spin phase
        # pointing bin is 3600 x 40 bins
        l1b_de = set_pointing_bin(l1b_de, spin_phase)
        # find the closet end acquisition time to each direct event
        closest_stop_acq = find_closest_stop_acq_to_de_pkt_time(l1a_de, acq_end)
        # set the spin cycle for each direct event
        l1b_de = set_spin_cylce(l1a_de, l1b_de)
        # calculate the TOF1 for golden triples
        # store in the l1a dataset to use in l1b calculations
        l1a_de = calculate_tof1_for_golden_triples(l1a_de)
        # set the coincidence type string for each direct event
        set_coincidence_type(l1a_de, l1b_de, attr_mgr_l1a, attr_mgr_l1b)
        # convert the TOFs to engineering units
        l1b_de = convert_tofs_to_eu(l1a_de, l1b_de, attr_mgr_l1a, attr_mgr_l1b)
        # set the species for each direct event
        l1b_de = set_species(l1a_de, l1b_de, attr_mgr_l1b)
        # TODO: set the direction for each direct event

    return [l1b_de]


def convert_start_end_times(spin_data: xr.Dataset) -> tuple[xr.DataArray, xr.DataArray]:
    # Convert subseconds from microseconds to seconds
    acq_start = spin_data["acq_start_sec"] + spin_data["acq_start_subsec"] * 1e-6
    acq_end = spin_data["acq_end_sec"] + spin_data["acq_end_subsec"] * 1e-6
    return (acq_start, acq_end)


def get_avg_spin_durations(
    acq_start: xr.DataArray, acq_end: xr.DataArray
) -> xr.DataArray:
    # Get the avg spin duration for each spin epoch
    avg_spin_durations = (acq_end - acq_start) / 28
    return avg_spin_durations


def get_spin_phase(
    l1a_de_data: xr.Dataset, avg_spin_durations: xr.DataArray
) -> np.array:
    counts = l1a_de_data["de_count"]
    de_time_asc_groups = np.split(l1a_de_data["de_time"].values, np.cumsum(counts)[:-1])
    print("average de time", np.average(l1a_de_data["de_time"].values))
    print("std de time", np.std(l1a_de_data["de_time"].values))
    print("min de time", np.min(l1a_de_data["de_time"].values))
    print("max de time", np.max(l1a_de_data["de_time"].values))
    print("de_time_asc_groups", de_time_asc_groups)
    spin_phase = []
    for i, groups in enumerate(de_time_asc_groups):
        print("groups", groups)
        print("avg_spin_durations", avg_spin_durations[i])
        print(
            "spin phase",
            np.array(groups) / np.array(avg_spin_durations[i].values) * 360,
        )

        spin_phase.extend(groups / avg_spin_durations[i].values * 360)

    return np.array(spin_phase)


def set_spin_bin(l1b_de: xr.Dataset, spin_phase: np.array) -> xr.Dataset:
    # Get the spin bin for each DE
    spin_bin = (spin_phase // 6).astype(int)
    l1b_de["spin_bin"] = xr.DataArray(
        spin_bin,
        dims=["direct_event"],
        # TODO: Add spin phase to YAML file
        # attrs=attr_mgr.get_variable_attributes("spin_bin"),
    )
    return l1b_de


def set_pointing_bin(l1b_de: xr.Dataset, spin_phase: np.array) -> xr.Dataset:
    # TODO: Need to add on the 40 bins in the 2nd dimension
    # Get the pointing bin for each DE
    pointing_bin = (spin_phase // 0.1).astype(int)
    l1b_de["pointing_bin"] = xr.DataArray(
        pointing_bin,
        dims=["direct_event"],
        # TODO: Add spin phase to YAML file
        # attrs=attr_mgr.get_variable_attributes("pointing_bin"),
    )
    return l1b_de


def find_closest_stop_acq_to_de_pkt_time(
    l1a_de: xr.DataArray, acq_end: xr.DataArray
) -> xr.DataArray:
    shcoarse = l1a_de["shcoarse"].values
    # Find the closest stop_acq for each shcoarse
    closest_stop_acq_indices = np.abs(shcoarse[:, None] - acq_end.values).argmin(axis=1)
    closest_stop_acq = acq_end[closest_stop_acq_indices]
    return closest_stop_acq


def set_spin_cylce(l1a_de: xr.Dataset, l1b_de: xr.Dataset) -> xr.Dataset:
    counts = l1a_de["de_count"]
    de_asc_groups = np.split(l1a_de["esa_step"].values, np.cumsum(counts)[:-1])
    spin_cycle = []
    for i, groups in enumerate(de_asc_groups):
        # TODO: Spin Number does not reset for each pointing. Need to figure out
        #  how to retain this information across days
        spin_start = np.arange(i * 28, len(groups))
        spin_cycle.extend(spin_start + 7 + (groups - 1) * 2)

    l1b_de["spin_cycle"] = xr.DataArray(
        spin_cycle,
        dims=["direct_event"],
        # TODO: Add spin cycle to YAML file
        # attrs=attr_mgr.get_variable_attributes("spin_cycle"),
    )

    return l1b_de


def calculate_tof1_for_golden_triples(l1a_de: xr.Dataset) -> xr.Dataset:
    print("l1a_de coincidence type", l1a_de["coincidence_type"])
    for idx, coin_type in enumerate(l1a_de["coincidence_type"].values):
        if coin_type == 0 and l1a_de["mode"][idx] == 0:
            # Calculate TOF1
            tof0 = l1a_de["tof0"][idx]
            tof2 = l1a_de["tof2"][idx]
            tof3 = l1a_de["tof3"][idx]
            cksm = l1a_de["cksm"][idx]
            # TODO: will get left ckecksum boundary from LUT table when available
            left_cksm_bound = 21
            l1a_de["tof1"][idx] = tof0 + tof3 - tof2 - cksm - left_cksm_bound
    return l1a_de


def set_coincidence_type(
    l1a_de: xr.Dataset,
    l1b_de: xr.Dataset,
    attr_mgr_l1a: ImapCdfAttributes,
    attr_mgr_l1b: ImapCdfAttributes,
):
    tof0_fill = attr_mgr_l1a.get_variable_attributes("tof0")["FILLVAL"]
    tof0_mask = l1a_de["tof0"] != tof0_fill
    tof1_fill = attr_mgr_l1a.get_variable_attributes("tof1")["FILLVAL"]
    tof1_mask = l1a_de["tof1"] != tof1_fill
    tof2_fill = attr_mgr_l1a.get_variable_attributes("tof2")["FILLVAL"]
    tof2_mask = l1a_de["tof2"] != tof2_fill
    tof3_fill = attr_mgr_l1a.get_variable_attributes("tof3")["FILLVAL"]
    tof3_mask = l1a_de["tof3"] != tof3_fill
    cksm_fill = attr_mgr_l1a.get_variable_attributes("cksm")["FILLVAL"]
    cksm_mask = l1a_de["cksm"] != cksm_fill

    coincidence_type = [
        f"{tof0_mask[i]}{tof1_mask[i]}{tof2_mask[i]}{tof3_mask[i]}{cksm_mask[i]}{l1a_de['mode'][i]}"
        for i in range(l1a_de["de_count"].values.sum())
    ]

    l1b_de["coincidence_type"] = xr.DataArray(
        coincidence_type,
        dims=["direct_event"],
        # TODO: Add coincidence_type to YAML file
        # attrs=attr_mgr.get_variable_attributes("spin_cycle"),
    )

    return l1b_de


def convert_tofs_to_eu(
    l1a_de: xr.Dataset,
    l1b_de: xr.Dataset,
    attr_mgr_l1a: ImapCdfAttributes,
    attr_mgr_l1b: ImapCdfAttributes,
):
    tof_fields = ["tof0", "tof1", "tof2", "tof3"]
    tof_conversions = [TOF0_CONV, TOF1_CONV, TOF2_CONV, TOF3_CONV]

    for tof, conv in zip(tof_fields, tof_conversions):
        # Get the fill value for the L1A and L1B TOF
        fillval_1a = attr_mgr_l1a.get_variable_attributes(tof)["FILLVAL"]
        fillval_1b = attr_mgr_l1b.get_variable_attributes(tof)["FILLVAL"]
        # Create a mask for the TOF
        mask = l1a_de[tof] != fillval_1a
        # convert the DE TOF to engineering units
        tof_eu = np.where(
            mask,
            conv.C0 + 2 * conv.C1 * l1a_de[tof],
            fillval_1b,
        )
        # Add the EU TOF to the dataset
        l1b_de[tof] = xr.DataArray(
            tof_eu,
            dims=["epoch"],
            attrs=attr_mgr_l1b.get_variable_attributes(tof),
        )

    return l1b_de


def set_species(
    l1a_de: xr.Dataset, l1b_de: xr.Dataset, attr_mgr_l1b: ImapCdfAttributes
):
    # Get the species identification for each DE
    # read in species identification tables
    # select from U_PAC options

    # TODO: U_PAC value should come from instrument status summary from NHK (PAC_VSET)
    # Define the ranges
    # TODO: this will be from an ancillary file when available
    range_H1_TOF2_U_PAC_7 = (13, 40)
    range_H2_TOF0S_U_PAC_7 = (30, 70)
    range_O1_TOF2_UPAC_7 = (75, 200)
    range_O2_TOF0S_UPAC_7 = (150, 300)

    # Initialize the species array with U for Unknown
    species = np.full(l1a_de["de_count"].values.sum(), "U")

    tof0 = l1a_de["tof0"]
    tof2 = l1a_de["tof2"]
    tof3 = l1a_de["tof3"]
    tof0s = tof0 + tof3 / 2
    # Check for range Hydrogen
    mask_H = (
        (tof2 >= range_H1_TOF2_U_PAC_7[0]) & (tof2 <= range_H1_TOF2_U_PAC_7[1])
    ) | ((tof0s >= range_H2_TOF0S_U_PAC_7[0]) & (tof0s <= range_H2_TOF0S_U_PAC_7[1]))
    species[mask_H] = "H"

    # Check for range Oxygen
    mask_O = ((tof2 >= range_O1_TOF2_UPAC_7[0]) & (tof2 <= range_O1_TOF2_UPAC_7[1])) | (
        (tof0s >= range_O2_TOF0S_UPAC_7[0]) & (tof0s <= range_O2_TOF0S_UPAC_7[1])
    )
    species[mask_O] = "O"

    # Add species to the dataset
    l1b_de["species"] = xr.DataArray(
        species,
        dims=["epoch"],
        # TODO: Add to yaml
        # attrs=attr_mgr.get_variable_attributes("species"),
    )

    return l1b_de


def set_bad_times(
    l1a_de: xr.Dataset, l1b_de: xr.Dataset, attr_mgr_l1b: ImapCdfAttributes
):
    # Initialize all times as not bad for now
    # 1 = badtime, 0 = not badtime
    l1b_de["badtimes"] = xr.DataArray(
        np.zeros(l1a_de["de_count"].sum()),
        dims=["epoch"],
        # TODO: Add to yaml
        # attrs=attr_mgr.get_variable_attributes("bad_times"),
    )

    return l1b_de


def create_datasets(
    attr_mgr: ImapCdfAttributes,
    logical_source: str,
    data_fields: list[Field],
) -> xr.Dataset:
    """
    Create a dataset using the populated data classes.

    Parameters
    ----------
    attr_mgr : ImapCdfAttributes
        Attribute manager used to get the data product field's attributes.
    logical_source : str
        The logical source of the data product that's being created.
    data_fields : list[dataclasses.Field]
        List of Fields for data classes.

    Returns
    -------
    dataset : xarray.Dataset
        Dataset with all data product fields in xr.DataArray.
    """
    # TODO: Once L1B DE processing is implemented using the spin packet
    #  and relative L1A DE time to calculate the absolute DE time,
    #  this epoch conversion will go away and the time in the DE dataclass
    #  can be used direction
    epoch_converted_time = met_to_ttj2000ns([0, 1, 2])

    # Create a data array for the epoch time
    # TODO: might need to update the attrs to use new YAML file
    epoch_time = xr.DataArray(
        data=epoch_converted_time,
        name="epoch",
        dims=["epoch"],
        attrs=attr_mgr.get_variable_attributes("epoch"),
    )

    if logical_source == "imap_lo_l1b_de":
        direction_vec = xr.DataArray(
            data=[0, 1, 2],
            name="direction_vec",
            dims=["direction_vec"],
            attrs=attr_mgr.get_variable_attributes("direction_vec"),
        )

        direction_vec_label = xr.DataArray(
            data=direction_vec.values.astype(str),
            name="direction_vec_label",
            dims=["direction_vec_label"],
            attrs=attr_mgr.get_variable_attributes("direction_vec_label"),
        )

        dataset = xr.Dataset(
            coords={
                "epoch": epoch_time,
                "direction_vec": direction_vec,
                "direction_vec_label": direction_vec_label,
            },
            attrs=attr_mgr.get_global_attributes(logical_source),
        )

    # Loop through the data fields that were pulled from the
    # data class. These should match the field names given
    # to each field in the YAML attribute file
    for data_field in data_fields:
        field = data_field.name.lower()
        # Create a list of all the dimensions using the DEPEND_I keys in the
        # YAML attributes
        dims = [
            value
            for key, value in attr_mgr.get_variable_attributes(field).items()
            if "DEPEND" in key
        ]

        # Create a data array for the current field and add it to the dataset
        # TODO: TEMPORARY. need to update to use l1a data once that's available.
        #  Won't need to check for the direction field when I have sample data either.
        if field == "direction":
            dataset[field] = xr.DataArray(
                [[0, 0, 1], [0, 1, 0], [0, 0, 1]],
                dims=dims,
                attrs=attr_mgr.get_variable_attributes(field),
            )
        # TODO: This is temporary.
        #  The data type will be set in the data class when that's created
        elif field in ["tof0", "tof1", "tof2", "tof3"]:
            dataset[field] = xr.DataArray(
                [np.float16(1), np.float16(1), np.float16(1)],
                dims=dims,
                attrs=attr_mgr.get_variable_attributes(field),
            )
        else:
            dataset[field] = xr.DataArray(
                [1, 1, 1], dims=dims, attrs=attr_mgr.get_variable_attributes(field)
            )

    return dataset
