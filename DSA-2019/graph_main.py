#By: Tiia Leinonen, in January 2019
#run: ipython graph_main.py
#test file: test_graph_1000.txt

#This program finds the minimum weighted path from town no.1 to a given town by reading a text file.
#text file looks like this
#first row:     towns roads
#rows 2-(n-1):  town town weight
#last row:      destination
#the lowest weight for the test file included, 'test_graph_1000.txt' is 92

from weightedgraphandbfs import *

def ask_file():
    while True:
        try:
            file = str(input("Give a file: "))
            break
        except ValueError:
            print("Error.")
    return(file)

def read_list(file):
    """Reads the file into a list."""
    list = [] 
    try:
        with open(file) as source:
            something = source.readline().strip(" \n")               #first row of the source holds the info about towns and roads
            towns, roads = something.split(" ")  
            towns = int(towns)
            roads = int(roads)
            for i in range(roads):                                   #reads the rows into the list
                row = source.readline().strip(" \n").split(" ")
                for e,i in enumerate(row):                         #from string to int
                    row[e] = int(i)
                list.append(row)
            dest = int(source.readline().strip(" \n"))              #last row is the destination town
    except IOError:
        print("Can't read file.")
     
    print("Towns: " + str(towns) + " , roads: " + str(roads) + " , destination: " + str(dest))   #prints information
    #print(list)
    return towns, roads, list, dest 
    
def main():

    file = ask_file()
    towns, roads, list, dest = read_list(file)

    g = Graph(towns)
       
    for road in range(roads):                                         #repeat add_edge
        g.add_edge(list[road][0],list[road][1],list[road][2])       #list type for Kruskal
        addedge(g,list[road][0],list[road][1],list[road][2])        #list type for BFS
    
    if ispath(g,1,dest):     
        #first find the minimum spanning tree with Kruskal's algorithm
        krusk = kruskal(g)
        #do BFS after Kruskal
        w = Graph(towns)                             
        for k in krusk:                    
            addedge(w,k[0],k[1],k[2])
            
        print(" ")
        print("RESULTS: ")
        path, height = getpath(w,1,dest) #start is always town 1
        print("Path: " + str(path))    
        print("Maximum height: " + str(height))
    else:
        print("No path found!")
        

main()

