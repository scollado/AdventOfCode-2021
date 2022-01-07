from unittest import TestCase

from day16 import LiteralPacket, Packet, OperatorPacket, SumPacket, ProductPacket, MinimumPacket, MaximumPacket, \
    LowerThanPacket, GreaterThanPacket, EqualPacket


class Test(TestCase):
    def test_read_literal_packet(self):
        input_value = 'D2FE28'
        expected_result = '011111100101'
        expected_version = 6

        result = Packet.read(input_value)
        self.assertIsInstance(result, LiteralPacket)
        self.assertEqual(expected_version, result.version())
        self.assertEqual(expected_result, str(result))

    def test_read_operator_packet_with_length_type_0(self):
        input_value = '38006F45291200'
        expected_version = 1
        expected_subpacket_count = 2

        result = Packet.read(input_value)
        self.assertIsInstance(result, OperatorPacket)
        self.assertEqual(expected_version, result.packet_version())
        self.assertEqual(expected_subpacket_count, len(result.subpackets))
        self.assertTrue(all([isinstance(packet, LiteralPacket) for packet in result.subpackets]))

    def test_read_operator_packet_with_length_type_1(self):
        input_value = 'EE00D40C823060'
        expected_version = 7
        expected_subpacket_count = 3

        result = Packet.read(input_value)
        self.assertIsInstance(result, OperatorPacket)
        self.assertEqual(expected_version, result.packet_version())
        self.assertEqual(expected_subpacket_count, len(result.subpackets))
        self.assertTrue(all([isinstance(packet, LiteralPacket) for packet in result.subpackets]))

    def test_version_examples(self):
        values = [
            ('8A004A801A8002F478', 16),
            ('620080001611562C8802118E34', 12),
            ('C0015000016115A2E0802F182340', 23),
            ('A0016C880162017C3686B18A3D4780', 31)
        ]
        for input_value, expected_version in values:
            packet = Packet.read(input_value)
            self.assertEqual(expected_version, packet.version())

    def test_sum_packet(self):
        input_value = 'C200B40A82'
        expected_result = 3

        packet = Packet.read(input_value)
        self.assertIsInstance(packet, SumPacket)
        self.assertEqual(expected_result, packet.value())

    def test_product_packet(self):
        input_value = '04005AC33890'
        expected_result = 54

        packet = Packet.read(input_value)
        self.assertIsInstance(packet, ProductPacket)
        self.assertEqual(expected_result, packet.value())

    def test_minimum_packet(self):
        input_value = '880086C3E88112'
        expected_result = 7

        packet = Packet.read(input_value)
        self.assertIsInstance(packet, MinimumPacket)
        self.assertEqual(expected_result, packet.value())

    def test_maximum_packet(self):
        input_value = 'CE00C43D881120'
        expected_result = 9

        packet = Packet.read(input_value)
        self.assertIsInstance(packet, MaximumPacket)
        self.assertEqual(expected_result, packet.value())

    def test_lowerthan_packet(self):
        input_value = 'D8005AC2A8F0'
        expected_result = 1

        packet = Packet.read(input_value)
        self.assertIsInstance(packet, LowerThanPacket)
        self.assertEqual(expected_result, packet.value())

    def test_greaterthan_packet(self):
        input_value = 'F600BC2D8F'
        expected_result = 0

        packet = Packet.read(input_value)
        self.assertIsInstance(packet, GreaterThanPacket)
        self.assertEqual(expected_result, packet.value())

    def test_simple_equal_packet(self):
        input_value = '9C005AC2F8F0'
        expected_result = 0

        packet = Packet.read(input_value)
        self.assertIsInstance(packet, EqualPacket)
        self.assertEqual(expected_result, packet.value())

    def test_complex_equal_packet(self):
        input_value = '9C0141080250320F1802104A08'
        expected_result = 1

        packet = Packet.read(input_value)
        self.assertIsInstance(packet, EqualPacket)
        self.assertEqual(expected_result, packet.value())

