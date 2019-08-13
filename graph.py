#!python
from collections import deque
import random


""" Vertex Class
A helper class for the Graph class that defines vertices and vertex neighbors.
"""


class Vertex(object):

    def __init__(self, vertex):
        """Initialize a vertex and its neighbors.

        neighbors: set of vertices adjacent to self,
        stored in a dictionary with key = vertex,
        value = weight of edge between self and neighbor.
        """
        self.id = vertex
        self.neighbors = {}
        self.parent = None

    def add_neighbor(self, vertex, weight=1):
        """Add a neighbor along a weighted edge."""
        # check if vertex is already a neighbot
        # if vertex in self.neighbors:
        #     # If so, raise KeyError
        #     raise KeyError(f'{vertex} is already neighbor of {self.id}')
        # if not, add vertex to neighbors and assign weight.
        self.neighbors[vertex] = weight

    def __str__(self):
        """Output the list of neighbors of this vertex."""
        return f'{self.id} adjacent to {[x.id for x in self.neighbors]}'

    def get_neighbors(self):
        """Return the neighbors of this vertex."""
        # return the neighbors
        return set(self.neighbors.keys())

    def get_id(self):
        """Return the id of this vertex."""
        return self.id

    def get_edge_weight(self, vertex):
        """Return the weight of this edge."""
        # return the weight of the edge from this
        # vertex to the given vertex.
        return self.neighbors[vertex]

    def __repr__(self):
        '''Return representation of vertex'''
        return f'Vertex {self.id}'

    
    


        


""" Graph Class
A class demonstrating the essential
facts and functionalities of graphs.
"""


