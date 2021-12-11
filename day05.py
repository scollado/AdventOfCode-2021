from __future__ import annotations

import re
from collections.abc import Iterable
from dataclasses import dataclass
from typing import Iterator, Sized

from aocutils.aoc import Exercise
from aocutils.file import get_input_data_filepath


@dataclass(repr=False)
class Point:
    x: int
    y: int
    value: int = 0

    def on_same_column_than(self, other_point: 'Point'):
        return self.x == other_point.x

    def on_same_line_than(self, other_point: 'Point'):
        return self.y == other_point.y

    def same_as(self, other: 'Point'):
        return other is not None and self.x == other.x and self.y == other.y

    def __repr__(self) -> str:
        return f"({self.x},{self.y})"

    def __add__(self, other: 'Point'):
        if not self.same_as(other):
            raise Exception(f'Can only add points on matching position {self} vs. {other}')

        self.value += 1
        return self


@dataclass
class Segment(Iterable):
    def __iter__(self) -> Iterator[Point]:
        return SegmentIterator(self)

    def __init__(self, start: Point, end: Point):
        self.start = start
        self.end = end

    @classmethod
    def from_string(cls, descriptor: str):
        pattern = r'(?P<start_x>\d+),(?P<start_y>\d+) -> (?P<end_x>\d+),(?P<end_y>\d+)'
        matches = re.match(pattern, descriptor.strip())
        return cls(
            start=Point(int(matches['start_x']), int(matches['start_y'])),
            end=Point(int(matches['end_x']), int(matches['end_y']))
        )

    def __repr__(self) -> str:
        return f"{self.start} -> {self.end}"

    def is_vertical(self) -> bool:
        return self.start.on_same_column_than(self.end)

    def is_horizontal(self) -> bool:
        return self.start.on_same_line_than(self.end)

    def is_oblique(self) -> bool:
        return not (self.is_horizontal() or self.is_vertical())


class SegmentIterator(Iterator):

    def __next__(self) -> Point:
        if self._current_point is None:
            self._current_point = self._segment.start
            return self._current_point

        if self._current_point.same_as(self._segment.end):
            raise StopIteration

        self._current_point = Point(
            x=self._current_point.x + self._x_step,
            y=self._current_point.y + self._y_step
        )

        return self._current_point

    def __init__(self, segment: Segment) -> None:
        super().__init__()
        self._segment = segment
        self._current_point = None

        if segment.is_vertical():
            self._x_step = 0
        elif segment.start.x > segment.end.x:
            self._x_step = -1
        else:
            self._x_step = 1

        if segment.is_horizontal():
            self._y_step = 0
        elif segment.start.y > segment.end.y:
            self._y_step = -1
        else:
            self._y_step = 1


class VentMap:

    def __init__(self, lines: list[Segment]) -> None:
        super().__init__()
        self.max_x = 0
        self.max_y = 0
        for segment in lines:
            self.max_x = max([self.max_x, max(segment.start.x, segment.end.x)])
            self.max_y = max([self.max_y, max(segment.start.y, segment.end.y)])

        self.map: tuple[Point] = tuple(Point(x, y)
                                       for y in range(1 + self.max_y)
                                       for x in range(1 + self.max_x))

        self.segments = tuple(lines)

    def __repr__(self):
        out = ''
        for index, point in enumerate(self.map):
            if point.value == 0:
                out += '.'
            else:
                out += str(point.value)

            if point.x == self.max_x:
                out += "\n"

        return out.strip()

    def draw_one(self, segment: Segment):
        for point in segment:
            position = (point.y * self.max_x) + point.y + point.x
            self.map[position] + point

    def draw(self) -> str:
        for segment in self.segments:
            self.draw_one(segment)

        return str(self)

    def high_points(self) -> int:
        return len([point for point in self.map if point.value >= 2])


class Day05(Exercise):

    def __init__(self, input_data: Iterable[str] | Sized[str]) -> None:
        super().__init__(input_data)
        self.segment_list = [Segment.from_string(line) for line in input_data]

    def part_one(self) -> int:
        orthogonal_segments = [segment for segment in self.segment_list if not segment.is_oblique()]
        part_one_map = VentMap(orthogonal_segments)
        print(part_one_map.draw())

        return part_one_map.high_points()

    def part_two(self) -> int:
        part_two_map = VentMap(self.segment_list)
        print(part_two_map.draw())

        return part_two_map.high_points()


if __name__ == '__main__':
    inputfile_path = get_input_data_filepath(__file__)
    with open(inputfile_path) as input_file:
        exercise = Day05(input_file.readlines())
        exercise.solve_all()
