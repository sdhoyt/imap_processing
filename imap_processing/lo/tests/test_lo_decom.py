import pytest

from imap_processing.lo.l0 import lo_l1a_decom


@pytest.fixture(scope="session")
def decom_test_data():
    """Read test data from file"""
    # TODO: Update CCSDS with updated data (this version is out of date)
    packet_file = (
        "imap_processing/lo/tests/Instrument_EMPOKE_test_20231027T173028.CCSDS"
    )
    # This xtce is out of date but being used to test with the out of
    # date sample test data currently available
    xtce = "imap_processing/lo/packet_definitions/P_ILO_BOOT_HK.xml"
    data_packet_list = lo_l1a_decom.decom_lo_packets(packet_file, xtce)
    return data_packet_list


def test_total_datasets(decom_test_data):
    """Test if total number of datasets is correct"""
    print("ran one")
    # assert len(decom_test_data) == total_datasets


def test_dataset_dims_length(decom_test_data):
    """Test if the time dimension length in the dataset is correct"""
    # assert decom_test_data["ILO_RAW_DE"].dims["Epoch"] == num_packet_times
