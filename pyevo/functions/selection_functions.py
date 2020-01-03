import copy
import functools
import itertools
import operator
import random


def select_elitist(population: set, quantity: int, metric: str = 'fitness') -> set:
    return set(sorted(population, key=operator.attrgetter(metric))[:quantity])


def select_proportionate(population: set, quantity: int, metric: str = 'fitness') -> set:
    selection = set()
    for specimen in random.choices(list(
            itertools.chain.from_iterable([[tree] * getattr(tree, metric) for tree in population])),
            k=quantity):
        selection.add(copy.deepcopy(specimen))
    assert len(selection) == quantity
    return selection


def select_stochastic_universal(population: set, quantity: int, metric: str = 'fitness') -> set:
    sum_of_fitness_values = functools.reduce(
        lambda current_sum, next_tree: current_sum + getattr(next_tree, metric),
        [0] + list(population))

    initial_value = float(0)
    while initial_value == 0 or initial_value == (sum_of_fitness_values / quantity):
        initial_value = random.uniform(0, sum_of_fitness_values / quantity)

    sample_space = list(itertools.chain.from_iterable(
        [[tree] * getattr(tree, metric) for tree in sorted(population, key=operator.attrgetter(metric))]))

    values = [int(initial_value + (n * sum_of_fitness_values / quantity)) for n in range(quantity)]

    result = set()
    for value in values:
        result.add(sample_space[value])

    return result


def select_tournament(population: set,
                      quantity: int,
                      num_of_tournaments: int,
                      number_of_participants: int,
                      metric: str = 'fitness'
                      ) -> set:
    assert (quantity / num_of_tournaments) % 1 == 0

    result = set()
    for tournament in range(num_of_tournaments):
        result.update(sorted(random.choices(population, k=number_of_participants),
                             key=operator.attrgetter(metric))[:int(quantity / num_of_tournaments)])

    assert len(result) == quantity
    return result


def select_best(population: set, metric: str = 'fitness') -> set:
    return set(max(population, key=operator.attrgetter(metric)))
