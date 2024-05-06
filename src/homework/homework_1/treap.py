import copy
from collections.abc import MutableMapping
from random import random
from typing import Any, Generic, Iterator, Optional, TypeVar

K = TypeVar("K")
V = TypeVar("V")


class Node(Generic[K, V]):
    def __init__(self, key: K, value: V, priority: float, left: Optional["Node"], right: Optional["Node"]) -> None:
        self.key: K = key
        self.value: V = value
        self.priority: float = priority
        self.left: Optional[Node] = left
        self.right: Optional[Node] = right

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, Node):
            raise TypeError(f"Comparison of objects of the {type(self)} and {type(other)} is not supported")

        return self.key == other.key and self.value == other.value

    def __ne__(self, other: Any) -> bool:
        return not (self == other)


class CartesianTree(MutableMapping):
    def __init__(self) -> None:
        self.root: Optional[Node] = None
        self.length: int = 0

    def __len__(self) -> int:
        return self.length

    def __getitem__(self, key: K) -> Any:
        def recursion(tree_node: Optional[Node], key: K) -> Optional[V]:
            if tree_node is None:
                raise KeyError(f"The element could not be found by key {key}")

            if tree_node.key == key:
                return tree_node.value
            else:
                return recursion(tree_node.left, key)

        first_tree, second_tree = split(self, key)
        return recursion(second_tree.root, key)

    def __setitem__(self, key: K, value: V) -> None:
        first_tree, second_tree = split(self, key)
        node = Node(key, value, random(), None, None)
        node_tree = CartesianTree()
        node_tree.root = node

        try:
            del second_tree[key]
        except KeyError:
            self.length += 1

        self.root = merge(merge(first_tree, node_tree), second_tree).root

    def __delitem__(self, key: K) -> None:
        def recursion(tree_node: Optional[Node], key: K) -> Optional[Node]:
            if tree_node is not None:
                if tree_node.key < key:
                    return recursion(tree_node.right, key)
                elif tree_node.key > key:
                    return recursion(tree_node.left, key)
                else:
                    return merge_nodes(tree_node.left, tree_node.right)
            else:
                raise KeyError(f"The element could not be found by key {key}")

        self.root = recursion(self.root, key)

    def __iter__(self) -> Iterator:
        if self.root is None:
            return iter([])

        def recursion(current_node: Node) -> Iterator:
            if current_node.left is not None:
                yield from recursion(current_node.left)
            yield current_node.key
            if current_node.right is not None:
                yield from recursion(current_node.right)

        yield from recursion(current_node=self.root)


def merge_nodes(lower_node: Optional[Node], higher_node: Optional[Node]) -> Optional[Node]:
    if lower_node is None:
        return higher_node
    if higher_node is None:
        return lower_node

    if lower_node.priority > higher_node.priority:
        node = lower_node
        node.right = merge_nodes(node.right, higher_node)

        return node
    else:
        node = higher_node
        node.left = merge_nodes(lower_node, higher_node.left)

        return node


def merge(lower_tree: CartesianTree, higher_tree: CartesianTree) -> CartesianTree:
    node = merge_nodes(lower_tree.root, higher_tree.root)
    output_tree = CartesianTree()
    output_tree.root = node

    return output_tree


def split_nodes(node: Optional[Node], key: K) -> tuple[Optional[Node], Optional[Node]]:
    if node is None:
        return None, None

    lower_node: Optional[Node]
    higher_node: Optional[Node]

    node_copy = copy.copy(node)

    if node_copy.key < key:
        lower_node = node_copy
        left_subnode, higher_node = split_nodes(lower_node.right, key)

        lower_node.right = left_subnode

    else:
        higher_node = node_copy
        lower_node, right_subnode = split_nodes(higher_node.left, key)

        higher_node.left = right_subnode

    return lower_node, higher_node


def split(tree: CartesianTree, key: K) -> tuple[CartesianTree, CartesianTree]:
    lower_node, higher_node = split_nodes(tree.root, key)
    lower_tree = CartesianTree()
    lower_tree.root = lower_node
    higher_tree = CartesianTree()
    higher_tree.root = higher_node

    return lower_tree, higher_tree
