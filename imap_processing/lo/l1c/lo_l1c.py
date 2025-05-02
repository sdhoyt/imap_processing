"""IMAP-Lo L1C Data Processing."""

from dataclasses import Field
from pathlib import Path

import numpy as np
import xarray as xr
from scipy.stats import binned_statistic_dd

from imap_processing.cdf.imap_cdf_manager import ImapCdfAttributes
from imap_processing.spice.time import met_to_ttj2000ns


def lo_l1c(dependencies: dict) -> list[Path]:
    """
    Will process IMAP-Lo L1B data into L1C CDF data products.

    Parameters
    ----------
    dependencies : dict
        Dictionary of datasets needed for L1C data product creation in xarray Datasets.

    Returns
    -------
    created_file_paths : list[Path]
        Location of created CDF files.
    """
    # create the attribute manager for this data level
    attr_mgr = ImapCdfAttributes()
    attr_mgr.add_instrument_global_attrs(instrument="lo")
    attr_mgr.add_instrument_variable_attrs(instrument="lo", level="l1c")

    # if the dependencies are used to create Annotated Direct Events
    if "imap_lo_l1b_de" in dependencies:
        logical_source = "imap_lo_l1c_pset"
        l1b_de = dependencies["imap_lo_l1b_de"]

        l1b_goodtimes_only = filter_goodtimes(l1b_de)
        pset = initialize_pset(l1b_goodtimes_only, attr_mgr, logical_source)
        pset["start_spin_num"], pset["end_spin_num"] = set_spin_nums(l1b_goodtimes_only)
        full_counts = create_pset_counts(l1b_goodtimes_only)
        pset["triples_counts"] = create_pset_counts(l1b_goodtimes_only, "triples")
        pset["doubles_counts"] = create_pset_counts(l1b_goodtimes_only, "doubles")
        pset["h_counts"] = create_pset_counts(l1b_goodtimes_only, "h")
        pset["o_counts"] = create_pset_counts(l1b_goodtimes_only, "o")
        pset["exposure_time"] = calculate_exposure_times(
            full_counts, l1b_goodtimes_only
        )
        pset["triples_rates"] = create_pset_rates(
            pset["triples_counts"], pset["exposure_time"]
        )
        pset["doubles_rates"] = create_pset_rates(
            pset["doubles_counts"], pset["exposure_time"]
        )
        pset["h_rates"] = create_pset_rates(pset["h_counts"], pset["exposure_time"])
        pset["o_rates"] = create_pset_rates(pset["o_counts"], pset["exposure_time"])
        pset["h_flux"] = create_pset_flux(pset["h_rates"])
        pset["o_flux"] = create_pset_flux(pset["o_rates"])

        # dataset: list[Path] = create_datasets(attr_mgr, logical_source,
        #                                      data_fields)  # type: ignore[arg-type]
    return [pset]


def initialize_pset(l1b_de, attr_mgr, logical_source) -> xr.Dataset:
    """
    Initialize the PSET dataset.

    Returns
    -------
    pset : xarray.Dataset
        Initialized PSET dataset.
    """
    pset = xr.Dataset(
        attrs=attr_mgr.get_global_attributes(logical_source),
    )

    mid_idx = len(l1b_de["epoch"]) // 2
    pset_epoch = l1b_de["epoch"][mid_idx].item()
    pset["epoch"] = xr.DataArray(
        np.array([pset_epoch]),
        dims=["epoch"],
        # attrs=attr_mgr.get_variable_attributes("epoch")
    )

    return pset


def filter_goodtimes(l1b_de: xr.Dataset) -> xr.Dataset:
    # TODO: Ancilary data for goodtimes is not available yet. Removing badtimes
    #  for now. This will be updated once the ancillary data is available.
    return l1b_de.where(l1b_de["badtimes"] == 0, drop=True)


def set_spin_nums(l1b_de: xr.Dataset) -> tuple[xr.DataArray, xr.DataArray]:
    start_spin_num = xr.DataArray(
        [l1b_de["spin_cycle"][0].values],
        dims=["epoch"],
        # TODO: add start_spin_num to attributes
        # attrs=attr_mgr.get_variable_attributes("start_spin_num"),
    )
    end_spin_num = xr.DataArray(
        [l1b_de["spin_cycle"][-1].values],
        dims=["epoch"],
        # TODO: add end_spin_num to attributes
        # attrs=attr_mgr.get_variable_attributes("end_spin_num"),
    )
    return start_spin_num, end_spin_num


def create_pset_counts(de: xr.Dataset, filter: str = "") -> xr.DataArray:
    filter_options = {
        "triples": ["111111", "111100", "111000"],
        "doubles": [
            "110100",
            "110000",
            "101101",
            "101100",
            "101000",
            "100100",
            "100101",
            "100000",
            "011100",
            "011000",
            "010100",
            "010101",
            "010000",
            "001100",
            "001101",
            "001000",
        ],
        "h": "h",
        "o": "o",
    }

    if filter not in filter_options and filter != "":
        raise ValueError(f"Invalid filter option. Choose from {filter_options}")

    if filter == "triples" or filter == "doubles":
        filter_idx = np.where(np.isin(de["coincidence_type"], filter_options[filter]))[
            0
        ]
    elif filter == "h" or filter == "o":
        filter_idx = np.where(np.isin(de["species"], filter_options[filter]))[0]
    else:
        filter_idx = np.arange(len(de["epoch"]))

    de_filtered = de.isel(epoch=filter_idx)
    data = np.column_stack(
        (
            de_filtered["pointing_bin_lon"],
            de_filtered["pointing_bin_lat"],
            de_filtered["esa_step"],
        )
    )
    lon_edges = np.arange(3601)
    lat_edges = np.arange(41)
    energy_edges = np.arange(8)

    hist, edges = np.histogramdd(
        data,
        bins=[lon_edges, lat_edges, energy_edges],
    )

    # add a new axis of size 1 for the epoch
    hist = hist[np.newaxis, :, :, :]

    counts = xr.DataArray(
        data=hist.astype(np.int16),
        dims=["epoch", "lon_bins", "lat_bins", "energy_bins"],
    )

    return counts


