from __future__ import annotations

from collections import Counter, defaultdict
from typing import Iterable, Sized

from aocutils.aoc import Exercise
from aocutils.file import get_input_data_filepath


class Polymer(Sized):

    def __len__(self) -> int:
        return sum(self.pairs.values()) + 1

    def __init__(self, source_template: str) -> None:
        self.template = source_template
        pairs = [left + right for left, right in zip(source_template, source_template[1:])]
        self.pairs = Counter(pairs)

    def __repr__(self):
        output = ''
        for pair in self.pairs.elements():
            output += pair[0]
        output += list(self.pairs.keys())[-1][-1]
        return output

    def strength(self) -> int:
        element_count = defaultdict(int)
        for (left, right), count in self.pairs.items():
            element_count[left] += count
        element_count[self.template[-1]] += 1
        counts = element_count.values()
        return max(counts) - min(counts)

    def apply_rules(self, rules: dict[str, str]):
        new_polymer_pairs = Counter([])
        for (left, right), count in self.pairs.items():
            if insert := rules[left + right]:
                new_polymer_pairs[left + insert] += count
                new_polymer_pairs[insert + right] += count
            else:
                new_polymer_pairs[left + right] += count

        self.pairs = new_polymer_pairs
        # new_chain = ''
        # for pair in [left + right for left, right in zip(self.template, self.template[1:])]:
        #     new_left_pair, new_right_pair = rules[pair].apply(pair)
        #     new_chain += new_left_pair[0] + new_right_pair[0]
        # new_chain += self.template[-1]
        #
        # return Polymer(new_chain)
        return self


class Day14(Exercise):

    def __init__(self, input_data: Iterable | Sized) -> None:
        super().__init__([line.strip() for line in input_data])
        self.polymer_template = self.input_data[0]
        self.rules = {pair: insert
                      for pair, insert in [line.strip().split(' -> ') for line in self.input_data[2:] if 0 < len(line)]}

    def develop_polymer(self, polymer, steps: int) -> Polymer:
        for run in range(steps):
            print(f'Run #{run + 1}')
            polymer.apply_rules(self.rules)
            print(polymer.pairs)
        return polymer

    def part_one(self) -> int:
        polymer = Polymer(self.polymer_template)
        return self.develop_polymer(polymer, 10).strength()

    def part_two(self) -> int:
        polymer = Polymer(self.polymer_template)
        return self.develop_polymer(polymer, 40).strength()


if __name__ == '__main__':
    inputfile_path = get_input_data_filepath(__file__)
    with open(inputfile_path) as input_file:
        exercise = Day14(input_file.readlines())
        exercise.solve_all()
