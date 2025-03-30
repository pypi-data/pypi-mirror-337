from .BinaryTreeNode import BinaryTreeNode
import networkx as nx
import matplotlib.pyplot as plt

class BinaryTree:
    """
    A class representing a binary tree.
    It supports insertion, deletion, and traversal operations.
    """
    def __init__(self):
        self.root_node: BinaryTreeNode = None
        self.size = 0
        self.nodes = []

    def insert(self, node: BinaryTreeNode):
        """
        Insert a node into the binary tree.
        :param node: BinaryTreeNode
        :return:
        """
        if node.level == 0 and self.root_node is not None:
            raise ValueError("Root node already exists")
        if node.level == 0:
            self.root_node = node
        else:
            if node.level == 1:
                node.parent = self.root_node
            elif node.level > 1 and node.parent.level == 0:
                raise ValueError("Parent node must be at level 1 to have root as parent")
            if len(self.nodes) < 2 ** node.level:
                self.nodes.append(node)
                children_at_level = [child for child in self.nodes if child.level == node.level]
                for child in children_at_level:
                    if child.level == node.level and child.parent == node.parent:
                        child.sibling = node
                        node.sibling = child
            else:
                raise ValueError("Maximum number of children reached for this level")
        self.size += 1

    def delete(self, node=None, value=None):
        """
        Delete a node from the binary tree while preserving the tree's structure.
        :param node: The node to delete.
        :param value: The value of the node to delete.
        :return:
        """
        if node is None and value is None:
            print("Either node or value must be provided")
            return

        if node is None:
            node = self._find(self.root_node, value)
            if not node:
                print("Node not found")
                return

        rightmost_leaf = self._find_rightmost_leaf()
        if node == rightmost_leaf:
            if node.parent:
                if node.parent.left == node:
                    node.parent.left = None
                else:
                    node.parent.right = None
            else:
                self.root_node = None
        else:
            node.value = rightmost_leaf.value
            if rightmost_leaf.parent.left == rightmost_leaf:
                rightmost_leaf.parent.left = None
            else:
                rightmost_leaf.parent.right = None

        self.size -= 1

    def _find(self, current, value):
        if not current:
            return None
        if current.value == value:
            return current
        elif value < current.value:
            return self._find(current.left, value)
        else:
            return self._find(current.right, value)

    def _find_rightmost_leaf(self):
        current = self.root_node
        while current.right:
            current = current.right
        return current

    def in_order_dfs(self):
        """
        Perform an in-order depth-first traversal of the binary tree.
        :return: A list of nodes in in-order.
        """

        def _in_order_dfs(node):
            if node is None:
                return []
            return _in_order_dfs(node.left) + [node] + _in_order_dfs(node.right)

        return _in_order_dfs(self.root_node)

    def pre_order_dfs(self):
        """
        Perform a pre-order depth-first traversal of the binary tree.
        :return: A list of nodes in pre-order.
        """

        def _pre_order_dfs(node):
            if node is None:
                return []
            return [node] + _pre_order_dfs(node.left) + _pre_order_dfs(node.right)

        return _pre_order_dfs(self.root_node)

    def post_order_dfs(self):
        """
        Perform a post-order depth-first traversal of the binary tree.
        :return: A list of nodes in post-order.
        """

        def _post_order_dfs(node):
            if node is None:
                return []
            return _post_order_dfs(node.left) + _post_order_dfs(node.right) + [node]

        return _post_order_dfs(self.root_node)

    def breadth_first_search(self):
        """
        Perform a breadth-first traversal of the binary tree.
        :return: A list of nodes in breadth-first order.
        """
        if not self.root_node:
            return []

        queue = [self.root_node]
        bfs_order = []

        while queue:
            current_node = queue.pop(0)
            bfs_order.append(current_node)

            if current_node.left:
                queue.append(current_node.left)
            if current_node.right:
                queue.append(current_node.right)

        return bfs_order

    def search(self, value):
        """
        Search for a node with the given value in the binary tree.
        :param value: The value to search for.
        :return: The node if found, otherwise None.
        """

        def _search(node, value):
            if node is None:
                return None
            if node.value == value:
                return node
            left_result = _search(node.left, value)
            if left_result is not None:
                return left_result
            return _search(node.right, value)

        return _search(self.root_node, value)

    def _pretty_print(self):
        if not self.root_node:
            return "<empty tree>"

        levels = []
        self._collect_levels(self.root_node, 0, levels)
        result = ""
        max_level = len(levels) - 1
        max_width = 2 ** max_level

        for level in range(max_level + 1):
            level_nodes = levels[level]
            space_between = max_width // (2 ** level)
            result += " " * (space_between // 2)
            result += (" " * space_between).join(str(node) for node in level_nodes)
            result += "\n"
        return result

    def _collect_levels(self, node, level, levels):
        if len(levels) == level:
            levels.append([])
        levels[level].append(node)
        if node.left:
            self._collect_levels(node.left, level + 1, levels)
        if node.right:
            self._collect_levels(node.right, level + 1, levels)

    def draw(self, node_size=2000, node_color="skyblue", font_size=10, font_weight="bold", arrows=False):
        if not self.root_node:
            print("Tree is empty")
            return

        G = nx.DiGraph()
        pos = {}
        labels = {}

        def add_edges(node, x, y, dx):
            if node:
                node_id = id(node)
                G.add_node(node_id)
                pos[node_id] = (x, y)
                labels[node_id] = str(node.value)
                if node.left:
                    G.add_edge(node_id, id(node.left))
                    add_edges(node.left, x - dx, y - 1, dx / 2)
                if node.right:
                    G.add_edge(node_id, id(node.right))
                    add_edges(node.right, x + dx, y - 1, dx / 2)

        add_edges(self.root_node, 0, 0, 1)
        plt.figure(figsize=(12, 8))
        nx.draw(G, pos, labels=labels, with_labels=True, node_size=node_size, node_color=node_color, font_size=font_size,
                font_weight=font_weight, arrows=arrows)
        plt.show()


    def __str__(self):
        return self._pretty_print()