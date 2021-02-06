"""
Cutset Conditioning and Map Coloring by Stefano Dainelli
    
graph3colors = {'a': ['e', 'b'],
                'b': ['c', 'a'],
                'c': ['b', 'f'],
                'd': ['g','f'],
                'e': ['a', 'f', 'g'],
                'f': ['e', 'c','d'],
                'g': ['d', 'e']
                }


graph2colors = {'a': ['e', 'b', 'c'],
                'b': ['a','d'],
                'c': ['a', 'd'],
                'd': ['e', 'c','b'],
                'e': ['d', 'a']
                }
        

graph4colors = {'a': ['g', 'c'],
                'b': ['g', 'f', 'e'],
                'c': ['d', 'g', 'a'],
                'd': ['e', 'c', 'g'],
                'e': ['f', 'd', 'g', 'b'],
                'f': ['e', 'b', 'g'],
                'g': ['b', 'e', 'a', 'f', 'd', 'c']
                }   
"""
#====================Libraries==========================
import random #library for generate random values
import copy #to create a copy of a graph
import string #library used for input
import networkx as nx #library used for drawing graphs
import matplotlib.pyplot as plt #library for generate graphs
import warnings #to ignore a warining message
warnings.filterwarnings("ignore")

#================General Functions======================= 
#function that generate a random graph

def generate_graph(num_vertex):
        
    #The number of edges is not bigger than 20 
    #to have a nearly-tree graph almost everytime
    if num_vertex < 7:
        max_edges = (num_vertex)*(num_vertex-1)/2
    else:
        max_edges = (num_vertex)*2-2
    num_edges = random.randrange(num_vertex, max_edges)
    
    while num_edges > 21:
        num_edges = random.randrange(num_vertex, max_edges)
    
    #Create a new object g that is the graph as dictionary
    graph_dict={}
    g=Graph(graph_dict)
    edges=[]
    
    #Create a different name for each vertex 
    #and create random edges
    for i in range(num_vertex):
        new_vertex = random.choice(string.ascii_letters)+random.choice(string.digits)+random.choice(string.ascii_letters)
        g.add_vertex(new_vertex)
    for i in range(num_edges):
        vert1 = random.choice(list(graph_dict.keys()))
        vert2 = random.choice(list(graph_dict.keys()))
        while vert2 == vert1:
            vert2 = random.choice(list(graph_dict.keys()))
        g.add_edge(vert1,vert2,edges)
    
    draw_graph(graph_dict)
    num_colors = int(input("How many colors?"))
    roots = g.vertex_max_edges(graph_dict)
    root = random.choice(roots)
    
    #Find a topological sort
    tp_sort = topological_sort(graph_dict, root)
    
    #Check if there are cycles
    if g.yet_cycles(graph_dict) == False:
        print("Cutset conditioning no needed")
        print ('The topological sort is:',tp_sort)
    else:
        tp_sort = cutset_conditioning(graph_dict, roots)
    
    tree_solver(tp_sort, num_colors) #for map-coloring domains are the colors
    
    
#Function to draw Graphs with matplotlib    
def draw_graph(graphToDraw):
                        
    f1 = plt.figure(1)
    G=nx.Graph()
    g=Graph(graphToDraw)
    # a list of nodes:
    G.add_nodes_from(list(graphToDraw.keys()))
    G.add_edges_from(list(g.edges()))
    plt.clf()
    nx.draw_planar(G, with_labels=True, node_size=1500, node_color='skyblue')
    plt.savefig("my_graph.png") # save graph
    plt.show() # display

#Function that find a small cutset if there are cycles,
#This function also call herself if the topological sort
#is not a good one, changing the root
def cutset_conditioning(graph, roots = [], i = 0):
    g = Graph(graph)
    print('The graph is',graph)
    cut_graph = {}
    c = Graph(cut_graph)
    maybe_tree = copy.deepcopy(graph)
    mt = Graph(maybe_tree)
    tp_list=[]
    roots = g.vertex_max_edges(graph)
    
    #First time root take first element of list roots
    root = roots[i]
    #Find a topological sort with the first root
    tp_sort = topological_sort(graph, root) 
    for parent in tp_sort:
        tp_list.append(parent)
    
    #Find the tree after the cutset
    for parent in tp_list:
        c.add_vertex(parent)
        maybe_tree.pop(parent, None)
        for node in maybe_tree:
            if parent in maybe_tree[node]:
                maybe_tree[node].remove(parent)
        
        #if there are no more cycles
        if mt.yet_cycles(maybe_tree) == False:
            for node in maybe_tree:
                if maybe_tree[node]==[]:
                    for vertex in graph[node]:
                        if vertex in cut_graph:
                            c.add_vertex(node)
        
        #if the cutset part is bigger than half number of nodes
        #it retry with another root
        if len(cut_graph.keys())>len(graph.keys())/2:
            roots.remove(root)
            cutset_conditioning(graph, roots, i = i+1)
            return
        #else return the cutset part
        elif mt.yet_cycles(maybe_tree) == False:
            print('-------------------------------------------------------------------------------------------------')
            print('The cutset part is:',cut_graph)
            print('-------------------------------------------------------------------------------------------------')
            print ('The topological sort is:',tp_sort)
            return tp_sort    

