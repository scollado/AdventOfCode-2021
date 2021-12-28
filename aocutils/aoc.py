from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Iterable, Sized


class Exercise(ABC):
    def __init__(self, input_data: Iterable | Sized | list[str]) -> None:
        super().__init__()
        self.input_data = input_data

    @abstractmethod
    def part_one(self) -> int:
        pass

    @abstractmethod
    def part_two(self) -> int:
        pass

    def solve_all(self) -> None:
        print("== Solving Part One:")
        solution_part_one = self.part_one()
        print("\n" + ("—" * 80) + "\n")

        print("== Solving Part Two:")
        solution_part_two = self.part_two()
        print("\n" + ("—" * 80) + "\n")

        print(f"» Solution for part one is {solution_part_one}.")
        print(f"» Solution for part two is {solution_part_two}.")


