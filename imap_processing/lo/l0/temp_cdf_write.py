from imap_processing import decom
from imap_processing.lo import __version__
from imap_processing.lo.l0.utils.lo_l0_container import LoL0Container
from imap_processing.lo.l0.utils.loApid import LoAPID
import imap_processing.lo.l0.lo_cdf_attrs as lo_cdf_attrs
from imap_processing.cdf.utils import write_cdf
import xarray as xr
from pathlib import Path

# TODO: Confirm whether count is needed. I don't know that this is
# necessary to save
sci_de_count = xr.DataArray(
    name="count",
    data=[0, 0, 0],
    attrs=lo_cdf_attrs.lo_tof_attrs.output()
)
sci_de_checksum = xr.DataArray(
    name="checksum", data=[0, 0, 0],
    attrs=lo_cdf_attrs.lo_tof_attrs.output()
)
sci_de_tof0 = xr.DataArray(
    name="tof0", data=[0, 0, 0],
    attrs=lo_cdf_attrs.lo_tof_attrs.output()
)
sci_de_tof1 = xr.DataArray(
    name="tof1", data=[0, 0, 0],
    attrs=lo_cdf_attrs.lo_tof_attrs.output()
)
sci_de_tof2 = xr.DataArray(
    name="tof2", data=[0, 0, 0],
    attrs=lo_cdf_attrs.lo_tof_attrs.output()
)
sci_de_tof3 = xr.DataArray(
    name="tof3", data=[0, 0, 0],
    attrs=lo_cdf_attrs.lo_tof_attrs.output()
)
sci_de_energy = xr.DataArray(
    name="energy", data=[0, 0, 0],
    attrs=lo_cdf_attrs.lo_tof_attrs.output()
)
sci_de_pos = xr.DataArray(
    name="pos", data=[0, 0, 0],
    attrs=lo_cdf_attrs.lo_tof_attrs.output()
)
sci_de_time = xr.DataArray(
    name='time', data=[0, 0, 0],
    attrs=lo_cdf_attrs.lo_tof_attrs.output()
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
        "time": sci_de_time
    },
    attrs=lo_cdf_attrs.lo_l1a_global_attrs.output(),
    #TODO: figure out how to convert time data to epoch
    coords={"epoch": sci_de_time}
)
# Maybe I need to set the Depend_0 thing and set it to epoch to get the
# time variable to work?

print(sci_de_dataset["tof0"].attrs)

write_cdf(sci_de_time, Path())