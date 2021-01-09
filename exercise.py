"""
Cutset Conditioning and Map Coloring by Stefano Dainelli
    
australia = { "a" : ["b","f"],
            "b" : ["a","c","f"],
            "c" : ["b", "f","d"],
            "d" : ["c","e","f"],
            "e" : ["d","f"],
            "f" : ["a","b","c","d","e"],
            "g" : []
        }


graph1 = { "a" : ["b","c","d"],
            "b" : ["a", "c","g"],
            "c" : ["a", "b", "d", "f"],
            "d" : ["a","c","e"],
            "e" : ["d"],
            "f" : ["c"],
            "g" : ["b"]
        }
        

graph2  = {"a" : ["b", "f"],
            "b": ["a","f","c"],
            "c": ["b", "d", "f", "g"],
            "d": ["e", "c"],
            "e": ["d", "f"],
            "f": ["a", "b", "c", "e"],
            "g": ["c"]
        }         
"""
#====================Libraries==========================
import random #library for generate random values
import string #library used for input
import networkx as nx #library used for drawing graphs
import matplotlib.pyplot as plt #library for generate graphs
import warnings #to ignore a warining message
warnings.filterwarnings("ignore", category=UserWarning)

#================General Functions======================= 
#function that generate a random graph

def generate_graph(num_vertex, random_map):
        
    #number of vertex, number of edges
    #The number of edges is not bigger than 20 
    #to have a nearly-tree graph almost everytime
    max_edges = (num_vertex)*(num_vertex-1)/2
    num_edges = random.randrange(num_vertex, max_edges)
    while num_edges > 20:
        num_edges = random.randrange(num_vertex,max_edges)
    
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
    
    #second_time is used to draw the cut graph from the first graph
    second_time=False
    
    #Watch if the graph is cyclic, 
    #in that case the program try to cut the right vertex
    draw_graph(graph_dict, second_time)
    vertex_cut = g.isCyclic(random_map)            
    
#Function to draw Graphs with matplotlib    
def draw_graph(graphToDraw, second_time):

#Case of FIRST GRAPH
    if second_time==False:                        
        f1 = plt.figure(1)
        G=nx.Graph()
        g=Graph(graphToDraw)
        # a list of nodes:
        G.add_nodes_from(list(graphToDraw.keys()))
        G.add_edges_from(list(g.edges()))
        plt.clf()
        nx.draw(G, with_labels=True, node_size=1500, node_color='skyblue')
        plt.savefig("my_graph.png") # save first graph

#Case of CUT GRAPH
    else:
        f2 = plt.figure(2)
        Gc=nx.Graph()
        gc=Graph(graphToDraw)
        # a list of nodes:
        Gc.add_nodes_from(list(graphToDraw.keys()))
        Gc.add_edges_from(list(gc.edges()))
        plt.clf()
        nx.draw(Gc, with_labels=True, node_size=1500)
        plt.savefig("my_cut_graph.png") # save as png

    plt.show() # display
    
#Function to initialize map coloring given the graph, 
#the number of colors and the vertex that must be cut(cutset conditioning)
def map_coloring(graph, num_color, vertex_cut):
    edges=[]
    #For each vertex create a tuple with his neighbours
    #and so returns all the edges
    for vertex in graph:
        for neighbour in graph[vertex]:
            edges.append([vertex,neighbour])
            
    # initiating a list of verteices
    all_vertices = []
    for v in graph.keys():
        all_vertices.append(v)
    print(solve_map_coloring(all_vertices, num_color, edges, 0))

    
#This function find out the right way to color 
#all the vertices if it is possible
def solve_map_coloring(all_vertices, num_color, edges, vertex):
    if (vertex == 0):
        
        # At first we can add any color for the vertex that was be cut
        new_edges = addColor(edges, all_vertices[0], 1)
        if (new_edges == False):
            return False
        ans = {all_vertices[0]:1}
        
        #Recursive call with vertex = 1
        res = solve_map_coloring(all_vertices, num_color, new_edges, 1)
        if (res == False):
            print('There are not enough colors')
            return False
        ans.update(res)
        return ans
    elif (vertex == len(all_vertices)):
        return {}

    # this function wath all the possible colors for vertices
    for color in range (1,num_color+1):
        ans = {all_vertices[vertex]:color}
        new_edges = addColor(edges, all_vertices[vertex], color)
        if (new_edges == False):
            continue
        res = solve_map_coloring(all_vertices, num_color, new_edges, vertex+1)
        if (res == False):
            continue
        ans.update(res)
        return ans

    # no choice for the current province
    return False
    
