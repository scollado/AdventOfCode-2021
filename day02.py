from typing import Iterable

from aocutils.aoc import Exercise
from aocutils.file import get_input_data_filepath


class Command:
    SYMBOLS = {
        'up': '↗',
        'down': '↘',
        'forward': '→'
    }

    def __init__(self, as_str: str) -> None:
        super().__init__()
        self.as_str = as_str

    def get_action(self) -> str:
        return self.as_str.split(' ')[0]

    def get_amount(self) -> int:
        return int(self.as_str.split(' ')[1])

    def get_symbol(self) -> str:
        return Command.SYMBOLS[self.get_action()]


class ElvishSubmarine:

    def __init__(self) -> None:
        super().__init__()
        self.depth = 0
        self.position = 0

    def up(self, amount: int) -> None:
        self.depth -= amount

    def down(self, amount: int) -> None:
        self.depth += amount

    def forward(self, amount: int) -> None:
        self.position += amount

    def run_command(self, command: Command) -> None:
        getattr(self, command.get_action())(command.get_amount())


class AimingElvishSubmarine(ElvishSubmarine):

    def __init__(self) -> None:
        super().__init__()
        self.aim = 0

    def down(self, amount: int) -> None:
        self.aim += amount

    def up(self, amount: int) -> None:
        self.aim -= amount

    def forward(self, amount: int) -> None:
        super().forward(amount)
        self.depth += self.aim * amount


class Day02(Exercise):

    def _read_commands(self) -> Iterable[Command]:
        for line in self.input_data:
            yield Command(line.strip())

    def part_one(self) -> int:
        yellow_submarine = ElvishSubmarine()

        for command in self._read_commands():
            yellow_submarine.run_command(command)
            print(f"{command.get_symbol()}({command.get_amount()}) " +
                  f"New Submarine position (depth: {yellow_submarine.depth}, pos: {yellow_submarine.position})")

        return yellow_submarine.depth * yellow_submarine.position

    def part_two(self) -> int:
        yellow_submarine = AimingElvishSubmarine()

        for command in self._read_commands():
            yellow_submarine.run_command(command)
            print(f"{command.get_symbol()}({command.get_amount()}) " +
                  f"New Submarine position (depth: {yellow_submarine.depth}, pos: {yellow_submarine.position}, " +
                  f"aim: {yellow_submarine.aim})")

        return yellow_submarine.depth * yellow_submarine.position


if __name__ == '__main__':
    inputfile_path = get_input_data_filepath(__file__)
    with open(inputfile_path) as input_file:
        exercise = Day02(input_file.readlines())
        exercise.solve_all()
