"Tests bins for pointing sets"

import numpy as np
import pytest

from imap_processing import imap_module_directory
from imap_processing.ultra.l1c.ultra_l1c_pset_bins import (
    build_energy_bins,
    build_spatial_bins,
    cartesian_to_spherical,
    get_histogram,
    get_pointing_frame_exposure_times,
)

BASE_PATH = imap_module_directory / "ultra" / "lookup_tables"


@pytest.fixture()
def test_data():
    """Test data fixture."""
    vx_sc = np.array([-186.5575, 508.5697, 508.5697, 508.5697])
    vy_sc = np.array([-707.5707, -516.0282, -516.0282, -516.0282])
    vz_sc = np.array([618.0569, 892.6931, 892.6931, 892.6931])
    energy = np.array([3.384, 3.385, 200, 200])
    v = np.column_stack((vx_sc, vy_sc, vz_sc))

    return v, energy


def test_build_energy_bins():
    """Tests build_energy_bins function."""
    energy_bin_edges = build_energy_bins()
    energy_bin_start = energy_bin_edges[:-1]
    energy_bin_end = energy_bin_edges[1:]

    assert energy_bin_start[0] == 0
    assert energy_bin_start[1] == 3.385
    assert len(energy_bin_edges) == 25

    # Comparison to expected values.
    np.testing.assert_allclose(energy_bin_end[1], 4.137, atol=1e-4)
    np.testing.assert_allclose(energy_bin_start[-1], 279.810, atol=1e-4)
    np.testing.assert_allclose(energy_bin_end[-1], 341.989, atol=1e-4)


def test_build_spatial_bins():
    """Tests build_spatial_bins function."""
    az_bin_edges, el_bin_edges, az_bin_midpoints, el_bin_midpoints = (
        build_spatial_bins()
    )

    assert az_bin_edges[0] == 0
    assert az_bin_edges[-1] == 360
    assert len(az_bin_edges) == 721

    assert el_bin_edges[0] == -90
    assert el_bin_edges[-1] == 90
    assert len(el_bin_edges) == 361

    assert len(az_bin_midpoints) == 720
    np.testing.assert_allclose(az_bin_midpoints[0], 0.25, atol=1e-4)
    np.testing.assert_allclose(az_bin_midpoints[-1], 359.75, atol=1e-4)

    assert len(el_bin_midpoints) == 360
    np.testing.assert_allclose(el_bin_midpoints[0], -89.75, atol=1e-4)
    np.testing.assert_allclose(el_bin_midpoints[-1], 89.75, atol=1e-4)


def test_cartesian_to_spherical(test_data):
    """Tests cartesian_to_spherical function."""
    v, _ = test_data

    az_sc, el_sc, r = cartesian_to_spherical(v)

    # MATLAB code outputs:
    np.testing.assert_allclose(
        np.unique(np.radians(az_sc)), np.array([1.31300, 2.34891]), atol=1e-05, rtol=0
    )
    np.testing.assert_allclose(
        np.unique(np.radians(el_sc)), np.array([-0.88901, -0.70136]), atol=1e-05, rtol=0
    )


def test_get_histogram(test_data):
    """Tests get_histogram function."""
    v, energy = test_data

    az_bin_edges, el_bin_edges, az_bin_midpoints, el_bin_midpoints = (
        build_spatial_bins()
    )
    energy_bin_edges = build_energy_bins()

    hist = get_histogram(v, energy, az_bin_edges, el_bin_edges, energy_bin_edges)

    assert hist.shape == (
        len(az_bin_edges) - 1,
        len(el_bin_edges) - 1,
        len(energy_bin_edges) - 1,
    )


def test_get_pointing_frame_exposure_times():
    """Tests get_pointing_frame_exposure_times function."""

    constant_exposure = BASE_PATH / "dps_grid45_compressed.cdf"
    spins_per_pointing = 5760
    exposure = get_pointing_frame_exposure_times(
        constant_exposure, spins_per_pointing, "45"
    )

    assert exposure.shape == (720, 360)
    # Assert that the exposure time at the highest azimuth is
    # 15s x spins per pointing.
    assert np.array_equal(
        exposure[:, 359], np.full_like(exposure[:, 359], spins_per_pointing * 15)
    )
    # Assert that the exposure time at the lowest azimuth is 0 (no exposure).
    assert np.array_equal(exposure[:, 0], np.full_like(exposure[:, 359], 0.0))
