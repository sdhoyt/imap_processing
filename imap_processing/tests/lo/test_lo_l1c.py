from collections import namedtuple

import numpy as np
import pytest
import xarray as xr

from imap_processing.cdf.imap_cdf_manager import ImapCdfAttributes
from imap_processing.lo.l1c.lo_l1c import (
    calculate_exposure_times,
    create_datasets,
    create_pset_counts,
    create_pset_flux,
    create_pset_rates,
    filter_goodtimes,
    initialize_pset,
    lo_l1c,
    set_spin_nums,
)


@pytest.fixture
def l1b_de():
    l1b_de = xr.Dataset(
        {
            "pointing_bin_lon": ("epoch", [20, 0, 20, 2000, 3500]),
            "pointing_bin_lat": ("epoch", [20, 20, 20, 20, 20]),
            "esa_step": ("epoch", [1, 2, 1, 4, 5]),
            "coincidence_type": (
                "epoch",
                [
                    "111111",
                    "111100",
                    "111000",
                    "110100",
                    "110000",
                ],
            ),
            "species": ("epoch", ["h", "o", "h", "h", "o"]),
            "spin_cycle": ("epoch", [1, 2, 3, 4, 5]),
            "avg_spin_durations": ("epoch", [15.2, 15.2, 14.9, 15, 14.9]),
            "badtimes": ("epoch", [0, 0, 0, 0, 0]),
        },
        coords={
            "epoch": [
                7.9794907049e17,
                7.9794907153e17,
                7.9794907254e17,
                7.9794907354e17,
                7.9794907454e17,
            ],
        },
    )
    return l1b_de


@pytest.fixture
def attr_mgr():
    attr_mgr_l1b = ImapCdfAttributes()
    attr_mgr_l1b.add_instrument_global_attrs(instrument="lo")
    attr_mgr_l1b.add_instrument_variable_attrs(instrument="lo", level="l1c")
    return attr_mgr_l1b


@pytest.fixture
def counts():
    """Fixture for initial counts."""
    return np.zeros((1, 3600, 40, 7))


@pytest.fixture
def h_counts(counts):
    h = counts.copy()
    h[0, 20, 20, 1] = 2
    h[0, 2000, 20, 4] = 1
    return h


@pytest.fixture
def o_counts(counts):
    o = counts.copy()
    o[0, 3500, 20, 5] = 1
    o[0, 0, 20, 2] = 1
    return o


@pytest.fixture
def triples_counts(counts):
    triples = counts.copy()
    triples[0, 20, 20, 1] = 2
    triples[0, 0, 20, 2] = 1
    return triples


@pytest.fixture
def doubles_counts(counts):
    doubles = counts.copy()
    doubles[0, 2000, 20, 4] = 1
    doubles[0, 3500, 20, 5] = 1
    return doubles


def test_lo_l1c(l1b_de):
    # Arrange
    data = {"imap_lo_l1b_de": l1b_de}

    expected_logical_source = "imap_lo_l1c_pset"
    # Act
    output_dataset = lo_l1c(data)

    # Assert
    assert expected_logical_source == output_dataset[0].attrs["Logical_source"]


def test_filter_goodtimes(l1b_de):
    # Arrange
    l1b_de_with_badtimes = xr.Dataset(
        {
            "pointing_bin_lon": ("epoch", [20, 0, 20, 2000, 3500, 200]),
            "pointing_bin_lat": ("epoch", [20, 20, 20, 20, 20, 40]),
            "esa_step": ("epoch", [1, 2, 1, 4, 5, 2]),
            "coincidence_type": (
                "epoch",
                ["111111", "111100", "111000", "110100", "110000", "000000"],
            ),
            "species": ("epoch", ["h", "o", "h", "h", "o", "u"]),
            "spin_cycle": ("epoch", [1, 2, 3, 4, 5, 12]),
            "avg_spin_durations": ("epoch", [15.2, 15.2, 14.9, 15, 14.9, 50]),
            "badtimes": ("epoch", [0, 0, 0, 0, 0, 1]),
        },
        coords={
            "epoch": [
                7.9794907049e17,
                7.9794907153e17,
                7.9794907254e17,
                7.9794907354e17,
                7.9794907454e17,
                7.9794907455e17,
            ],
        },
    )
    l1b_de_no_badtimes_expected = l1b_de.copy()

    # Act
    l1b_no_badtimes = filter_goodtimes(l1b_de)

    # Assert
    xr.testing.assert_equal(l1b_no_badtimes, l1b_de_no_badtimes_expected)


def test_set_spin_nums(l1b_de):
    # Arrange
    expected_start_spin_num = 1
    expected_end_spin_num = 5
    # Act
    start_spin_num, end_spin_num = set_spin_nums(l1b_de)

    # Assert
    np.testing.assert_array_equal(start_spin_num, expected_start_spin_num)
    np.testing.assert_array_equal(end_spin_num, expected_end_spin_num)


def test_intialize_pset(l1b_de, attr_mgr):
    # Act
    pset = initialize_pset(l1b_de, attr_mgr, "imap_lo_l1c_pset")
    expected_epoch = np.array(7.9794907254e17)

    # Assert
    np.testing.assert_array_equal(pset["epoch"], expected_epoch)


def test_create_pset_counts(l1b_de):
    # Arrange
    expected_counts = np.zeros((1, 3600, 40, 7))
    expected_counts[0, 20, 20, 1] = 2
    expected_counts[0, 2000, 20, 4] = 1
    expected_counts[0, 3500, 20, 5] = 1
    expected_counts[0, 0, 20, 2] = 1

    # Act
    counts = create_pset_counts(l1b_de)

    # Assert
    np.testing.assert_array_equal(counts, expected_counts)