#Find a topological sort given a root        
def topological_sort(graph, root):
    tp_list = {}
    tp = Graph(tp_list)
    tp.add_vertex(root)
    for vertex in graph[root]:
        tp.add_vertex(vertex)
    for vertex in graph:       
        for vertex2 in graph[vertex]:
            if vertex2 not in tp_list.keys():
                tp.add_vertex(vertex2)
        if vertex not in tp_list.keys():
            tp.add_vertex(vertex)
    visited = []
    for node in tp_list:
        visited.append(node)
        children = []
        for child in graph[node]:
            if child not in visited:
                children.append(child)
                tp_list[node].append(child)
    return tp_list

#tree solver return the colors of each node
def tree_solver(tp_sort, num_colors):
    color = {}
    clr = Graph(color)
    visited = []
    for parent in tp_sort:
        clr.add_vertex(parent)
        color[parent] = '1'
    for parent in tp_sort:
        for child in tp_sort[parent]:            
            if make_arc_consistent(parent, child, color, num_colors, visited) == False:
                print('There are not enough colors')
                return False
    print('The color of each node is:',color)

#This function give colors at each node until all 
#nodes connected by edges have a different one
def make_arc_consistent(parent, child, color, num_colors, visited):
    if color[parent] == color[child]:
        if color[child] == '1' and num_colors >= 2 and child not in visited:
            color[child] = '2'
        elif color[child] != '3' and color[child] < '4' and num_colors >= 3:
            color[child] = '3'
        elif color[child] != 4 and num_colors >= 4:
            color[child] = '4'
        else:
            return False
    visited.append(child)
    
    
#=============Graph_Class===================================
        
#Class that contain all the functions of a graph    
class Graph(object):
    #initialize a graph object
    def __init__(self, graph_dict=None):
        if graph_dict == None:
            graph_dict = {}
        self.__graph_dict = graph_dict
        
    #Adds vertex in graph
    def add_vertex(self, vertex):
        if vertex not in self.__graph_dict:
            self.__graph_dict[vertex] = []    

    #Adds edges in graph
    def add_edge(self, vertex1, vertex2, edges_list):
        if {vertex1, vertex2} not in edges_list:
            self.__graph_dict[vertex1].append(vertex2)
            self.__graph_dict[vertex2].append(vertex1)
            edges_list.append({vertex1,vertex2})
    
    #Return the list of all edges of the graph
    def edges(self):
        return self.generate_edges()
    
    #Return the list of all edges of the graph
    def generate_edges(self):
        edges = []
        for vertex in self.__graph_dict:
            for neighbour in self.__graph_dict[vertex]:
                if {neighbour, vertex} not in edges:
                    edges.append({vertex, neighbour})
        return edges
    
    #Return the list of edges of a given vertex
    def edges_vertex(self, vertex):
        return self.generate_edges_vertex(vertex)
    
    #Return the list of edges of a given vertex
    def generate_edges_vertex(self,vertex):
        edges = []
        for neighbour in self.__graph_dict[vertex]:
            if {neighbour, vertex} not in edges:
                edges.append({vertex, neighbour})
        return edges
    
    #This function choose which nodes have
    #the biggest number of edges,
    def vertex_max_edges(self, graph):
        max_edges = 0
        max_edges_list = []
        for vertex in graph:
            new_max_edges = len(self.edges_vertex(vertex))#count the number of edges of all vertex in cycle
            if  new_max_edges > max_edges:
                max_edges = new_max_edges
                vertex_max_edges = vertex
        for vertex in graph:
            if len(self.edges_vertex(vertex)) == len(self.edges_vertex(vertex_max_edges)):
                max_edges_list.append(vertex)
        for vertex in graph:
            if len(self.edges_vertex(vertex)) == len(self.edges_vertex(vertex_max_edges))-1:
                max_edges_list.append(vertex)
        for vertex in graph:
            if len(self.edges_vertex(vertex)) == len(self.edges_vertex(vertex_max_edges))-2:
                max_edges_list.append(vertex)
        return max_edges_list
           
    
    #Check if there are cycles in the graph
    def yet_cycles(self, new_graph):
        visited = {}
        #put all vertices as not visited
        for i in new_graph:
            visited[i] = False
        for i in new_graph:  
            if visited[i] ==False:  
                if(self.yet_cycles_util(i,visited,-1, new_graph)) == True: 
                    return True
        return False
    
    def yet_cycles_util(self,v,visited,parent, new_graph):
        # Mark the current node as visited  
        visited[v]= True
  
        # Recur for all the vertices  
        # adjacent to this vertex 
        for i in new_graph[v]: 
              
            # If the node is not  
            # visited then recurse on it 
            if  visited[i]==False :  
                if(self.yet_cycles_util(i,visited,v, new_graph)): 
                    return True
                
            #check if there is a cycle 
            elif  parent!=i: 
                return True
        return False
