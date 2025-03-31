import unittest
from BaseKit import *

class TestTransform(unittest.TestCase):
    def test_integer_conversion(self):
        self.assertEqual(rebase("1011_2", to_base=10), "11_10")
        self.assertEqual(rebase("FF_16", to_base=2), "11111111_2")
        self.assertEqual(rebase("1A_16", to_base=10), "26_10")
        self.assertEqual(rebase("10_8", to_base=10), "8_10")
    
    def test_fractional_conversion(self):
        self.assertEqual(rebase("3.14_10", to_base=16), "3.23D7_16")
        self.assertEqual(rebase("A.8_16", to_base=10), "10.5_10")
        self.assertEqual(rebase("0.5_10", to_base=2), "0.1_2")
    
    def test_edge_cases(self):
        self.assertEqual(rebase("0_10", to_base=2), "0_2")
        self.assertEqual(rebase("1_10", to_base=36), "1_36")
        self.assertEqual(rebase("Z_36", to_base=10), "35_10")
    
    def test_error_handling(self):
        with self.assertRaises(Error.BelongingToBase):
            rebase("3.14_10", to_base=37)

        with self.assertRaises(Error.BelongingFromBase):
            rebase("3.14_37")

        with self.assertRaises(Error.DigitInvalidForBase):
            rebase("G_16")

        with self.assertRaises(Error.BaseIntError):
            rebase("10_G")

        with self.assertRaises(Error.NoBaseGiven):
            rebase("10",from_base="")

        with self.assertRaises(Error.BelongingAlphabet):
            rebase("3.1#_10", to_base=20)


class TestCalac(unittest.TestCase):
    def test_basic_operations(self):
        self.assertEqual(eval2dec("10_2 + A_16"), "12_10")  # Исправлено: 2 + 10 = 12
        self.assertEqual(eval2dec("(10_8 + 20_16) / 2_10"), "20.0_10")  # Исправлено: (8 + 32) / 2 = 20
        self.assertEqual(eval2dec("3_10 * 5_10"), "15_10")
        self.assertEqual(eval2dec("FF_16 - 10_10"), "245_10")
    
    def test_advanced_operations(self):
        self.assertEqual(eval2dec("(10_10 + 10_10) * 2_10"), "40_10")
        self.assertEqual(eval2dec("2_10 ^ 4_10"), "16_10")
        self.assertEqual(eval2dec("10_2 * 3_16 / 2_10"), "3.0_10")  # Исправлено: 2 * 3 / 2 = 3
    
    def test_fractional_results(self):
        self.assertEqual(eval2dec("1.5_10 * 2_10"), "3.0_10")
        self.assertEqual(eval2dec("A_16 / 2_10"), "5.0_10")
        self.assertEqual(eval2dec("3_10 / 2_10"), "1.5_10")
    
    def test_error_propagation(self):
        with self.assertRaises(Exception):
            eval2dec("10_2 + G_16")

if __name__ == "__main__":
    unittest.main(verbosity=2)
