from statistics import median

from aocutils.aoc import Exercise
from aocutils.file import get_input_data_filepath


class ConstantCostCrabFormation:

    def __init__(self, positions: list[int]) -> None:
        self.positions: list[int] = positions
        self.target_position: int = median(positions)

    def fuel_consumption(self) -> int:
        total = 0

        for pos in self.positions:
            distance = self.distance(pos)
            print(f'From {pos} to {self.target_position}: {distance} fuel units')
            total += distance

        return int(total)

    def distance(self, pos) -> int:
        return max(pos, self.target_position) - min(pos, self.target_position)


class LinearCostCrabFormation:

    def __init__(self, positions: list[int]) -> None:
        self.positions: list[int] = positions
        self.max_pos = max(positions)
        self.min_pos = min(positions)

        # Yeah... brute-force all the way
        self.target_position, self.target_cost = self.compute_cheapest_target()

    @classmethod
    def distance_cost(cls, distance):
        return sum(range(distance + 1))

    @classmethod
    def distance(cls, from_pos, to_pos) -> int:
        return max(from_pos, to_pos) - min(from_pos, to_pos)

    def fuel_consumption(self) -> int:
        return self.target_cost

    def compute_cheapest_target(self) -> tuple[int, int]:
        fuel_costs = [0] * (self.max_pos + 1)
        for target in range(self.min_pos, self.max_pos + 1):
            for pos in self.positions:
                fuel_costs[target] += self.distance_cost(self.distance(pos, target))

        min_cost = min(fuel_costs)
        return fuel_costs.index(min_cost), min_cost


class Day07(Exercise):

    def part_one(self) -> int:
        crabs = ConstantCostCrabFormation([int(pos) for pos in list(self.input_data)[0].split(',')])
        return crabs.fuel_consumption()

    def part_two(self) -> int:
        crabs = LinearCostCrabFormation([int(pos) for pos in list(self.input_data)[0].split(',')])
        print(f'Moving every crabs to {crabs.target_position}')
        return crabs.fuel_consumption()


if __name__ == '__main__':
    inputfile_path = get_input_data_filepath(__file__)
    with open(inputfile_path) as input_file:
        exercise = Day07(input_file.readlines())
        exercise.solve_all()
