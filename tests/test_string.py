from unittest import TestCase

from aocutils.string import hex2bin


class Test(TestCase):
    def test_hex2bin(self):
        values = [
            ('D2FE28', '110100101111111000101000'),
            ('38006F45291200', '00111000000000000110111101000101001010010001001000000000')
        ]

        for input_value, expected_value in values:
            self.assertEqual(expected_value, hex2bin(input_value))
