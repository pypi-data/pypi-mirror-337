# python-binary-tree
A simple implementation of a binary tree in Python.

## Installation
```bash 
pip install python-binary-tree
```
## Usage
```python
from binary_tree import BinaryTree
from binary_tree import BinaryTreeNode
# Create a binary tree and add nodes
bt = BinaryTree()
# Create nodes with values
root = BinaryTreeNode(0)
node1 = BinaryTreeNode(1)
node2 = BinaryTreeNode(2)
node3 = BinaryTreeNode(3)
node4 = BinaryTreeNode(4)
node5 = BinaryTreeNode(5)

# Add relationships between nodes
root.add_left(node1)
root.add_right(node2)

node1.add_right(node3)
node2.add_right(node4)
node1.add_left(node5)

# Insert nodes into the binary tree
bt.insert(root)
bt.insert(node1)
bt.insert(node2)

bt.draw()
```
### Example Output
![exampleplot.png](exampleplot.png)