def test_create_h_pset_counts(l1b_de, h_counts):
    # Act
    counts = create_pset_counts(l1b_de, "h")

    # Assert
    np.testing.assert_array_equal(counts, h_counts)


def test_create_o_pset_counts(l1b_de, o_counts):
    # Act
    counts = create_pset_counts(l1b_de, "o")

    # Assert
    np.testing.assert_array_equal(counts, o_counts)


def test_create_triples_pset_counts(l1b_de, triples_counts):
    # Act
    counts = create_pset_counts(l1b_de, "triples")

    # Assert
    np.testing.assert_array_equal(counts, triples_counts)


def test_create_doubles_pset_counts(l1b_de, doubles_counts):
    # Act
    counts = create_pset_counts(l1b_de, "doubles")

    # Assert
    np.testing.assert_array_equal(counts, doubles_counts)


def test_calculate_exposure_times(l1b_de):
    # Arrange
    counts = create_pset_counts(l1b_de)
    expected_exposure_times = np.full((1, 3600, 40, 7), np.nan)
    # Average of the exposure times for each bin
    expected_exposure_times[0, 20, 20, 1] = np.mean([15.2, 14.9])
    expected_exposure_times[0, 2000, 20, 4] = 15
    expected_exposure_times[0, 3500, 20, 5] = 14.9
    expected_exposure_times[0, 0, 20, 2] = 15.2
    # Act
    exposure_times = calculate_exposure_times(counts, l1b_de)

    # Assert
    np.testing.assert_allclose(
        exposure_times,
        expected_exposure_times,
        atol=1e-2,
    )


def test_create_pset_rates(h_counts):
    # Arrange
    exposure_time = np.full((1, 3600, 40, 7), np.nan)
    exposure_time[0, 20, 20, 1] = 20
    exposure_time[0, 2000, 20, 4] = 15
    h_counts = xr.DataArray(h_counts)
    exposure_time = xr.DataArray(exposure_time)

    rates_expected = np.full((1, 3600, 40, 7), np.nan)
    # count / exposure_time for each bin
    rates_expected[0, 20, 20, 1] = 2 / 20
    rates_expected[0, 2000, 20, 4] = 1 / 15

    # Act
    rates = create_pset_rates(h_counts, exposure_time)

    # Assert
    np.testing.assert_allclose(
        rates,
        rates_expected,
        atol=1e-2,
    )


def test_create_pset_flux():
    # Arrange
    rate = np.full((1, 3600, 40, 7), np.nan)
    rate[0, 20, 20, 1] = 0.1
    rate[0, 2000, 20, 4] = 0.2

    expected_flux = np.full((1, 3600, 40, 7), np.nan)
    # rate / (geometric_factor * energy * efficiency_factor)
    # Ancillary tables are not yet available, so they are hardcoded as follows:
    # geometric_factor = 1.0
    # energy = same value as the ESA_step associated with that energy
    # efficiency_factor = 1.0
    expected_flux[0, 20, 20, 1] = 0.1 / (1.0 * 2.0 * 1.0)
    expected_flux[0, 2000, 20, 4] = 0.2 / (1.0 * 5.0 * 1.0)

    # Act
    flux = create_pset_flux(rate)

    # Assert
    np.testing.assert_allclose(
        flux,
        expected_flux,
        atol=1e-2,
    )


def test_create_dataset():
    attr_mgr = ImapCdfAttributes()
    attr_mgr.add_instrument_global_attrs(instrument="lo")
    attr_mgr.add_instrument_variable_attrs(instrument="lo", level="l1c")

    logical_source = "imap_lo_l1c_pset"

    data_field_tup = namedtuple("data_field_tup", ["name"])
    data_fields = [
        data_field_tup("POINTING_START"),
        data_field_tup("POINTING_END"),
        data_field_tup("MODE"),
        data_field_tup("PIVOT_ANGLE"),
        data_field_tup("TRIPLES_COUNTS"),
        data_field_tup("TRIPLES_RATES"),
        data_field_tup("DOUBLES_COUNTS"),
        data_field_tup("DOUBLES_RATES"),
        data_field_tup("HYDROGEN_COUNTS"),
        data_field_tup("HYDROGEN_RATES"),
        data_field_tup("OXYGEN_COUNTS"),
        data_field_tup("OXYGEN_RATES"),
        data_field_tup("EXPOSURE_TIME"),
    ]

    dataset = create_datasets(attr_mgr, logical_source, data_fields)

    np.testing.assert_array_equal(dataset.pointing_start, np.ones(1))
    np.testing.assert_array_equal(dataset.pointing_end, np.ones(1))
    np.testing.assert_array_equal(dataset.mode, np.ones(1))
    np.testing.assert_array_equal(dataset.pivot_angle, np.ones(1))
    np.testing.assert_array_equal(dataset.triples_counts, np.ones((1, 3600, 7)))
    np.testing.assert_array_equal(dataset.triples_rates, np.ones((1, 3600, 7)))
    np.testing.assert_array_equal(dataset.doubles_counts, np.ones((1, 3600, 7)))
    np.testing.assert_array_equal(dataset.doubles_rates, np.ones((1, 3600, 7)))
    np.testing.assert_array_equal(dataset.hydrogen_counts, np.ones((1, 3600, 7)))
    np.testing.assert_array_equal(dataset.hydrogen_rates, np.ones((1, 3600, 7)))
    np.testing.assert_array_equal(dataset.oxygen_counts, np.ones((1, 3600, 7)))
    np.testing.assert_array_equal(dataset.oxygen_rates, np.ones((1, 3600, 7)))
    np.testing.assert_array_equal(dataset.exposure_time, np.ones((1, 7)))