class Graph:
    def __init__(self, weighted=False, directed=True):
        """Initialize a graph object with an empty dictionary."""
        self.vertex_list = {}
        self.num_vertices = 0
        self.weighted = weighted
        self.directed = directed

    def add_vertex(self, key):
        """Add a new vertex object to the graph with the given key and return the vertex."""
        # Raise error if key already exist in graph
        if key in self.vertex_list:
            raise KeyError(f'Vertex {key} is already in the graph')
        # increment the number of vertices
        self.num_vertices += 1
        # create a new vertex
        new_vertex = Vertex(key)
        # add the new vertex to the vertex list
        self.vertex_list[key] = new_vertex
        # return the new vertex
        return new_vertex

    def get_vertex(self, key):
        """Return the vertex if it exists"""
         # Raise error if not in graph
        if key not in self.vertex_list:
            raise KeyError(f'Vertex {key} is not in the graph')
        # return the vertex if it is in the graph
        return self.vertex_list[key]
        

    def add_edge(self, from_key, to_key, weight=1):
        """add an edge from vertex with key `from_key` to vertex with key `to_key` with a weight."""
        
        if weight != 1 and not self.weighted:
            self.weighted = True
        # if either vertex is not in the graph,
        # add it - or return an error (choice is up to you).
        if from_key not in self.vertex_list:
           self.add_vertex(from_key)
        # if both vertices in the graph, add the
        # edge by making key1 a neighbor of key2
        # and using the addNeighbor method of the Vertex class.
        # Hint: the vertex key1 is stored in self.vertList[f].
        if to_key not in self.vertex_list:
            self.add_vertex(to_key)

        from_vertex = self.vertex_list[from_key]
        to_vertex = self.vertex_list[to_key]

        from_vertex.add_neighbor(to_vertex, weight)

        if not self.directed:
            to_vertex.add_neighbor(from_vertex, weight)

    def get_vertices(self):
        """return all the vertices in the graph"""
        return set(self.vertex_list.values())

    def get_edge_list(self):
        '''Return a list of edges'''
        edge_list = set()

        for from_vertex in self.get_vertices():
            for to_vertex in from_vertex.get_neighbors():
                # If weighted, store the edge weight in the graph
                if self.weighted:
                    weight = from_vertex.neighbors[to_vertex]

                # If the graph is directed
                if self.directed and self.weighted:
                    edge_list.add((from_vertex.id, to_vertex.id, weight))
                if self.directed and not self.weighted:
                    edge_list.add((from_vertex.id, to_vertex.id))

                # If the graph is undirected only one edge between two vertices
                if not self.directed and self.weighted:
                    if(to_vertex.id, from_vertex.id, weight) not in edge_list:
                        edge_list.add((from_vertex.id, to_vertex.id, weight))
                if not self.directed and not self.weighted:
                    if (to_vertex.id, from_vertex.id) not in edge_list:
                        edge_list.add((from_vertex.id, to_vertex.id))

        return edge_list

    def breadth_first_search(self, vertex, n, new=True):
        '''Implementation of BFS to Find vertices n edges'''

        # Raise error if not a Vertex type
        if not isinstance(vertex, Vertex):
            raise TypeError('vertex must be an instance of Vertex')
        
        # Raise error if vertex not found
        if vertex not in self.get_vertices():
            raise ValueError(f'{vertex} is not in the graph')

        # Only vertices at level n
        if new:
            # Keeps track of the vertices that already been visited
            visit = set([vertex])
            
        # Create deque with passed in vertex
        vertex_deque = deque([vertex])
        # Tracks the current level
        level_counter = 0
        # Tracks the vertices from level n still in deque
        still_in_deque = 1

        while len(vertex_deque) > 0 and level_counter < n:
            # Remove vertex from the front of the deque
            remove_vertex = vertex_deque.popleft()

            # Queue vertices if has not been visited
            if new:
                # go through removed vertex's neighbor
                for v in remove_vertex.get_neighbors():
                    # if has not been visited
                    if v not in visit:
                        # Set the parent
                        v.parent = remove_vertex
                        # add to the back of deque
                        vertex_deque.append(v)
                        # mark v as visit
                        visit.add(v)
            else:
                # add all vertices that v has access to back of the deque
                vertex_deque.extend(remove_vertex.get_neighbors())

            # Decrese one after removing vertex
            still_in_deque -= 1

            # Set level after all vertex from the current level are removed
            if still_in_deque == 0:
                level_counter += 1
                # Vertices that can be reach from this level
                still_in_deque = len(vertex_deque)
                

        # If there's no more levels
        if level_counter < n:
            # return an empty set
            return set()

        # Return a set of all the vertices that can be reach at nth level
        return set(vertex_deque)


    def find_shortest_path(self, start, end):
        '''Find the shortest path betwen two vertices'''
        # Raise error if not found
        if start not in self.vertex_list:
            raise KeyError(f'Vertex {start} is not in the Graph')
        if end not in self.vertex_list:
            raise KeyError(f'Vertex {end} is not in the graph')
        
        # Set start and end 
        start_vertex = self.vertex_list[start]
        end_vertex = self.vertex_list[end]

        # Get vertices one edge away from starting vertex
        level = 1
        vertex_level = self.breadth_first_search(start_vertex, level)
        

        # Loops until there's no level and is the end of the vertex
        while end_vertex not in vertex_level:
            # If there are no more vertices
            if len(vertex_level) == 0:
                return None
            # Increase level to get one more edge away from starting vertex
            level += 1
            vertex_level = self.breadth_first_search(start_vertex, level)

        # Create a path list and ending vertex
        path = [end_vertex]
        parent = end_vertex
        while start_vertex != parent:
            # Move to the current vertex's parent and add it to path
            parent = parent.parent
            path.append(parent)

        # Reverse the path
        path[:] = reversed(path)
        return path
    
    def depth_first_search(self, start, end, visit = []):
        '''Implementation of DFS'''
        # Set the starting and end vertices
        start_vertex = self.vertex_list[start]
        end_vertex = self.vertex_list[end]
        # Mark starting vertex as visit
        visit += [start_vertex]
        # Loop through all neighbors in starting vertex
        print(f"Neighbors of {start_vertex.id}", start_vertex.get_neighbors())
        for neighbor in start_vertex.get_neighbors():
            # print(f"Neighbors of {neighbor.id}", neighbor.get_neighbors())
            # Base case. If the neighbor is the end vertex 
            if neighbor is end_vertex:
                # Loop throuhg the end vertex neighbors
                for nbr in neighbor.get_neighbors():
                    # check the end vertex neighbor is also neighbor of starting vertex
                    # and that is not visit. To handle cases of end vertex having other 
                    # more neighbors.
                    if nbr in end_vertex.get_neighbors() and nbr not in visit and nbr in start_vertex.get_neighbors():
                        # Visit the neighbor where nbr is the vertex before the end vertex 
                        visit += [nbr]
                # Visit the end vertex
                if end_vertex not in visit:
                    visit += [end_vertex]
                # Return base case
                return visit
            # Check if neighbor has been visit
            if neighbor not in visit:
                # Check if neighbor is neighbor of end vertex
                if neighbor in end_vertex.neighbors:
                    # Calls dfs on neighbor
                    visit = self.depth_first_search(neighbor.id, end_vertex.id)
        # return the visited neighbor
        return visit

    def find_maximal_clique(self):
        """Return a maximal clique of a given vertex."""
        # Set the vertex parameter to randomly selected vertex
        vertex = random.choice(list(self.get_vertices()))

        # Raise error if vertex not in the graph
        if vertex not in self.get_vertices():
            raise ValueError(f"Vertex({vertex}) is not in the Graph")

        # Initialize clique as a set of vertices
        clique = set([vertex])

        # Clique members must be neighor of vertex parameter
        for neighor in vertex.get_neighbors():
            # Keep track of clique memebers that are adjacent to neighor
            counter = 0
            # Check each clique member if it is adjacent to current neighor
            for member in clique:
                # If the current neighor is not adjacent to this clique member
                if neighor not in member.get_neighbors():
                    # Break out of this loop, and move to next neighor
                    break
                # If it is, increase the count of adjacent clique members
                counter += 1
                # If all clique members are adjacent to current neighor,
                if counter == len(clique):
                    # Add the current neighor to the clique
                    clique.add(neighor)
                    # Make sure to break out of loop
                    # Avoids RuntimeError: Set changed size during iteration
                    break

        # After all neighors checked, return the clique
        return clique
    

    def read_graph_from_file(self, file_name):
        '''Read graph from a file'''
        file = open(file_name, 'r') 
        file_list = file.readlines()
        vertices = file_list[1].rstrip().split(',')
        valid_types = 'gGdD'
        graph_type = ''
        directed = False
        weighted = False
        edges_list = []

        # Checks for valid types
        if file_list[0].rstrip() in valid_types:
            graph_type = file_list[0].rstrip().upper()
            
        else:
            raise ValueError('G or D is not specified')
        # Checks if graph id directed
        if graph_type == 'D':
            directed = True
        # Checks if graph is weighted
        for item in range(2, len(file_list)):
            edge = file_list[item].rstrip().replace('(', '').replace(')', '').split(',')
            if len(edge) == 3:
                weighted = True
            edges_list.append(edge)
        # Sets the type of the graph 
        if self.num_vertices == 0:
            self.weighted = weighted
            self.directed = directed

        # Add vertices to the graph
        for vertex in vertices:
            if isinstance(vertex, int):
                self.add_vertex(int(vertex))
            else:
                self.add_vertex(str(vertex))

        for edge in edges_list:
            if weighted:
                if isinstance(vertex, int):
                    self.add_edge(int(edge[0]), int(edge[1]), int(edge[2]))
                else:
                    self.add_edge(str(edge[0]), str(edge[1]), int(edge[2]))
            else:
                if isinstance(vertex, int):
                    self.add_edge(int(edge[0]), int(edge[1]))
                else:
                    self.add_edge(str(edge[0]), str(edge[1]))

    #A function used by isConnected 
    def DFSUtil(self,v,visited): 
        # Mark the current node as visited  
        visited[v]= True
  
        #Recur for all the vertices adjacent to this vertex 
        for i in self.vertex_list[v].neighbors:
            if visited[i.id]==False: 
                self.DFSUtil(i.id,visited)

    def is_connected(self):
        '''Checks if all non-zero degree vertices are connected.'''
        # Mark all the vertices as not visited
        visited = [False]*(self.num_vertices + 1)
        # Find a vertex with non-zero degree
        for i in range(1,self.num_vertices):
            if len(self.vertex_list[i].neighbors) > 1:
                break
        if i == self.num_vertices-1: 
            return True
        # Start DFS
        self.DFSUtil(i, visited)
        for i in range(1,self.num_vertices):
            if visited[i] == False and len(self.vertex_list[i].neighbors) > 0:
                return False
        return True
     
    def is_Eulerian(self):
        '''Return true if a Eulerian cycle exist'''
        if self.is_connected() == False:
            return 0
        else:
            # Count vertices with odd degree
            odd = 0
            for i in range(1,self.num_vertices):
                if len(self.vertex_list[i].neighbors) % 2 != 0:
                    odd += 1
            if odd == 0: # if the odd count is 0 then is Eulerian
                return 2 
            elif odd == 2: # if the odd count is 2 is semi-eulerian
                return 1 
            elif odd > 2: # if the odd count is more than 2 
                return 0  # the graph is not Eulerian

        
        

    def __iter__(self):
        """Iterate over the vertex objects in the graph, to use sytax: for v in g"""
        return iter(self.vertex_list.values())


# Driver code


if __name__ == "__main__":

    g = Graph()
    g.read_graph_from_file('graph_data.txt')
    print(g)