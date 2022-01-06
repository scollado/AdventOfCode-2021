from __future__ import annotations

from abc import abstractmethod
from queue import PriorityQueue
from typing import Callable

from aocutils.matrix import Matrix


def manhattan_distance(a: Matrix.Cell, b: Matrix.Cell) -> int:
    return abs(a.x - b.x) + abs(a.y - b.y)


class PathFinder:
    @abstractmethod
    def find_path_to(self, target) -> list:
        pass


class Dijkstra(PathFinder):
    """
    Dijkstra Path finding
    """

    def __init__(self, matrix: Matrix, start: Matrix.Cell):
        self.start = start
        self.matrix = matrix

    def find_path_to(self, target: Matrix.Cell) -> list[Matrix.Cell]:
        frontier = PriorityQueue()
        frontier.put((0, self.start))
        came_from: dict[Matrix.Cell, Matrix.Cell] = dict()
        cost = dict()
        cost[self.start] = 0
        while not frontier.empty():
            current: Matrix.Cell = frontier.get()[1]

            if current == target:
                break

            for neighbor in current.neighbors():
                new_cost = cost[current] + int(neighbor.value)
                if neighbor not in cost or new_cost < cost[neighbor]:
                    cost[neighbor] = new_cost
                    priority = new_cost
                    frontier.put((priority, neighbor))
                    came_from[neighbor] = current

        return self._rebuild_path(target, came_from)

    def _rebuild_path(self, to: Matrix.Cell, came_from: dict[Matrix.Cell, Matrix.Cell]) -> list[Matrix.Cell]:
        current = to
        path: list[Matrix.Cell] = []
        while current != self.start:
            path.append(current)
            current = came_from[current]
        path.append(self.start)
        path.reverse()

        return path


class AStar(Dijkstra):
    """
    A* Path finding
    """

    def find_path_to(self,
                     target: Matrix.Cell,
                     heuristic: Callable[[Matrix.Cell, Matrix.Cell], float | int] = None) -> list[Matrix.Cell]:
        if heuristic is None:
            heuristic = manhattan_distance

        frontier = PriorityQueue()
        frontier.put((0, self.start))
        came_from: dict[Matrix.Cell, Matrix.Cell] = dict()
        cost = dict()
        cost[self.start] = 0

        while not frontier.empty():
            current: Matrix.Cell = frontier.get()[1]

            if current == target:
                break

            for neighbor in current.neighbors():
                new_cost = cost[current] + int(neighbor.value)
                if neighbor not in cost or new_cost < cost[neighbor]:
                    cost[neighbor] = new_cost
                    priority = new_cost + heuristic(target, neighbor)
                    frontier.put((priority, neighbor))
                    came_from[neighbor] = current

        return self._rebuild_path(target, came_from)