#This function colors the vertex with a color and return false if not possible,
#returns a set of restrictions if possible
def addColor(edges, all_vertices, color):
    ans = []
    for i in edges:
        res = checkRestriction(i, all_vertices, color)
        if res == False:
            return False
        elif res == None:
            continue
        else:
            ans.append(res)
    return ans

# Check if the restriction is respected and return false if it is not possible,
#returns a new restriction if it is possible
def checkRestriction(i, all_vertices, color):
    #finding the index of the vertex
    index = -1
    other = -1
    if i[0] == all_vertices:
        index = 0
        other = 1
    elif i[1] == all_vertices:
        index = 1
        other = 0
    else:
        return i

    if isinstance(i[other], int):
        # other is a color
        if (color != i[other]):
            return None
        else:
            return False
    else:
        return [i[other], color]
        
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

    #Function to find out if the graph is cyclic,
    #in that case find all cycles calling isCyclicUtil
    def isCyclic(self, random_map):
        graph = self.__graph_dict
        visited = {}
        thereIsCycle = False
        
        #put all vertices as not visited
        for i in graph:
            visited[i] = False
        
        #initialize as empty the lists 
        #that will contain cycles of the graph
        memorized_paths = []
        all_cycle=[]
        
        #For each vertex, and for each vertex
        #linked to the first one, try to find a path
        #if there is a cycle
        for vertex in graph:
            for near_vertex in graph[vertex]:
                
                #Doesn't control a vertex already visited
                if visited[near_vertex] == False:
                    all_cycle = self.isCyclicUtil(near_vertex,visited,-1, memorized_paths, all_cycle)
                    
                    #If there is at list one cycle
                    if (all_cycle):
                        thereIsCycle = True
                thereIsCycle = False
        
        #If all_cycle is not empty
        #find out how cut the graph to obtain a tree
        if (all_cycle):
            vertex_cut = self.cut_cycle(all_cycle, graph,random_map)  
            return vertex_cut
    
    # A recursive function that find if there is a 
    # cycle in subgraph reachable from vertex v. 
    def isCyclicUtil(self,v,visited,parent, memorized_paths, all_cycle):
        graph = self.__graph_dict
        
        # Visit the vertex v  
        visited[v] = True
        
        #Watch all the vertex linked to v
        for i in self.__graph_dict[v]: 
            #If the vertex i is not visited
            #recurse on it
            if  visited[i]==False :
                if(self.isCyclicUtil(i,visited,v,memorized_paths, all_cycle)):
                    return memorized_paths
                
            # If parent is different
            # from current vertex, 
            # then there is a cycle 
            elif  parent!=i:
                #So find the path of the cycle
                if self.find_path_cycle(i,v, memorized_paths):
                    cycle = self.find_path_cycle(i,v, memorized_paths) #Returns a single cycle
                    all_cycle = self.all_paths(cycle, memorized_paths) #Return all cycles
                    return all_cycle
        return all_cycle

    #Find the path from a vertex to another if there is a cycle between them
    #memorized_paths is used to have a single list of cycles
    #[path] is a single cycle
    def find_path_cycle(self, start_vertex, end_vertex, memorized_paths, path=[]):
        graph = self.__graph_dict
        path = path + [start_vertex]
        
        if start_vertex == end_vertex and len(path)>2:
            return [path]
        if start_vertex not in graph:
            return []
        
        paths = []
        for vertex in graph[start_vertex]: #choose a vertex linked to start_vertex
            if  vertex not in path:
                extended_paths = self.find_path_cycle(vertex, end_vertex, memorized_paths, path)
                for p in extended_paths:
                    if p not in paths:
                        paths.append(p)
        return paths
    
    #This function allow to store all cycle-paths in one list
    def all_paths(self, paths, memorized_paths): 
        if paths and paths not in memorized_paths:# if paths is not empty AND paths is not in memorized_paths
            for path in paths:
                memorized_paths.append(path) 
        return memorized_paths
    
    
    #This function is called only if all_cycle is not empty
    #and for every cycle of the graph, choose what's the best
    #vertex to obtain a tree if it s possible
    def cut_cycle(self, cycleToCut, graph, random_map):
        for cycle in cycleToCut:
            
            #if there is more than one cycle
            if len(cycleToCut) > 1:
                vertex_cut = self.vertex_max_edges(cycleToCut)
            #if there is just one cycle
            else:
                vertex_cut = self.vertex_min_edges(cycleToCut)
        
        #Return the CUT GRAPH after we find out which vertex must be cut
        print (self.cut_graph(vertex_cut, graph, random_map))
        return vertex_cut
    
    #If there are more than one cycle, this function
    #choose which vertex of the cycles has
    #the biggest number of edges,
    #except edges that are not in the path of the cycles
    def vertex_max_edges(self, cycleToCut):
        max_edges = 0
        for cycle in cycleToCut:
            for vertex in cycle:
                new_max_edges = len(self.cycle_edges_vertex(vertex, cycleToCut))#count the number of edges of all vertex in cycle
                if  new_max_edges > max_edges:
                    max_edges = new_max_edges
                    vertex_max_edges = vertex
        return vertex_max_edges
   
    #If there are just one cycle, this function
    #choose which vertex of the cycles has
    #the lowest number of edges
    def vertex_min_edges(self, cycleToCut):
        min_edges = 100000
        vertex_min_edges=0
        for cycle in cycleToCut:
            for vertex in cycle:
                new_min_edges = len(self.generate_edges_vertex(vertex))#count the number of edges of all vertex in cycle
                if  new_min_edges < min_edges:
                    min_edges = len(self.generate_edges_vertex(vertex))
                    vertex_min_edges = vertex
        return vertex_min_edges        

    #Create a new graph similar to the first one,
    #but without cycles
    def cut_graph(self, vertex_cut, graph, random_map): #new cut graph
        graph2 = graph.copy()
        g2 = Graph(graph2)
        graph2[vertex_cut] = []
        print ('The GRAPH is: ')
        print (graph)

        #Remove all edges linked to the vertex
        #that must be cut
        for vertex in graph2:
            if vertex_cut in graph2[vertex]:
                graph2[vertex].remove(vertex_cut)
        
        #Necessary to draw a different graph
        #Check of the graph was not a nearly-tree graph
        second_time=True
        yet_cycle = g2.yet_cycles(graph2)
        if yet_cycle == True:
            num_vertex = len (graph2.keys())
            print('^--This graph is not a nearly-tree graph--^')
            print ("")
            return generate_graph(num_vertex, random_map)
        if random_map == False:
            draw_graph(graph2, second_time)
        
        print('--------------------------------------------------------------------------------------------------------------------------------------------------------')
        print ('The vertex that must be cut is', vertex_cut)  
        print('--------------------------------------------------------------------------------------------------------------------------------------------------------')
        print ('The CUT GRAPH is:')
        print (graph2)
        if random_map == True:
            if vertex_cut == None:
                vertex_cut = random.choice(list(graph.keys()))
                print("")
                num_color = int(input("How many colors?"))
                map_coloring(graph, num_color, vertex_cut)
            else:
                print("")
                num_color = int(input("How many colors?"))
                map_coloring(graph, num_color, vertex_cut)
    
    #Return edges of vertices that are involved in a cycle
    #Doesn't control edges that link a vertex in cycle
    #with a vertex oyt of the cycle
    def cycle_edges_vertex(self, vertex, cycleToCut):
        graph = self.__graph_dict
        edges = []
        for cycle in cycleToCut:
            for neighbour in self.__graph_dict[vertex]:
                if neighbour in cycle and {neighbour, vertex} not in edges:
                    edges.append({vertex, neighbour})
        return edges                
        
    #Check if there are cycles in the cut graph
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