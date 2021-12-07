from __future__ import annotations

from typing import Iterable, Sized, Optional

from aocutils.aoc import Exercise
from aocutils.file import get_input_data_filepath


class BingoCard:

    def __init__(self, rows: tuple[tuple[int]]) -> None:
        super().__init__()
        self.rows = tuple({number: False for number in row} for row in rows if len(row))

    def __str__(self) -> str:
        str_card = ""
        for row in self.rows:
            for number, checked in row.items():
                if checked:
                    str_card += '☑'
                else:
                    str_card += '☐'
                str_card += f"{number}\t"
            str_card += "\n"

        return str_card

    def is_winning_row(self, row_index: int) -> bool:
        return all([checked for checked in self.rows[row_index].values()])

    def is_winning_column(self, column_index: int) -> bool:
        return all([
            list(row.values())[column_index]
            for row in self.rows
        ])

    def draw(self, drawn_number: int) -> tuple[Optional[int], Optional[int]]:
        for row_index, row in enumerate(self.rows):
            for column_index, number in enumerate(row.keys()):
                if drawn_number == number:
                    row[drawn_number] = True
                    return row_index, column_index

        return None, None

    def unchecked_numbers(self) -> tuple[int]:
        return tuple([int(number)
                      for row in self.rows
                      for number, checked in row.items() if not checked])


class BingoSystem:

    def __init__(self, input_data: list[str]) -> None:
        self.draws: tuple[int] = tuple(int(number) for number in input_data.pop(0).strip().split(','))
        input_data.pop(0)
        self.cards = []
        card_rows = []
        while input_data:
            number_line = tuple(int(number) for number in input_data.pop(0).strip().split(sep=' ') if number)
            if not number_line:
                if not len(card_rows):
                    continue
                print(f'Creating a new BingoCard with rows {tuple(card_rows)}')
                self.cards.append(BingoCard(tuple(card_rows)))
                card_rows = []
                continue
            card_rows.append(number_line)

    def draw(self) -> list[tuple]:
        winning_order = []
        cards = self.cards
        for number in self.draws:
            for card_id, card in enumerate(cards):
                if card in [winning_card for winning_card, last_draw in winning_order]:
                    continue
                row, col = card.draw(number)
                if row is None or col is None:
                    continue

                is_winning_row = card.is_winning_row(row)
                is_winning_column = card.is_winning_column(col)

                if is_winning_row or is_winning_column:
                    print(f"Winning card with draw {number}:\n{card}")
                    winning_order.append(tuple([card, number]))

        return winning_order


class Day04(Exercise):
    def __init__(self, input_data: Iterable | Sized) -> None:
        super().__init__(input_data)
        self.winning_order = BingoSystem(list(input_data)).draw()

    def solve_for_card_at_index(self, index: int) -> int:
        winning_card, last_drawn = self.winning_order[index]
        print(winning_card)
        print(f'Winning draw: {last_drawn}')
        unchecked = winning_card.unchecked_numbers()
        print(f'Unchecked numbers: {unchecked} (sum: {sum(unchecked)})')

        return sum(unchecked) * last_drawn

    def part_one(self) -> int:
        return self.solve_for_card_at_index(0)

    def part_two(self) -> int:
        return self.solve_for_card_at_index(-1)


if __name__ == '__main__':
    inputfile_path = get_input_data_filepath(__file__)
    with open(inputfile_path) as input_file:
        exercise = Day04(input_file.readlines())
        exercise.solve_all()
