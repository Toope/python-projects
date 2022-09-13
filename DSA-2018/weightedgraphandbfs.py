
WHITE = 0
GREY = 1
BLACK = 2
INF = float('inf')

class WeightedEdgeNode:
    def __init__(self,nde,wgt=0):
        self.node = nde
        self.weight = wgt
        
class Graph:
        
    def __init__(self,num_of_verts):     
        self.num_of_vertices = num_of_verts         #set the node amount
        self.graph = []                             #graph : [[1,2,73],[2,3,85],...]
        self.vertices = []
        self.adj_list = {}
        
        #for bfs             		
        for x in range(1,num_of_verts+1):                 
            self.adj_list[x] = []
            self.vertices.append(x)

        self.color = {}                             
        for x in range(1,num_of_verts+1):
            self.color[x] = WHITE

        self.dist = {}
        for x in range(1,num_of_verts+1):
            self.dist[x] = INF
            
        self.pred = {}
        for x in range(1,num_of_verts+1):
            self.pred[x] = None                          
        #bfs ends

    #for Kruskal 
    def add_edge(self,u,v,weight):                  #adds edge to graph
        """Adds edge to graph."""
        self.graph.append([u,v,weight])        

    def find_set(self, group, i): 
        if group[i] == i: 
            set = i
        else:
            set = self.find_set(group, group[i])
        return set
   
    def union(self, group, x, y):
        x_g = self.find_set(group, x)                 #finds the groups
        y_g = self.find_set(group, y)       
        group[y_g] = x_g                              #performs union
           
def addedge(g,x,y,wght):	
	g.adj_list[x].append(WeightedEdgeNode(y,wght))
	g.adj_list[y].append(WeightedEdgeNode(x,wght))	
       
def bfsearch(g,s):
    queue = list()   
	
    for i in g.vertices:
        g.color[i] = WHITE
        g.dist[i] = INF
        g.pred[i] = 0

    g.dist[s] = 0
    g.color[s] = GREY
    queue.append(s)
	
    while len(queue)!=0:
        u = queue.pop(0)  

        for edge in g.adj_list[u]:
            v = edge.node
            if g.color[v] == WHITE:
                g.color[v] = GREY
                g.dist[v] = g.dist[u] + 1
                g.pred[v] = u
                queue.append(v)

        g.color[u] = BLACK
        
def ispath(g,s,d):
    bfsearch(g,s)
    if g.dist[d] == INF:
        return False		
    return True

def getpath(g,s,d):
    path = []
    bfsearch(g,s)
    u = d
    max_height = 0                               #max height is 0 for start
    if g.dist[d] != INF:
        while g.pred[u] != 0:
            path.append(u)               
            for edge in g.adj_list[u]: 
                v = edge.node                   
                if (g.pred[u] == v or g.pred[u] == u) and edge.weight > max_height:
                    max_height = edge.weight                    
            u = g.pred[u]            
        path.append(s)	
    path.reverse()	
    #print(max_height)
    return path, max_height


def kruskal(g):  
    """Finds MST with Kruskal's algorithm."""
    A = []                                                              #A results
    e = 0                                                               #e edges
    i = 0                                                               #i loop variable
    group = []                                                          #group = list for groups of nodes
    for vert in range(g.num_of_vertices+1): 
        group.append(vert) 
  
    g.graph.sort(key = lambda x: x[2])                                  #sorts the list by weight 
   
    while e < g.num_of_vertices -1 : 
        u,v,w =  g.graph[i]                                             #take the lightest one        
        if g.find_set(group, u) != g.find_set(group ,v):                #if they are in different groups-> union!           
            A.append([u,v,w])                                           #add edge to A        
            g.union(group, g.find_set(group, u), g.find_set(group ,v))  #union
            e = e + 1                                                               
        i = i + 1 
     
    #print("Kruskal: ")       
    #for u,v,weight in A: 
        #print("Edge:(%d,%d), weight:%d" % (u,v,weight)) 
    
    return A
    