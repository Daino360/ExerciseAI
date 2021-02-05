# ExerciseAI

In questo esercizio si implementa la tecnica **cutset conditioning**.
Inoltre nell’esercizio si applica l’algoritmo al problema **map coloring** generando mappe casuali

## 1 - Parti del lavoro riprese da altre fonti
Non avendo mai utilizzato il codice Python, ho deciso di scrivere il codice con questo linguaggio.
All'interno del codice ci sono diverse parti prese da siti online, poi riadattate al mio codice al fine di riuscire ad applicare il cutset conditioning a grafi che possono essere approssimati ad alberi.

Per rappresentare il grafo come dizionario, usare alcune semplici sue funzioni e trovare il percorso dati due vertici:

https://www.python-course.eu/graphs_python.php

Per disegnare il grafo ho utilizzato il seguente link e la documentazione necessaria per NetworkX:

https://www.python-course.eu/networkx.php

Per poter trovare se ci sono cicli all'interno del grafo:

https://www.geeksforgeeks.org/detect-cycle-undirected-graph/

## 2 - Come utilizzare il codice
Per inizializzare il codice su *Jupyter Notebook* si importa il file *exerciseAI.py*
```python 
%matplotlib qt
import exerciseAI
```  
### 2.1 - Grafi non casuali
Se si desidera applicare il **cutset conditioning** ad un grafo non casuale sarà necessario, dopo aver importato `exerciseAI` e aver inizializzato `%matplotlib qt`:

* **Immettere** il grafo al quale si desidera applicare l'algoritmo:
  ```python
  graph3colors = {'a': ['e', 'b'], 
  'b': ['c', 'a'],
  'c': ['b', 'f'],
  'd': ['g','f'],
  'e': ['a', 'f', 'g'],
  'f': ['e', 'c','d'],
  'g': ['d', 'e']
  }
  ```

* **Disegnare** il grafo con la libreria inizializzata precedentemente `%matplotlib qt`:
  ```python
  exerciseIA.draw_graph(graph3colors)
  ```
* **Applicare** l'algoritmo **cutset conditioning**, che taglia il grafo se presenta dei cicli:
  ```python
  exerciseIA.cutset_conditioning(graph3colors)
  ```
  Questo ci renderà in output:
  ```
    The graph is {'a': ['e', 'b'], 'b': ['c', 'a'], 'c': ['b', 'f'], 'd': ['g', 'f'], 'e': ['a', 'f', 'g'], 'f': ['e', 'c', 'd'], 'g': ['d', 'e']}
    -------------------------------------------------------------------------------------------------
    The cutset part is: {'e': []}
    -------------------------------------------------------------------------------------------------
    The topological sort is: {'e': ['a', 'f', 'g'], 'a': ['b'], 'f': ['c', 'd'], 'g': ['d'], 'b': ['c'], 'c': [], 'd': []}
    The color of each node is: {'e': '1', 'a': '2', 'f': '2', 'g': '2', 'b': '1', 'c': '3', 'd': '1'}
  ```
  
Successivamente, per applicare la tecnica del **map_coloring**:

* **Inizializzare** *tp_sort* con l'ordine topologico trovato al passo precedente e **chiamare** `tree_solver(tp_sort,numero_colori)`,inserendo il numero di colori con il quale si vuole colorare il grafo. Per esempio:
  ```python
  tp_sort = {'e': ['a', 'f', 'g'],
   'a': ['b'],
   'f': ['c', 'd'],
   'g': ['d'],
   'b': ['c'],
   'c': [],
   'd': []}
  exerciseIA.tree_solver(tp_sort, 3)
  ```
  Questo renderà come output:
  
  ```
  The color of each node is: {'e': '1', 'a': '2', 'f': '2', 'g': '2', 'b': '1', 'c': '3', 'd': '1'}
  ```
  Dove ad ogni vertice viene assegnato un colore in modo tale che non si abbia due vertici connessi dello stesso colore

### 2.2 - Grafi casuali con un numero di nodi dato in input
Per generare grafi casuali, si chiama la funzione:
```python
exerciseAI.generate_graph(numero_vertici)
```
e il codice crea un grafo casuale con il numero di vertici dato in input e un numero di archi minore di 20. Dopodichè viene chiesto di immettere in input il numero di colori da utilizzare per colorare i nodi (`How many colors?`). Infine, trova i vertici da tagliare e colora il grafo partendo dai nodi del taglio, dando come output per esempio:
  ```
    The graph is {'a': ['e', 'b'], 'b': ['c', 'a'], 'c': ['b', 'f'], 'd': ['g', 'f'], 'e': ['a', 'f', 'g'], 'f': ['e', 'c', 'd'], 'g': ['d', 'e']}
    -------------------------------------------------------------------------------------------------
    The cutset part is: {'e': []}
    -------------------------------------------------------------------------------------------------
    The topological sort is: {'e': ['a', 'f', 'g'], 'a': ['b'], 'f': ['c', 'd'], 'g': ['d'], 'b': ['c'], 'c': [], 'd': []}
    The color of each node is: {'e': '1', 'a': '2', 'f': '2', 'g': '2', 'b': '1', 'c': '3', 'd': '1'}
  ```
