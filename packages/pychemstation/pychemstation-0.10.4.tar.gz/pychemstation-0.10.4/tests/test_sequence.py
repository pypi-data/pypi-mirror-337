import unittest

from tests.constants import (
    clean_up,
    set_up_utils,
)


class TestSequence(unittest.TestCase):
    """
    These tests should always work with an online controller.
    """

    def setUp(self):
        self.hplc_controller = set_up_utils(242, offline=False, runs=False)

    def tearDown(self):
        clean_up(self.hplc_controller)


if __name__ == "__main__":
    unittest.main()
