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
    attr_mgr = ImapCdfAttributes()
    attr_mgr.add_instrument_global_attrs(instrument="lo")
    attr_mgr.add_instrument_variable_attrs(instrument="lo", level="l1b")
    attr_mgr.add_global_attribute("Data_version", data_version)

    # if the dependencies are used to create Annotated Direct Events

    if "imap_lo_l1a_de" in dependencies and "imap_lo_l1a_spin" in dependencies:
        logical_source = "imap_lo_l1b_de"
        print(dependencies["imap_lo_l1a_de"])
        print(dependencies["imap_lo_l1a_spin"])
        dataset = xr.Dataset(
            attrs=attr_mgr.get_global_attributes(logical_source),
        )

        spin_data = dependencies["imap_lo_l1a_spin"]

        # Get the avg spin duration for each spin epoch
        avg_spin_durations = (spin_data["stop_acq"] - spin_data["start_acq"]) / 28

        ### FIND CLOSEST STOP ACQ TO DE TIME ###
        shcoarse = dependencies["imap_lo_l1a_de"]["SHCOARSE"].values
        stop_acq = dependencies["imap_lo_l1a_spin"]["stop_acq"].values

        # Find the closest stop_acq for each shcoarse
        closest_stop_acq_indices = np.abs(shcoarse[:, None] - stop_acq).argmin(axis=1)
        closest_stop_acq = stop_acq[closest_stop_acq_indices]

        print(closest_stop_acq)
        #########################################

        ##### CONVERT EU TODO: MOVE TO FUNCTION #######################
        tof_fields = ["tof0", "tof1", "tof2", "tof3"]
        tof_conversions = [TOF0_CONV, TOF1_CONV, TOF2_CONV, TOF3_CONV]

        for tof, conv in zip(tof_fields, tof_conversions):
            # convert the DE TOF to engineering units
            tof_eu = conv.C0 + 2 * conv.C1 * dependencies["imap_lo_l1a_de"][tof]

            # Add the EU TOF to the dataset
            dataset[tof] = xr.DataArray(
                tof_eu,
                dims=["epoch"],
                attrs=attr_mgr.get_variable_attributes(tof),
            )
        #####################################

        # line up each DE SHCOARSE with the stop Acq for each spin epoch by finding the
        # closest stop acq to the DE time
        # calculate the average spin duration for each spin epoch using the following:
        #   (stop acq - start acq) / 28
        # Assign each DE to a spin number using the following:
        #   spin_cycle = spin_start_number + 7 + (ESA_step - 1) * 2

        # Set Coincidence strings

        # species identification

        # initialize badtimes

        # set spin bin

        # create pointing bin

        # set direction

    # return dataset


# TODO: This is going to work differently when I sample data.
#  The data_fields input is temporary.
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
