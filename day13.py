from __future__ import annotations

import re
from collections.abc import Sized
from typing import Any

from aocutils.aoc import Exercise
from aocutils.matrix import Matrix
from aocutils.file import get_input_data_filepath


class TransparentSheet(Matrix, Sized):
    class Dot(Matrix.Cell):
        """
        @field value: bool
        """

        def __init__(self, matrix: Matrix, x: int, y: int, value: Any) -> None:
            super().__init__(matrix, x, y, value == '1')

        def __add__(self, other: TransparentSheet.Dot) -> TransparentSheet.Dot:
            new_value = '0'
            if self.value or other.value:
                new_value = '1'
            return TransparentSheet.Dot(self.matrix, self.x, self.y, new_value)

        def __repr__(self) -> str:
            if self.value:
                return '1'

            return '0'

    @classmethod
    def create_from(cls, other: TransparentSheet) -> TransparentSheet:
        return cls(str(other).split("\n"))

    @classmethod
    def draw_from_points(cls, points: list[str]) -> TransparentSheet:
        points: list[tuple] = [tuple(line.split(',')) for line in points]
        max_x = max([int(point[0]) for point in points])
        max_y = max([int(point[1]) for point in points])
        transparent = [['0' for _ in range(max_x + 1)] for _ in range(max_y + 1)]
        for (x, y) in points:
            transparent[int(y)][int(x)] = '1'

        return cls([''.join(line) for line in transparent])

    def __add__(self, other: TransparentSheet) -> TransparentSheet:
        new_matrix = TransparentSheet.create_from(self)

        for index, dot in enumerate(self.cells):
            new_matrix.cells[index] = dot + other.cells[index]

        return new_matrix

    def __len__(self) -> int:
        return sum([1 for dot in self.cells if dot.value])

    def _init_value(self, x, y, value: str) -> Matrix.Cell:
        return TransparentSheet.Dot(self, x, y, value)

    def vfold(self, column: int) -> TransparentSheet:
        left: TransparentSheet
        right: TransparentSheet
        left, right = self.vsplit(column)
        right = right.hflip()
        return left + right

    def hfold(self, row: int):
        top: TransparentSheet
        down: TransparentSheet
        top, down = self.hsplit(row)
        down = down.vflip()
        return top + down


class Day13(Exercise):

    def __init__(self, input_data: list[str]) -> None:
        input_data = [line.strip() for line in input_data]
        super().__init__(input_data)
        blank_line = input_data.index('')
        points = input_data[:blank_line]
        self.folds = input_data[blank_line + 1:]
        self.transparent = TransparentSheet.draw_from_points(points)

    def part_one(self) -> int:
        return len(self.apply_folding(self.folds[:1]))

    def part_two(self) -> str:
        final_matrix = str(self.apply_folding(self.folds)).replace('0', ' ').replace('1', '#')
        return "\n" + final_matrix

    def apply_folding(self, folds: list[str]) -> TransparentSheet:
        working_matrix = self.transparent
        pattern = re.compile(r'fold along (?P<axe>[xy])=(?P<position>\d+)')
        print(working_matrix)
        print('')
        for fold in folds:
            matches = pattern.search(fold).groupdict()
            print(f"Applying fold on {matches['axe']}={matches['position']}")
            if 'y' == matches['axe']:
                working_matrix = working_matrix.hfold(int(matches['position']))
            else:
                working_matrix = working_matrix.vfold(int(matches['position']))

            print(working_matrix)
            print('')

        return working_matrix


if __name__ == '__main__':
    inputfile_path = get_input_data_filepath(__file__)
    with open(inputfile_path) as input_file:
        exercise = Day13(input_file.readlines())
        exercise.solve_all()
