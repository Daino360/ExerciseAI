# ExerciseAI

In questo esercizio si implementa la tecnica cutset conditioning.
Inoltre nell’esercizio si applica l’algoritmo al problema map-coloring generando mappe casuali

## Parti del lavoro riprese da altre fonti
Non avendo mai utilizzato il codice Python, ho deciso di scrivere il codice con questo linguaggio.
All'interno del codice ci sono diverse parti prese da siti online, poi riadattate al mio codice al fine di riuscire ad applicare il cutset conditioning a grafi che possono essere approssimati ad alberi.

Per rappresentare il grafo come dizionario, usare alcune semplici sue funzioni e trovare il percorso dati due vertici:
https://www.python-course.eu/graphs_python.php

Per disegnare il grafo e il grafo tagliato ho utilizzato il seguente link e la documentazione necessaria per NetworkX:
https://www.python-course.eu/networkx.php

Per poter trovare se ci sono cicli all'interno del grafo:
https://www.geeksforgeeks.org/detect-cycle-undirected-graph/
Quest' ultimo algoritmo trovava solamente se erano presenti cicli, io l'ho riadattato per far si che trovasse anche il percorso dei cicli e ritornasse poi tutti i cicli.

Infine, per il map-coloring:
https://github.com/jaymeliao/CSP-MapColoring


## Come utilizzare il codice
Per inizializzare il codice su *Jupyter Notebook* si importa il file *exercise.py*
```python 
%matplotlib qt
import exercise
``` 
Dopodichè verrà chiesto di mettere in input **1** per il **cutset conditioning**, **2** per il **map coloring**
 
* Per l'algoritmo **cutset conditioning**:
  Il codice crea un grafo casuale con un numero di vertici che va da 4 a 15, un numero di archi minore di 20 e poi trova il vertice da tagliare, dando come output (per esempio):
  ```
    The GRAPH is:
    {'a': ['b', 'c', 'd'], 'b': ['c', 'g'], 'c': ['b', 'd', 'f'], 'd': ['c', 'e'], 'e': ['d'], 'f': ['c'], 'g': ['b']}
    -------------------------------------------------
    The vertex that must be cut is a
    -------------------------------------------------
    The CUT GRAPH is: 
    {'a': [], 'b': ['c', 'g'], 'c': ['b', 'd', 'f'], 'd': ['c', 'e'], 'e': ['d'], 'f': ['c'], 'g': ['b']}
  ```
    
* Per il **map coloring**:
  Dopo aver messo in input il valore 2 per il map coloring, è necessario introdurre il numero di colori come altro input da tastiera. Questo si trova sotto la finestra che si   andrà a creare. Messo in input il numero dei colori, da come output lo stesso che per il cutset conditioning, con l'aggiunta di un dizionario dove per ogni nodo sono specificati dei numeri che indicano i colori diversi per nodi connessi (per esempio):
  ```
    {'f1H': 1, 'M4j': 1, 'T4O': 1, 'J2o': 2, 'b8Q': 1, 'k3Z': 1, 'U8n': 2}
  ```
  
Se si desidera applicare il cutset conditioning ad un certo grafo sarà necessario quindi:
* **Importare** *Graph* da *exercise* 
  ```python
  from exercise import Graph
  ```
* **Immettere** il grafo al quale si desidera applicare il cutset conditioning e **creare** l'oggetto del grafo:
  ```python
  graph1 = { "a" : ["b","c","d"],
          "b" : ["a", "c","g"],
          "c" : ["a", "b", "d", "f"],
          "d" : ["a","c","e"],
          "e" : ["d"],
          "f" : ["c"],
          "g" : ["b"]
        }
  g1=Graph(graph1)
  ```
* **Disegnare** il grafo con la libreria inizializzata precedentemente `%matplotlib qt`:
  ```python
  exercise.draw_graph(graph1, False)
  ```
* **Controllare** se ci sono cicli e quindi **creare** un grafo dopo il taglio. Questo ci renderà in output lo stesso [risultato] visto prima :
  ```python
  g1.isCyclic(False)
  ```
