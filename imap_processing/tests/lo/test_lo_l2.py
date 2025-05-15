import pytest

from imap_processing import imap_module_directory
from imap_processing.cdf.utils import load_cdf


@pytest.fixture
def pset():
    dataset = load_cdf(
        imap_module_directory / "tests/lo/test_cdfs/imap_lo_l1c_pset_20250415_v001.cdf"
    )
    return dataset


def test_hflux_map(pset):
    print("PSET", pset)
