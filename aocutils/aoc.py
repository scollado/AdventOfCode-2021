from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Iterable, Sized, Any, Optional


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


class Matrix:
    class Cell:

        def __init__(self, matrix: Matrix, x: int, y: int, value: Any) -> None:
            self.matrix = matrix
            self.x = x
            self.y = y
            self.value = value

        def __repr__(self):
            return str(self.value)

        def __eq__(self, other: Matrix.Cell):
            return self.value == other.value

        def neighbors(self) -> list[Matrix.Cell]:
            return [neighbor
                    for neighbor in [self.top_left(), self.top(), self.top_right(), self.right(),
                                     self.bottom_right(), self.bottom(), self.bottom_left(), self.left()]
                    if neighbor is not None]

        def top_left(self) -> Optional[Matrix.Cell]:
            if self.x <= 0 or self.y <= 0:
                return None
            return self.matrix[(self.x - 1, self.y - 1)]

        def top(self) -> Optional[Matrix.Cell]:
            if self.y <= 0:
                return None
            return self.matrix[(self.x, self.y - 1)]

        def top_right(self) -> Optional[Matrix.Cell]:
            if self.y <= 0 or self.x >= self.matrix.max_x:
                return None
            return self.matrix[(self.x + 1, self.y - 1)]

        def right(self) -> Optional[Matrix.Cell]:
            if self.x >= self.matrix.max_x:
                return None
            return self.matrix[(self.x + 1, self.y)]

        def bottom_right(self) -> Optional[Matrix.Cell]:
            if self.y >= self.matrix.max_y or self.x >= self.matrix.max_x:
                return None
            return self.matrix[(self.x + 1, self.y + 1)]

        def bottom(self) -> Optional[Matrix.Cell]:
            if self.y >= self.matrix.max_y:
                return None
            return self.matrix[(self.x, self.y + 1)]

        def bottom_left(self) -> Optional[Matrix.Cell]:
            if self.y >= self.matrix.max_y or self.x <= 0:
                return None
            return self.matrix[(self.x - 1, self.y + 1)]

        def left(self) -> Optional[Matrix.Cell]:
            if self.x <= 0:
                return None
            return self.matrix[(self.x - 1, self.y)]

    def __init__(self, input_data: list[str]) -> None:
        self.input_data = input_data
        self.max_x = len(input_data[0].strip()) - 1
        self.max_y = len(input_data) - 1

        self.values = [self._init_value(x, y, value)
                       for y, row in enumerate(input_data)
                       for x, value in enumerate(row.strip())
                       ]

    def __getitem__(self, coordinates: tuple[int, int]) -> Optional[Any]:
        col, row = coordinates
        if col > self.max_x or row > self.max_y:
            raise KeyError

        value_index = self.max_x * row + col + row
        return self.values[value_index]

    def __repr__(self) -> str:
        output = ''
        for value in self.values:
            output += str(value)
            if value.x == self.max_x:
                output += "\n"
        return output.strip()

    def __eq__(self, other: Matrix):
        return str(self) == str(other)

    @abstractmethod
    def _init_value(self, x, y, value) -> Matrix.Cell:
        return Matrix.Cell(self, x, y, value)

    def vsplit(self, x: int) -> tuple[Matrix, Matrix]:
        matrix_lines = str(self).split("\n")
        for line in matrix_lines:
            for column, value in enumerate(line):
                if column == x:
                    print(' | ', end='')
                else:
                    print(value, end='')
            print('')
        print('')

        left_half = [line[0:x] for line in matrix_lines]
        right_half = [line[x+1:] for line in matrix_lines]

        return self.__class__(left_half), self.__class__(right_half)

    def hsplit(self, y: int) -> tuple[Matrix, Matrix]:
        matrix_lines = str(self).split("\n")
        for line, value in enumerate(matrix_lines):
            if line == y:
                print('—' * len(value))
            else:
                print(value)
        print('')

        top_half = matrix_lines[0:y]
        bottom_half = matrix_lines[y+1:]

        return self.__class__(top_half), self.__class__(bottom_half)

    def vflip(self) -> Matrix:
        return self.__class__(list(reversed(self.input_data)))

    def hflip(self) -> Matrix:
        return self.__class__([line[::-1] for line in self.input_data])
