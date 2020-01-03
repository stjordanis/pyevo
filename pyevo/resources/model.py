import collections
import typing

from pyevo.config import config
from pyevo.functions.growth_strategies import grown_full_functionals
from pyevo.resources.node import FunctionalNode, TerminalNode
from pyevo.functions.operator_functions import *
from pyevo.functions.selection_functions import *
from pyevo.resources.tree import Tree

ResultData = collections.namedtuple('ResultData',
                                    'run generation '
                                    'avg_fitness max_fitness target')


class Model:
    """Generic model example for GP derived algorithms.

    General steps:
    1. Initializing a population
    2. (Re)Initializing the loop
    3. Performing selections and operations
    4. Cycling the loop.
    """

    def __init__(self,
                 node_templates: tuple,
                 fitness_function: typing.Callable = None,
                 ):
        """Initializer function setting attributes."""
        self.fitness_function = fitness_function
        self.node_templates = node_templates

        self.population = None

    def _initialize_population(self,
                               population: set = None,
                               population_size: int = None):
        """Algorithm step to initialize the population that will be operated on."""
        self.population = population or set()

        if population_size and not population:
            for tree in range(population_size):
                choice = random.choices(
                    self.node_templates,
                    weights=[template.weight for template in self.node_templates],
                    k=1
                )[0]
                if choice.terminal:
                    self.population.add(Tree(root=TerminalNode(logic=choice.logic)))
                else:
                    self.population.add(Tree(root=grown_full_functionals(
                        FunctionalNode(logic=choice.logic),
                        self.node_templates,
                        10, 10, .5, 2)))

    def _initialize_loop(self):
        """Algorithm step to calculate all fitnesses and check exit conditions."""
        for tree in self.population:
            tree.calculate_fitness(fitness_function=self.fitness_function)

    def genetic_programming(self,
                            run_count: int,
                            population_size: int,
                            select_for_reproduction: int,
                            select_for_mutation_crossover: int,
                            number_of_generations: int,
                            selection_strategy: typing.Callable = select_proportionate,
                            max_grow_depth: int = 3,
                            max_grow_width: int = 10,
                            grow_probability: float = .5,
                            fitness_scale: float = 1.0,
                            target_label: str = None
                            ) -> typing.List[ResultData]:

        result = list()

        for run in range(run_count):
            self._initialize_population(population_size=population_size)
            self._initialize_loop()

            for generation in range(number_of_generations):
                self.population = \
                    selection_strategy(self.population, select_for_reproduction).union(
                        crossover(mutate(selection_strategy(self.population, select_for_mutation_crossover),
                                         self.node_templates, max_grow_depth, max_grow_width, grow_probability)))
                self._initialize_loop()
                avg_fitness = (sum(tree.fitness for tree in self.population) / len(self.population)) / (fitness_scale or 1.0)
                max_fitness = (max(tree.fitness for tree in self.population)) / (fitness_scale or 1.0)
                result.append(ResultData(
                    run,
                    generation,
                    avg_fitness,
                    max_fitness,
                    target_label
                ))

        return result
