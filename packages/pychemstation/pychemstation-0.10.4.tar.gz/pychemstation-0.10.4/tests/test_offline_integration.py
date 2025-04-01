import unittest

from pychemstation.analysis.process_report import ReportType
from pychemstation.utils.sequence_types import SequenceDataFiles
from pychemstation.utils.tray_types import FiftyFourVialPlate
from tests.constants import DEFAULT_SEQUENCE, VIAL_PLATES, clean_up, set_up_utils


class TestStable(unittest.TestCase):
    """
    These tests should always work, while the controller is offline or online.
    """

    def setUp(self):
        self.hplc_controller = set_up_utils(242, offline=True)

    def tearDown(self):
        clean_up(self.hplc_controller)

    def test_tray_nums_only(self):
        for i in range(len(VIAL_PLATES)):
            self.assertEqual(
                VIAL_PLATES[i], FiftyFourVialPlate.from_int(VIAL_PLATES[i].value())
            )

    def test_get_last_run_sequence(self):
        path = "hplc_testing 2025-03-27 17-13-47"
        self.hplc_controller.sequence_controller.data_files.append(
            SequenceDataFiles(dir=path, sequence_name=DEFAULT_SEQUENCE)
        )
        try:
            most_recent_folder = self.hplc_controller.sequence_controller.data_files[-1]
            check_folder = (
                self.hplc_controller.sequence_controller.fuzzy_match_most_recent_folder(
                    most_recent_folder=most_recent_folder
                )
            )
            self.assertEqual(check_folder.ok_value.dir, path)
            self.hplc_controller.sequence_controller.data_files[
                -1
            ].dir = check_folder.ok_value
            chrom = self.hplc_controller.get_last_run_sequence_data()
            self.assertTrue(chrom)
        except Exception:
            self.fail()

    def test_plate_number(self):
        self.assertEqual(FiftyFourVialPlate.from_str("P1-A1").value(), 4096)
        self.assertEqual(FiftyFourVialPlate.from_str("P1-A4").value(), 4099)

    def test_get_method_report(self):
        method_path = "0_2025-03-15 19-14-35.D"
        report = self.hplc_controller.get_last_run_method_report(
            custom_path=method_path, report_type=ReportType.CSV
        )
        self.assertEqual(report.vial_location, FiftyFourVialPlate.from_int(4096))

    def test_get_seq_report(self):
        seq_path = "hplc_testing 2025-03-27 17-13-47"
        report = self.hplc_controller.get_last_run_sequence_reports(
            custom_path=seq_path, report_type=ReportType.TXT
        )
        self.assertEqual(len(report[0].signals[0].peaks), 12)

    def test_get_method_uv(self):
        method_path = "0_2025-03-15 19-14-35.D"
        try:
            self.hplc_controller.get_last_run_method_data(
                custom_path=method_path, read_uv=True
            )
        except Exception:
            pass

    def test_get_seq_uv(self):
        seq_path = "hplc_testing 2025-03-27 17-13-47"
        try:
            self.hplc_controller.get_last_run_sequence_data(
                custom_path=seq_path, read_uv=True
            )
        except Exception:
            pass


if __name__ == "__main__":
    unittest.main()
