from __future__ import annotations

import math
from collections.abc import Sized
from typing import Any

from aocutils.aoc import Exercise
from aocutils.matrix import Matrix
from aocutils.file import get_input_data_filepath


class MapPoint(Matrix.Cell):

    def __init__(self, matrix: Matrix, x: int, y: int, value: Any) -> None:
        super().__init__(matrix, x, y, value)

        self.basin_id = None

        if self.value >= 9:
            self.basin_id = -1

    def __hash__(self) -> int:
        return super().__hash__()

    def __eq__(self, other: MapPoint):
        return self.x == other.x and self.y == other.y and self.value == other.value and self.basin_id == other.basin_id

    def is_lowest(self) -> bool:
        return self.value < min([point.value for point in self.neighbors()])


class Basin(Sized):

    def __init__(self, basin_id: int, starting_point: MapPoint) -> None:
        self.id = basin_id
        self.points = {starting_point}
        self.propagate(starting_point)

    def __len__(self) -> int:
        return len(self.points)

    def propagate(self, from_point: MapPoint):
        if from_point.basin_id is not None:
            return
        from_point.basin_id = self.id
        self.points.add(from_point)
        for neighbor in from_point.neighbors():
            self.propagate(neighbor)


class HeightMap(Matrix):

    def _init_value(self, x, y, value) -> Matrix.Cell:
        return MapPoint(self, x, y, int(value))

    def low_points(self) -> list[MapPoint]:
        return [point for point in self.cells if point.is_lowest()]

    def basins(self) -> list[Basin]:
        return [Basin(basin_id, point) for basin_id, point in enumerate(self.low_points())]


class Day09(Exercise):

    def part_one(self) -> int:
        height_map = HeightMap(list(self.input_data), allow_diagonal=False)
        return sum([1 + point.value for point in height_map.low_points()])

    def part_two(self) -> int:
        height_map = HeightMap(list(self.input_data), allow_diagonal=False)
        basins = sorted(height_map.basins(), key=len)
        return math.prod([len(basin) for basin in basins[-3:]])


if __name__ == '__main__':
    inputfile_path = get_input_data_filepath(__file__)
    with open(inputfile_path) as input_file:
        exercise = Day09(input_file.readlines())
        exercise.solve_all()
