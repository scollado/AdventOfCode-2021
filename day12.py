from __future__ import annotations

from collections import Counter
from typing import Callable, Iterable, Sized

from typing_extensions import TypeAlias

from aocutils.aoc import Exercise
from aocutils.file import get_input_data_filepath


class Cave:
    CAVE_START = 'start'
    CAVE_END = 'end'

    def __init__(self, node_name: str):
        self.visits = []
        self.node_name = node_name
        self.neighbors: list[Cave] = list()

    def __repr__(self) -> str:
        return self.node_name

    def __hash__(self) -> int:
        return hash(self.node_name)

    def __eq__(self, o: Cave) -> bool:
        return self.node_name == o.node_name

    def __gt__(self, other: Cave) -> bool:
        return self.node_name > other.node_name

    def __lt__(self, other: Cave) -> bool:
        return self.node_name < other.node_name

    def is_big(self):
        return self.node_name.upper() == self.node_name

    def add_neighbor(self, neighbor: Cave):
        if neighbor not in self.neighbors:
            self.neighbors.append(neighbor)
            neighbor.add_neighbor(self)


CaveMap: TypeAlias = dict[str, Cave]


class CaveMapVisitor:

    def __init__(self, caves: CaveMap,
                 start_cave: Cave, end_cave: Cave,
                 visit_condition: Callable[[Cave, list[Cave]], bool]) -> None:
        self.start_cave = start_cave
        self.end_cave = end_cave
        self.caves = caves
        self.visit_condition = visit_condition
        self.visited_paths = []

    def list_paths(self):
        self.visit_cave(self.start_cave, [])

        return sorted([','.join([str(node) for node in visited_path])
                       for visited_path in self.visited_paths
                       ])

    def visit_cave(self, cave: Cave, visited: list[Cave]):
        visited.append(cave)
        if cave == self.end_cave:
            print(f'Found Path : {visited}')
            self.visited_paths.append(visited)
            return
        for neighbor in cave.neighbors:
            if not self.visit_condition(neighbor, visited):
                continue

            self.visit_cave(neighbor, visited.copy())


class Day12(Exercise):

    @staticmethod
    def part_one_visit_condition(cave: Cave, visited_caves: list[Cave]) -> bool:
        return cave not in visited_caves or cave.is_big()

    @staticmethod
    def part_two_visit_condition(cave: Cave, visited_caves: list[Cave]) -> bool:
        small_cave_counter = Counter([cave for cave in visited_caves if not cave.is_big()])
        return cave not in visited_caves or cave.is_big() or (cave.node_name != Cave.CAVE_START and
                                                              2 not in small_cave_counter.values())

    @staticmethod
    def build_nodes(input_data) -> CaveMap:
        caves = dict()
        for line in input_data:
            start, end = line.strip().split('-')
            if start in caves:
                start_node = caves[start]
            else:
                start_node = Cave(start)
                caves[start] = start_node

            if end in caves:
                end_node = caves[end]
            else:
                end_node = Cave(end)
                caves[end] = end_node

            start_node.add_neighbor(end_node)

        return caves

    def __init__(self, input_data: Iterable | Sized) -> None:
        super().__init__(input_data)
        self.nodes = self.build_nodes(input_data)

    def part_one(self) -> int:
        cave_map = self.nodes
        visitor = CaveMapVisitor(
            cave_map,
            cave_map[Cave.CAVE_START],
            cave_map[Cave.CAVE_END],
            self.part_one_visit_condition
        )
        return len(visitor.list_paths())

    def part_two(self) -> int:
        cave_map = self.nodes
        visitor = CaveMapVisitor(
            cave_map,
            cave_map[Cave.CAVE_START],
            cave_map[Cave.CAVE_END],
            self.part_two_visit_condition
        )
        return len(visitor.list_paths())


if __name__ == '__main__':
    inputfile_path = get_input_data_filepath(__file__)
    with open(inputfile_path) as input_file:
        exercise = Day12(input_file.readlines())
        exercise.solve_all()
