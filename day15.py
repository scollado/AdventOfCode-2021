from __future__ import annotations

from aocutils.aoc import Exercise
from aocutils.file import get_input_data_filepath
from aocutils.matrix import Matrix
from aocutils.pathfinding import Dijkstra


class RiskMap(Matrix):
    class RiskLevel(Matrix.Cell):

        def __hash__(self) -> int:
            return hash(f'({str(self.x)}, {str(self.y)})={str(self.value)}')

        def __eq__(self, other: Matrix.Cell):
            return super().__eq__(other) and self.x == other.x and self.y == other.y

        def __repr__(self) -> str:
            return f'({self.x},{self.y})={self.value}'

    def _init_value(self, x, y, value) -> RiskMap.RiskLevel:
        return RiskMap.RiskLevel(self, x, y, int(value))


class ExtendedRiskMap(RiskMap):

    def __init__(self, input_data: list[str], extension_factor: int) -> None:
        self.original_input_data = input_data
        scaled_input_data: list[str] = []
        scaled_columns: list[str] = []

        def limit(value: int) -> int:
            if value > 9:
                return value - 9
            return value

        for line in input_data:
            new_line = ''
            for offset in range(extension_factor):
                new_line += ''.join([str(limit(offset + int(digit)))
                                     for digit in line.strip()])
            scaled_columns.append(new_line)

        for offset in range(extension_factor):
            for line in scaled_columns:
                scaled_input_data.append(''.join([str(limit(offset + int(digit)))
                                                  for digit in line]))

        super().__init__(scaled_input_data, allow_diagonal=False)


class Day15(Exercise):

    def part_one(self) -> int:
        risk_map = RiskMap(self.input_data, allow_diagonal=False)
        return self.solve(risk_map)

    def part_two(self) -> int:
        extended_map = ExtendedRiskMap(self.input_data, 5)
        return self.solve(extended_map)

    @staticmethod
    def solve(risk_map: RiskMap) -> int:
        pathfinder = Dijkstra(matrix=risk_map, start=risk_map.cells[0])
        path = pathfinder.find_path_to(risk_map.cells[-1])

        result = sum([cell.value for cell in path if cell != risk_map[(0, 0)]])
        print(f'{path} = {result}')
        return result


if __name__ == '__main__':
    inputfile_path = get_input_data_filepath(__file__)
    with open(inputfile_path) as input_file:
        exercise = Day15(input_file.readlines())
        exercise.solve_all()
