from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable, Sized

from aocutils.aoc import Exercise
from aocutils.file import get_input_data_filepath

WIRES = 'abcdef'

'''
  0:      1:      2:      3:      4:
 aaaa    ....    aaaa    aaaa    ....
b    c  .    c  .    c  .    c  b    c
b    c  .    c  .    c  .    c  b    c
 ....    ....    dddd    dddd    dddd
e    f  .    f  e    .  .    f  .    f
e    f  .    f  e    .  .    f  .    f
 gggg    ....    gggg    gggg    ....

  5:      6:      7:      8:      9:
 aaaa    aaaa    aaaa    aaaa    aaaa
b    .  b    .  .    c  b    c  b    c
b    .  b    .  .    c  b    c  b    c
 dddd    dddd    ....    dddd    dddd
.    f  e    f  .    f  e    f  .    f
.    f  e    f  .    f  e    f  .    f
 gggg    gggg    ....    gggg    gggg

'''


@dataclass(frozen=True, repr=False)
class SegmentWiring:
    top: str
    top_right: str
    bottom_right: str
    bottom: str
    bottom_left: str
    top_left: str
    middle: str


class SegmentDisplay:

    def __init__(self, wiring: SegmentWiring) -> None:
        self.wiring = wiring

    def convert_signal(self, signal: str) -> str:
        signal = ''.join(sorted(signal))

        number_mapping = [
            ''.join(sorted([self.wiring.top, self.wiring.top_right, self.wiring.top_left,
                            self.wiring.bottom, self.wiring.bottom_right, self.wiring.bottom_left])),
            ''.join(sorted([self.wiring.top_right, self.wiring.bottom_right])),
            ''.join(sorted([self.wiring.top, self.wiring.top_right, self.wiring.middle,
                            self.wiring.bottom_left, self.wiring.bottom])),
            ''.join(sorted([self.wiring.top, self.wiring.middle, self.wiring.bottom,
                            self.wiring.top_right, self.wiring.bottom_right])),
            ''.join(
                sorted([self.wiring.top_left, self.wiring.top_right, self.wiring.middle, self.wiring.bottom_right])),
            ''.join(sorted([self.wiring.top, self.wiring.top_left, self.wiring.middle, self.wiring.bottom_right,
                            self.wiring.bottom])),
            ''.join(sorted([self.wiring.top, self.wiring.top_left, self.wiring.middle,
                            self.wiring.bottom_right, self.wiring.bottom_left, self.wiring.bottom])),
            ''.join(sorted([self.wiring.top, self.wiring.top_right, self.wiring.bottom_right])),
            ''.join(sorted([self.wiring.top, self.wiring.top_right, self.wiring.top_left, self.wiring.middle,
                            self.wiring.bottom_right,
                            self.wiring.bottom_left, self.wiring.bottom])),
            ''.join(sorted([self.wiring.top, self.wiring.top_right, self.wiring.top_left, self.wiring.middle,
                            self.wiring.bottom_right,
                            self.wiring.bottom]))
        ]

        return str(number_mapping.index(signal))

    def display_digit(self, digit: int) -> str:
        out = ''

        # Top
        if digit in [0, 2, 3, 5, 6, 7, 8, 9]:
            out += f" {self.wiring.top * 4} \n"
        else:
            out += ' .... \n'

        # Top left / right
        if digit in [0, 4, 8, 9]:
            line = self.wiring.top_left + (' ' * 4) + self.wiring.top_right + "\n"
            out += line * 2
        elif digit in [1, 2, 3, 7]:
            line = '.' + (' ' * 4) + self.wiring.top_right + "\n"
            out += line * 2
        else:  # 5, 6
            line = self.wiring.top_left + (' ' * 4) + ".\n"
            out += line * 2

        # Middle
        if digit in [2, 3, 4, 5, 6, 8, 9]:
            out += f" {self.wiring.middle * 4} \n"
        else:  # 0, 1, 7
            out += ' ' + ('.' * 4) + " \n"

        # Bottom left / right
        if digit in [0, 6, 8]:
            line = self.wiring.bottom_left + (' ' * 4) + self.wiring.bottom_right + "\n"
            out += line * 2
        elif digit in [1, 3, 4, 5, 7, 9]:
            line = '.' + (' ' * 4) + self.wiring.bottom_right + "\n"
            out += line * 2
        else:  # 2
            line = self.wiring.bottom_left + (' ' * 4) + ".\n"
            out += line * 2

        # Bottom
        if digit in [0, 2, 3, 5, 6, 8, 9]:
            out += ' ' + (self.wiring.bottom * 4) + ' '
        else:  # 1, 4, 7
            out += ' ' + ('.' * 4) + ' '

        return out


