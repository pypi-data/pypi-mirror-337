import unittest

from tests.constants import *

offline = True


class TestNightly(unittest.TestCase):
    """
    These tests are not meant to work! Purely for new trying out new functionality.
    """
    def setUp(self):
        self.hplc_controller = set_up_utils(242)

    def test_load_inj(self):
        try:
            inj_table = self.hplc_controller.load_injector_program()
            self.assertTrue(len(inj_table.functions) == 2)
        except Exception as e:
            self.fail(f"Should have not failed, {e}")


if __name__ == '__main__':
    unittest.main()
