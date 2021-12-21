from __future__ import annotations

from aocutils.aoc import Exercise, Matrix
from aocutils.file import get_input_data_filepath


class FlashingOctopus(Matrix.Cell):

    def __init__(self, octopus_map: OctopusesMap, x: int, y: int, energy_level: int = 0) -> None:
        super().__init__(octopus_map, x, y, energy_level)
        self.flashed = False

    def flash(self) -> bool:
        if self.value <= 9 or self.flashed:
            return False
        self._propagate_energy()
        self.flashed = True
        return True

    def reset(self):
        self.value = 0
        self.flashed = False

    def _propagate_energy(self):
        for octopus in self.neighbors():
            octopus.value += 1


class OctopusesMap(Matrix):

    def _init_value(self, x, y, value) -> Matrix.Cell:
        return FlashingOctopus(self, x, y, int(value))

    def tick(self) -> int:

        # Increase energy level
        for octopus in self.values:
            octopus.value += 1

        # Make octopuses flash and propagate energy until no flash happens
        turn_flashes = None
        tick_flashes = 0
        while turn_flashes is None or 0 < turn_flashes:
            turn_flashes = len([octopus.flashed for octopus in self.values if octopus.flash()])
            tick_flashes += turn_flashes

        # Reset flashed octopuses
        for octopus in [flashed for flashed in self.values if flashed.flashed]:
            octopus.reset()

        return tick_flashes


class Day11(Exercise):
    def part_one(self) -> int:
        octopus_map = OctopusesMap(list(self.input_data))

        total_flashes = 0
        for _ in range(0, 100):
            total_flashes += octopus_map.tick()

        return total_flashes

    def part_two(self) -> int:
        octopus_map = OctopusesMap(list(self.input_data))

        target_value = '0' * len(octopus_map.values)
        tick_count = 0

        while str(octopus_map).replace("\n", "") != target_value:
            octopus_map.tick()
            tick_count += 1

        return tick_count


if __name__ == '__main__':
    inputfile_path = get_input_data_filepath(__file__)
    with open(inputfile_path) as input_file:
        exercise = Day11(input_file.readlines())
        exercise.solve_all()
