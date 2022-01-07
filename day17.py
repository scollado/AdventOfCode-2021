from __future__ import annotations

import re
from math import copysign
from typing import Iterable, Sized

from aocutils.aoc import Exercise
from aocutils.file import get_input_data_filepath

Position = tuple[int, int]


class Probe:

    def __init__(self, horizontal_velocity: int, vertical_velocity: int) -> None:
        super().__init__()
        self.horizontal_velocity = abs(horizontal_velocity)
        self.vertical_velocity = vertical_velocity
        self.position: Position = (0, 0)

    def move(self) -> Position:
        self.position = (self.position[0] + self.horizontal_velocity, self.position[1] + self.vertical_velocity)
        self.vertical_velocity -= 1
        if self.horizontal_velocity != 0:
            self.horizontal_velocity -= int(copysign(1, self.horizontal_velocity))

        return self.position


class TargetArea:

    def __init__(self, x_range: str, y_range: str):
        self.x_boundaries = sorted(int(bound) for bound in x_range.split('..'))
        self.y_boundaries = sorted(int(bound) for bound in y_range.split('..'))

    def __contains__(self, item) -> bool:
        if isinstance(item, Probe):
            return min(self.x_boundaries) <= item.position[0] <= max(self.x_boundaries) \
                   and min(self.y_boundaries) <= item.position[1] <= max(self.y_boundaries)

        return False

    def __repr__(self) -> str:
        return f'({min(self.x_boundaries)}, {max(self.y_boundaries)}) to ({max(self.x_boundaries)}, {min(self.y_boundaries)})'


class LaunchAttempt:

    def __init__(self, starting_velocities: tuple[int, int], target: TargetArea) -> None:
        self.target = target
        self.probe = Probe(starting_velocities[0], starting_velocities[1])
        self.moves: list[tuple[int, int]] = []

        while not self.is_complete():
            self.moves.append(self.probe.move())

    def is_successfull(self) -> bool:
        return self.probe in self.target

    def is_missed(self) -> bool:
        probe_x, probe_y = self.probe.position
        return probe_y < min(self.target.y_boundaries) or probe_x > max(self.target.x_boundaries)

    def is_complete(self) -> bool:
        return self.is_successfull() or self.is_missed()

    def max_height(self) -> int:
        return max(height for _, height in self.moves)


def read_target_area(input_data: str) -> TargetArea:
    pattern = re.compile(r'target area: x=(?P<x_boundaries>[\d.-]+), y=(?P<y_boundaries>[\d.-]+)')
    matches = pattern.match(input_data)
    return TargetArea(matches.group('x_boundaries'), matches.group('y_boundaries'))


class Day17(Exercise):

    def __init__(self, input_data: Iterable | Sized | list[str]) -> None:
        super().__init__(input_data)
        self.attempts = []
        self.successes = []
        target = read_target_area(self.input_data.pop().strip())
        self.log.info('Target area: %s', target)

        max_x = max(target.x_boundaries)
        min_y = min(target.y_boundaries)
        for x_velocity in range(max_x+1):
            for y_velocity in range(min_y-1, abs(min_y) + 1):
                self.log.debug('Trying velocity (x: %d, y: %d)', x_velocity, y_velocity)
                attempt = LaunchAttempt((x_velocity, y_velocity), target)
                self.attempts.append(attempt)
                if attempt.is_successfull():
                    self.successes.append(attempt)
                    self.log.info('(x: %d, y: %d)\t ⇒ Success in %d steps!', x_velocity, y_velocity, len(attempt.moves))

        print(f'Found {len(self.successes)} velocity configs in {len(self.attempts)} launch simulations.')
        print(f'Longuest Trick shot : {max(len(attempt.moves) for attempt in self.successes)} steps')

    def part_one(self) -> int:
        return max(success.max_height() for success in self.successes)

    def part_two(self) -> int:
        return len(self.successes)


if __name__ == '__main__':
    inputfile_path = get_input_data_filepath(__file__)
    with open(inputfile_path) as input_file:
        exercise = Day17(input_file.readlines())
        exercise.solve_all()
