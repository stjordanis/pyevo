import typing

from pyevo.resources.node import Node


class Tree:
    def __init__(self, **kwargs):
        self.fitness = int()
        self.complexity = int()
        self.novelty = int()
        self.root = kwargs.get('root', Node())

    def __hash__(self):
        return self.root.__hash__()

    def calculate_fitness(self, fitness_function: typing.Callable) -> None:
        self.fitness = fitness_function(self.root())

    def calculate_complexity(self, complexity_function: typing.Callable) -> None:
        self.complexity = complexity_function(self.root())

    def calculate_novelty(self, novelty_function: typing.Callable) -> None:
        self.novelty = novelty_function(self.root())