def calculate_exposure_times(counts: xr.DataArray, l1b_de: xr.Dataset) -> xr.DataArray:
    # Create bin edges
    lon_edges = np.arange(3601)
    lat_edges = np.arange(41)
    energy_edges = np.arange(8)

    data = np.column_stack(
        (l1b_de["pointing_bin_lon"], l1b_de["pointing_bin_lat"], l1b_de["esa_step"])
    )

    result = binned_statistic_dd(
        data,
        l1b_de["avg_spin_durations"].to_numpy(),
        statistic="mean",
        bins=[lon_edges, lat_edges, energy_edges],
    )

    stat = result.statistic[np.newaxis, :, :, :]

    exposure_time = xr.DataArray(
        data=stat.astype(np.float16),
        dims=["epoch", "lon_bins", "lat_bins", "energy_bins"],
    )

    return exposure_time


def create_pset_rates(
    counts: xr.DataArray, exposure_time: xr.DataArray
) -> xr.DataArray:
    # TODO: This is going to work differently when I sample data.
    #  The data_fields input is temporary.
    rates = counts / exposure_time
    rates = xr.DataArray(
        data=rates.astype(np.float16),
        dims=["epoch", "lon_bins", "lat_bins", "energy_bins"],
    )
    return rates


def create_pset_flux(rates: xr.DataArray) -> xr.DataArray:
    # temporary values. These will all come from ancillary data when
    # the data is available.
    geometric_factor = 1.0
    efficiency_factor = 1.0
    energy_dict = {1: 1, 2: 2, 3: 3, 4: 4, 5: 5, 6: 6, 7: 7}
    energies = np.array([energy_dict[i] for i in range(1, 8)])

    energies = energies.reshape(1, 1, 7)

    flux = rates / (geometric_factor * energies * efficiency_factor)

    flux = xr.DataArray(
        data=flux.astype(np.float16),
        dims=["epoch", "lon_bins", "lat_bins", "energy_bins"],
    )

    return flux


def create_datasets(
    attr_mgr: ImapCdfAttributes, logical_source: str, data_fields: list[Field]
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
    epoch_converted_time = [met_to_ttj2000ns(1)]

    # Create a data array for the epoch time
    # TODO: might need to update the attrs to use new YAML file
    epoch_time = xr.DataArray(
        data=epoch_converted_time,
        name="epoch",
        dims=["epoch"],
        attrs=attr_mgr.get_variable_attributes("epoch"),
    )

    if logical_source == "imap_lo_l1c_pset":
        esa_step = xr.DataArray(
            data=[1, 2, 3, 4, 5, 6, 7],
            name="esa_step",
            dims=["esa_step"],
            attrs=attr_mgr.get_variable_attributes("esa_step"),
        )
        pointing_bins = xr.DataArray(
            data=np.arange(3600),
            name="pointing_bins",
            dims=["pointing_bins"],
            attrs=attr_mgr.get_variable_attributes("pointing_bins"),
        )

        esa_step_label = xr.DataArray(
            esa_step.values.astype(str),
            name="esa_step_label",
            dims=["esa_step_label"],
            attrs=attr_mgr.get_variable_attributes("esa_step_label"),
        )
        pointing_bins_label = xr.DataArray(
            pointing_bins.values.astype(str),
            name="pointing_bins_label",
            dims=["pointing_bins_label"],
            attrs=attr_mgr.get_variable_attributes("pointing_bins_label"),
        )
        dataset = xr.Dataset(
            coords={
                "epoch": epoch_time,
                "pointing_bins": pointing_bins,
                "pointing_bins_label": pointing_bins_label,
                "esa_step": esa_step,
                "esa_step_label": esa_step_label,
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
        # TODO: TEMPORARY. need to update to use l1b data once that's available.
        if field in ["pointing_start", "pointing_end", "mode", "pivot_angle"]:
            dataset[field] = xr.DataArray(
                data=[1],
                dims=dims,
                attrs=attr_mgr.get_variable_attributes(field),
            )
        # TODO: This is temporary.
        #  The data type will be set in the data class when that's created
        elif field == "exposure_time":
            dataset[field] = xr.DataArray(
                data=np.ones((1, 7), dtype=np.float16),
                dims=dims,
                attrs=attr_mgr.get_variable_attributes(field),
            )

        elif "rate" in field:
            dataset[field] = xr.DataArray(
                data=np.ones((1, 3600, 7), dtype=np.float16),
                dims=dims,
                attrs=attr_mgr.get_variable_attributes(field),
            )
        else:
            dataset[field] = xr.DataArray(
                data=np.ones((1, 3600, 7), dtype=np.int16),
                dims=dims,
                attrs=attr_mgr.get_variable_attributes(field),
            )

    return dataset
