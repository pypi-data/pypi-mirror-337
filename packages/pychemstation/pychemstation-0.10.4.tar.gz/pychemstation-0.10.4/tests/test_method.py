import random
import unittest

from pychemstation.utils.method_types import TimeTableEntry
from tests.constants import (
    clean_up,
    set_up_utils,
    DEFAULT_METHOD,
)


class TestMethod(unittest.TestCase):
    """
    These tests should always work with an online controller.
    """

    def setUp(self):
        self.hplc_controller = set_up_utils(242, offline=False, runs=False)
        self.hplc_controller.switch_method(DEFAULT_METHOD)

    def tearDown(self):
        clean_up(self.hplc_controller)

    def test_update_method_components(self):
        new_flow = random.randint(1, 10) / 10
        self.hplc_controller.method_controller.edit_flow(new_flow=new_flow)
        new_post_time = random.randint(1, 6)
        self.hplc_controller.method_controller.edit_post_time(
            new_post_time=new_post_time
        )
        new_stop_time = random.randint(1, 20)
        self.hplc_controller.method_controller.edit_stop_time(
            new_stop_time=new_stop_time
        )
        new_om = random.randint(1, 50)
        self.hplc_controller.method_controller.edit_initial_om(new_om=new_om)
        method_details = self.hplc_controller.load_method()
        self.assertEqual(method_details.params.flow, new_flow)
        self.assertEqual(method_details.post_time, new_post_time)
        self.assertEqual(method_details.stop_time, new_stop_time)
        self.assertEqual(method_details.params.organic_modifier, new_om)

    def test_update_only_timetable(self):
        start_time_1 = random.randint(1, 10)
        starting_og = random.randint(1, 50)
        timetable_flow = random.randint(1, 10) / 10
        timetable = [
            TimeTableEntry(
                start_time=start_time_1,
                organic_modifer=starting_og,
                flow=timetable_flow,
            ),
            TimeTableEntry(
                start_time=start_time_1 + 5, organic_modifer=78, flow=1 - timetable_flow
            ),
        ]
        self.hplc_controller.method_controller.edit_method_timetable(timetable)
        method_details = self.hplc_controller.load_method()
        self.assertEqual(method_details.timetable, timetable)


if __name__ == "__main__":
    unittest.main()