class EntryLine:

    def __init__(self, line: str) -> None:
        self.input_value, self.output_signals = line.strip().split(' | ')

    def count_unique_output_signals(self) -> int:
        return len([signal
                    for signal in self.output_signals.split(' ')
                    if len(signal) in [2, 3, 4, 7]])

    def output_value(self):
        display_segment = SegmentDisplay(self.decode_segments_wiring())
        out = ''
        for signal in self.output_signals.split(' '):
            out += display_segment.convert_signal(signal)

        return out

    def decode_segments_wiring(self):
        input_signals = sorted([set(sorted(signal.strip())) for signal in self.input_value.split(' ')], key=len)
        # 1(2bit) 7(3bit) 4(4bit) 2/3/5(5bits) 0/6/9(6bit) 8(7bit)
        signal_1 = input_signals[0]  # Shorter signal = 2 segments
        signal_4 = input_signals[2]  # 4 = 4 segments
        signal_7 = input_signals[1]  # 7 = 3 segments
        signal_8 = input_signals[-1]  # Longest signal = 7 segments

        top_segment = (signal_7 - signal_1).pop()

        # segments for 8 minus segments for 6 gives the top-right segment, which is part of segments for 1
        signal_6 = [signal_set for signal_set in input_signals[6:9] if (signal_8 - signal_set).pop() in signal_1].pop()
        top_right_segment = (signal_8 - signal_6).pop()

        # Bottom-right segment = segments for 1 minus top-right segment
        bottom_right_segment = (signal_1 - {top_right_segment}).pop()

        # segments for 9 minus segments for 4, minus top segment gives (only) the bottom segment
        signal_9 = [signal_set
                    for signal_set in input_signals[6:9]
                    if signal_set != signal_6 and 1 == len(signal_set - signal_4 - {top_segment})].pop()
        bottom_segment = (signal_9 - signal_4 - {top_segment}).pop()

        # Only 6-signals digit remaining : 0
        signal_0 = [signal_set
                    for signal_set in input_signals
                    if 6 == len(signal_set) and signal_set not in [signal_6, signal_9]].pop()

        # Middle segment = segments for 8 minus segments for 0
        middle_segment = (signal_8 - signal_0).pop()

        # enough finding to build signal for 3 segments
        # signal_3 = {top_segment, top_right_segment, bottom_segment, bottom_right_segment, middle_segment}

        # Segments for 6 minus segments for 5 gives bottom-left segment only
        signal_5 = [signal_set
                    for signal_set in input_signals[3:6]
                    if 1 == len(signal_6 - signal_set)].pop()
        # bottom-left segment : segments for 6 minus segments for 5
        bottom_left_segment = (signal_6 - signal_5).pop()

        return SegmentWiring(
            top=top_segment,
            top_right=top_right_segment,
            bottom_right=bottom_right_segment,
            bottom=bottom_segment,
            bottom_left=bottom_left_segment,
            top_left=(signal_8 - {top_segment, top_right_segment, bottom_segment, bottom_right_segment,
                                  bottom_left_segment, middle_segment}).pop(),
            middle=middle_segment
        )


class Day08(Exercise):

    def __init__(self, input_data: Iterable | Sized) -> None:
        super().__init__(input_data)
        self.note_entries = [EntryLine(line) for line in self.input_data]

    def part_one(self) -> int:
        return sum([entry.count_unique_output_signals() for entry in self.note_entries])

    def part_two(self) -> int:
        return sum([int(line.output_value()) for line in self.note_entries])


if __name__ == '__main__':
    inputfile_path = get_input_data_filepath(__file__)
    with open(inputfile_path) as input_file:
        exercise = Day08(input_file.readlines())
        exercise.solve_all()
