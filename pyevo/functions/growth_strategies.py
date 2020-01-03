import random

from pyevo.resources.node import Node, TerminalNode, FunctionalNode


def grow_random(
        node: Node,
        node_templates: tuple,
        max_depth: int,
        max_children: int,
        grow_probability: float
) -> None:
    if isinstance(node, TerminalNode) \
            and node.depth < max_depth:
        return

    while random.random() > grow_probability \
            and not len(node.children) > max_children:
        selected_node_template = random.choices(
            [template for template in node_templates],
            weights=[template.weight
                     for template in node_templates],
            k=1
        )[0]

        if selected_node_template.terminal:
            node.children += \
                list((TerminalNode(
                    logic=selected_node_template.logic
                    ),))
        else:
            node.children += \
                list((FunctionalNode(
                    logic=selected_node_template.logic
                    ),))

    for child in node.children:
        grow_random(
            child, node_templates, max_depth,
            max_children, grow_probability
        )


def grown_random(node: Node, node_templates: tuple, max_depth: int, max_width: int, grow_probability: float) -> Node:
    grow_random(node, node_templates=node_templates, max_depth=max_depth, max_children=max_width,
                grow_probability=grow_probability)
    return node


def grow_full_functionals(node: Node,
                          node_templates: tuple,
                          max_depth: int,
                          max_width: int,
                          grow_probability: float,
                          functional_min_leaves: int) -> None:
    grown_random(node, node_templates, max_depth, max_width, grow_probability)
    for descendant in (node.descendants.union({node})):
        if isinstance(descendant, FunctionalNode) and len(descendant.children) < 2:
            descendant.children = random.choices(
                [TerminalNode(logic=node_template.logic) for node_template in node_templates if node_template.terminal],
                weights=[node_template.weight for node_template in node_templates if node_template.terminal],
                k=functional_min_leaves
            )


def grown_full_functionals(node: Node,
                           node_templates: tuple,
                           max_depth: int,
                           max_width: int,
                           grow_probability: float,
                           functional_min_leaves: int) -> Node:
    grow_full_functionals(node, node_templates, max_depth, max_width, grow_probability, functional_min_leaves)
    return node
