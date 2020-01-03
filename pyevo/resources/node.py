import functools


class Node:
    def __init__(self, **kwargs):
        self.depth = kwargs.get("depth", 0)
        self.logic = kwargs.get("logic", lambda: None)
        self.number = kwargs.get("number", '0')
        self.parent = kwargs.get("parent", None)

    @property
    def children(self) -> list:
        return list()

    @children.setter
    def children(self, children: list) -> None:
        pass

    @property
    def descendants(self) -> set:
        return functools.reduce(lambda union, next_child: union.union(next_child.descendants),
                                self.children,
                                set(self.children))

    @property
    def parent(self):
        return self._parent

    @parent.setter
    def parent(self, parent):
        self._parent = parent


class FunctionalNode(Node):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.children = kwargs.get('children', list())

    def __call__(self):
        return self.logic(self.children)

    @property
    def children(self) -> list:
        return self._children

    @children.setter
    def children(self, children: list) -> None:
        self._children = list()
        number = 0
        for child in children:
            self._children.append(child)
            child.number = self.number + str(number)
            number += 1
            child.parent = self


class TerminalNode(Node):
    def __call__(self):
        return self.logic()

    @property
    def children(self):
        return list()
