from __future__ import annotations

import math
import uuid
from collections.abc import Sized
from dataclasses import dataclass
from typing import Optional

from aocutils.aoc import Exercise
from aocutils.file import get_input_data_filepath


@dataclass
class MapPoint:
    parent_map: HeightMap
    x: int
    y: int
    depth: int

    def __post_init__(self):
        self.basin_id = None

        if self.depth >= 9:
            self.basin_id = -1

    def __hash__(self) -> int:
        return hash(f'({str(self.x)}, {str(self.y)})={str(self.depth)}')

    def is_lowest(self) -> bool:
        return self.depth < min([point.depth for point in self.neighbors()])

    def top_neighbor(self) -> Optional[MapPoint]:
        if self.y <= 0:
            return None

        return self.parent_map[(self.x, self.y - 1)]

    def right_neighbor(self) -> Optional[MapPoint]:
        if self.x >= self.parent_map.width - 1:
            return None

        return self.parent_map[(self.x + 1, self.y)]

    def down_neighbor(self) -> Optional[MapPoint]:
        if self.y >= self.parent_map.height - 1:
            return None

        return self.parent_map[(self.x, self.y + 1)]

    def left_neighbor(self) -> Optional[MapPoint]:
        if self.x <= 0:
            return None

        return self.parent_map[(self.x - 1, self.y)]

    def neighbors(self) -> list[MapPoint]:
        return [point
                for point in (self.top_neighbor(), self.right_neighbor(), self.down_neighbor(), self.left_neighbor())
                if point is not None]


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


class HeightMap:

    def __getitem__(self, coordinates: tuple[int, int]) -> MapPoint:
        col, row = coordinates
        if col >= self.width or row >= self.height:
            raise KeyError

        point_index = (self.width - 1) * row + col + row
        return self.points[point_index]

    def __init__(self, rows: list[str]) -> None:
        self.height = len(rows)
        self.width = len(rows[0].strip())
        self.points = [MapPoint(self, x, y, int(depth))
                       for y, row in enumerate(rows)
                       for x, depth in enumerate(row.strip())]

    def low_points(self) -> list[MapPoint]:
        return [point for point in self.points if point.is_lowest()]

    def basins(self) -> list[Basin]:
        return [Basin(basin_id, point) for basin_id, point in enumerate(self.low_points())]


class Day09(Exercise):

    def part_one(self) -> int:
        height_map = HeightMap(list(self.input_data))
        return sum([1 + point.depth for point in height_map.low_points()])

    def part_two(self) -> int:
        height_map = HeightMap(list(self.input_data))
        basins = sorted(height_map.basins(), key=len)
        return math.prod([len(basin) for basin in basins[-3:]])


if __name__ == '__main__':
    inputfile_path = get_input_data_filepath(__file__)
    with open(inputfile_path) as input_file:
        exercise = Day09(input_file.readlines())
        exercise.solve_all()
