from __future__ import annotations

import math
from abc import ABC, abstractmethod
from io import StringIO

from aocutils.aoc import Exercise
from aocutils.file import get_input_data_filepath
from aocutils.string import hex2bin_stream, bin2int


class Packet(ABC):

    def __init__(self, version: int, binary_content: StringIO) -> None:
        super().__init__()
        self._version: int = version
        self.binary_content = binary_content

    def packet_version(self) -> int:
        return self._version

    @abstractmethod
    def version(self) -> int:
        pass

    @abstractmethod
    def value(self) -> int:
        pass

    @classmethod
    def read(cls, hex_string: str) -> Packet:
        with hex2bin_stream(hex_string) as binary_repr:
            return cls.from_stream(binary_repr)

    @classmethod
    def from_stream(cls, binary_repr) -> Packet:
        packet_version = bin2int(binary_repr.read(3))
        packet_type_id = bin2int(binary_repr.read(3))
        return PACKET_TYPES[packet_type_id](packet_version, binary_repr)


class LiteralPacket(Packet):

    def version(self) -> int:
        return self.packet_version()

    def __init__(self, version: int, binary_content: StringIO) -> None:
        super().__init__(version, binary_content)
        is_last = False
        self.content = ''
        while not is_last:
            is_last = self.binary_content.read(1) == '0'
            self.content += self.binary_content.read(4)

    def __repr__(self) -> str:
        return self.content

    def value(self) -> int:
        return bin2int(str(self))


class OperatorPacket(Packet, ABC):

    def __init__(self, version: int, binary_content: StringIO) -> None:
        super().__init__(version, binary_content)
        self.subpackets = []
        self.length_type_id = self.binary_content.read(1)

        if '0' == self.length_type_id:
            subpackets_length = bin2int(self.binary_content.read(15))
            with StringIO(self.binary_content.read(subpackets_length)) as subpackets_list:
                self._fill_subpackets(subpackets_list)
        else:
            subpackets_count = bin2int(self.binary_content.read(11))
            self._fill_subpackets(self.binary_content, subpackets_count)

    def _fill_subpackets(self, subpackets_list: StringIO, limit: int = None):

        while True:
            try:
                self.subpackets.append(Packet.from_stream(subpackets_list))
                if limit is not None and limit <= len(self.subpackets):
                    break
            except:
                break

    def _subpacket_values(self) -> list[int]:
        return [packet.value() for packet in self.subpackets]

    def version(self) -> int:
        return self.packet_version() + sum([sub.version() for sub in self.subpackets])


class SumPacket(OperatorPacket):

    def value(self) -> int:
        return sum(self._subpacket_values())


class ProductPacket(OperatorPacket):

    def value(self) -> int:
        return math.prod(self._subpacket_values())


class MinimumPacket(OperatorPacket):

    def value(self) -> int:
        return min(self._subpacket_values())


class MaximumPacket(OperatorPacket):

    def value(self) -> int:
        return max(self._subpacket_values())


class GreaterThanPacket(OperatorPacket):

    def value(self) -> int:
        packet_values = self._subpacket_values()
        return int(packet_values[0] > packet_values[1])


class LowerThanPacket(OperatorPacket):

    def value(self) -> int:
        packet_values = self._subpacket_values()
        return int(packet_values[0] < packet_values[1])


class EqualPacket(OperatorPacket):

    def value(self) -> int:
        packet_values = self._subpacket_values()
        return int(packet_values[0] == packet_values[1])


PACKET_TYPES = [
    SumPacket,
    ProductPacket,
    MinimumPacket,
    MaximumPacket,
    LiteralPacket,
    GreaterThanPacket,
    LowerThanPacket,
    EqualPacket
]


class Day16(Exercise):
    def part_one(self) -> int:
        return Packet.read(self.input_data[0].strip()).version()

    def part_two(self) -> int:
        return Packet.read(self.input_data[0].strip()).value()


if __name__ == '__main__':
    inputfile_path = get_input_data_filepath(__file__)
    with open(inputfile_path) as input_file:
        exercise = Day16(input_file.readlines())
        exercise.solve_all()
