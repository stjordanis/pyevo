import copy
import random

from pyevo.functions.growth_strategies import grow_full_functionals


def mutate(
        population: set,
        node_templates: tuple,
        max_depth: int,
        max_width: int,
        grow_probability: float
) -> set:
    result = copy.deepcopy(population)
    for tree in result:
        grow_full_functionals(
            random.choice(
                list(tree.root.descendants)
                + [tree.root]
            ),
            node_templates,
            max_depth,
            max_width,
            grow_probability,
            2)
    return result


def crossover(population: set) -> set:
    one, other = list(copy.deepcopy(population)), list(copy.deepcopy(population))
    random.shuffle(other)
    for first_tree, second_tree in zip(one, other):
        first_node = random.choice(list(first_tree.root.descendants) + [first_tree.root])
        second_node = random.choice(list(second_tree.root.descendants) + [second_tree.root])

        if first_node is not first_tree.root and second_node is not second_tree.root:
            first_node.parent.children = [second_node] + \
                                         [child for child in first_node.parent.children if child is not first_node]
            second_node.parent.children = [first_node] + \
                                          [child for child in second_node.parent.children if child is not second_node]
        elif first_node is not first_tree.root:
            first_node.parent.children = [second_node] + \
                                         [child for child in first_node.parent.children if child is not first_node]
            second_tree.root = first_node
        elif second_node is not second_tree.root:
            second_node.parent.children = [first_node] + \
                                          [child for child in second_node.parent.children if child is not second_node]
            first_tree.root = second_node
    return set(one).union(set(other))
