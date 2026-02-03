# ExerciseAI

This project implements the **cutset conditioning** technique and applies it to the **map coloring** problem by generating both predefined and random maps.

The goal is to approximate general graphs as trees by identifying and cutting cycles, then solving the coloring problem on the resulting structure.

---

## 1 - External Sources and References

This project was also an opportunity to deepen my Python skills.  
Some parts of the code were adapted from online resources and then modified to fit the specific requirements of applying cutset conditioning to graphs that can be approximated as trees.

### Graph representation and basic utilities
Used to represent graphs as dictionaries, perform basic operations, and find paths between nodes:

https://www.python-course.eu/graphs_python.php

### Graph visualization
Used for drawing graphs with NetworkX:

https://www.python-course.eu/networkx.php

### Cycle detection in undirected graphs
Used to detect cycles in the graph:

https://www.geeksforgeeks.org/detect-cycle-undirected-graph/

---

## 2 - How to Use the Code

To run the project in a *Jupyter Notebook*, import the `exerciseAI.py` file:

```python
%matplotlib qt
import exerciseAI
````

---

### 2.1 - Non-random Graphs

To apply **cutset conditioning** to a predefined graph, after importing `exerciseAI` and initializing `%matplotlib qt`:

#### Define the graph

```python
graph3colors = {
    'a': ['e', 'b'], 
    'b': ['c', 'a'],
    'c': ['b', 'f'],
    'd': ['g', 'f'],
    'e': ['a', 'f', 'g'],
    'f': ['e', 'c', 'd'],
    'g': ['d', 'e']
}
```

#### Draw the graph

```python
exerciseAI.draw_graph(graph3colors)
```

#### Apply cutset conditioning

This step cuts the graph if cycles are detected:

```python
exerciseAI.cutset_conditioning(graph3colors)
```

Example output:

```
The graph is {'a': ['e', 'b'], 'b': ['c', 'a'], 'c': ['b', 'f'], 'd': ['g', 'f'], 'e': ['a', 'f', 'g'], 'f': ['e', 'c', 'd'], 'g': ['d', 'e']}
-------------------------------------------------------------------------------------------------
The cutset part is: {'e': []}
-------------------------------------------------------------------------------------------------
The topological sort is: {'e': ['a', 'f', 'g'], 'a': ['b'], 'f': ['c', 'd'], 'g': ['d'], 'b': ['c'], 'c': [], 'd': []}
The color of each node is: {'e': '1', 'a': '2', 'f': '2', 'g': '2', 'b': '1', 'c': '3', 'd': '1'}
```

---

### Map Coloring

To apply the **map coloring** technique:

1. Initialize `tp_sort` with the topological order obtained in the previous step.
2. Call `tree_solver(tp_sort, number_of_colors)`.

Example:

```python
tp_sort = {
    'e': ['a', 'f', 'g'],
    'a': ['b'],
    'f': ['c', 'd'],
    'g': ['d'],
    'b': ['c'],
    'c': [],
    'd': []
}

exerciseAI.tree_solver(tp_sort, 3)
```

Output:

```
The color of each node is: {'e': '1', 'a': '2', 'f': '2', 'g': '2', 'b': '1', 'c': '3', 'd': '1'}
```

Each node is assigned a color such that no two adjacent nodes share the same color.

---

### 2.2 - Random Graphs

To generate a random graph with a given number of nodes, call:

```python
exerciseAI.generate_graph(numero_vertici)
```

The function:

* Generates a random graph with the specified number of vertices
* Limits the number of edges to fewer than 20
* Asks the user to input the number of colors (`How many colors?`)
* Identifies the cutset
* Colors the graph starting from the cutset nodes

Example output:

```
The graph is {'a': ['e', 'b'], 'b': ['c', 'a'], 'c': ['b', 'f'], 'd': ['g', 'f'], 'e': ['a', 'f', 'g'], 'f': ['e', 'c', 'd'], 'g': ['d', 'e']}
-------------------------------------------------------------------------------------------------
The cutset part is: {'e': []}
-------------------------------------------------------------------------------------------------
The topological sort is: {'e': ['a', 'f', 'g'], 'a': ['b'], 'f': ['c', 'd'], 'g': ['d'], 'b': ['c'], 'c': [], 'd': []}
The color of each node is: {'e': '1', 'a': '2', 'f': '2', 'g': '2', 'b': '1', 'c': '3', 'd': '1'}
```
