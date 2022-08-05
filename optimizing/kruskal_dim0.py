# -*- coding: utf-8 -*-
"""
Created on Sun Jul 24 23:15:16 2022

@author: zareb
"""
import numpy as np
import itertools
import copy

large = 10000

class uf_ds:
    parent_node = {}
    
    def __init__(self):
        self.parent_node = {}
    
    def __eq__(self, other): 
       for obj in self.parent_node:
           if obj not in other.parent_node:
               return False
           if self.op_find(obj) != other.op_find(obj):
               return False
       return True
           
       return True    
    def __deepcopy__(self, memo):
        parent_node = copy.deepcopy(self.parent_node)
        other = uf_ds()
        other.parent_node = parent_node
        return other
    
    def __copy__(self):
        parent_node = copy.copy(self.parent_node)
        other = uf_ds()
        other.parent_node = parent_node
        return other
        
    def make_set(self, u):
        #for i in u:
            self.parent_node[u] = u

    def op_find(self, k):
        if self.parent_node[k] == k:
            return k
        return self.op_find(self.parent_node[k])

    def op_union(self, a, b):
        x = self.op_find(a)
        y = self.op_find(b)
        self.parent_node[x] = y
    

def display(u, uf_data):
    return([uf_data.op_find(i) for i in u])

def print_uf(u, uf_data):
    for i in u:
        if i in uf_data.parent_node:
            print(uf_data.op_find(i).value)

class vertex:
    
    def __init__(self, value = -1):
        self.value = value


class edge:
    
    def __init__(self, vertex1, vertex2, value = -1):
        self.vertices = (vertex1, vertex2)
        self.value = value
    
    def get_vertices(self):
        return self.vertices

class graph:
    
    def __init__(self, vertices, edges):
        self.vertices = vertices
        self.num_vertices = len(vertices)
        self.edges = edges
        self.num_simplices = len(self.edges) + len(self.vertices)
        self.simplices = vertices, edges
    
        

def filtration(graph, random = 0):
    
    if random:
        for vertex in graph.vertices:
            vertex.value = np.random.randint(0, large*graph.num_simplices)
        for e in graph.edges:
            max_vertex = np.max([e.get_vertices()[0].value, e.get_vertices()[1].value])
            e.value = np.random.randint(max_vertex+1, large*graph.num_simplices)
        clean_procedure(graph)
        
    else:
        for i,vertex in enumerate(graph.vertices):
           vertex.value = i
           
        for i,edge in enumerate(graph.edges):
            edge.value = i + graph.num_vertices
 
def clean_procedure(graph):
    values = []
    simplex_list = list(np.concatenate(graph.simplices).flat)
    for simplex in simplex_list:
        values.append(simplex.value)
    values.sort()
    for simplex in simplex_list:
        simplex.value = values.index(simplex.value)
 

def preprocess(g, random):

    filtration(g,random = random)

    simplex_list = g.simplices
    simplex_list = list(np.concatenate(simplex_list).flat)
    simplex_list.sort(key=lambda x: x.value, reverse=False)

    return simplex_list

def kruskal_filtration(simplex_list, vertices):
    
    vertex_count = 0
    data_history = []
    data = uf_ds()
    barcode = {}
    
    for i,simplex in enumerate(simplex_list):
        
        if type(simplex) == vertex:
            data.make_set(simplex)
            vertex_count += 1
        
        else:
            v1, v2 = simplex.vertices
            e1, e2 = data.op_find(v1), data.op_find(v2)
            if e1 != e2:
                older, younger = sorted([e1,e2],key=lambda x: x.value, reverse=False)
                data.op_union(younger, older)
                barcode[younger.value] = [simplex, simplex.value]
                
        
        c = copy.copy(data)
        if  i == 0 or c != data_history[-1][1] :
            data_history.append([i,c])

                  
    result = display(vertices, data) 
    remaining = []
    for i in result:
        if i not in remaining:
            remaining.append(i)
            barcode[i.value] = 'inf'
            
    data_history = {item[0]: item[1] for item in data_history}       
    for i in range(len(simplex_list)):
        if i in data_history.keys():
            real_copy = data_history[i]
        else:
            data_history[i] = real_copy
        
    return barcode, data_history


def print_barcode(barcode):
    for key, value in barcode.items():
        if value=='inf':
            print("[" + str(key) + ", inf )" )
        else:
            print("[" + str(key) + ", " + str(value[1]) + " )")



# ALGORITHM FOR SWITCHING:
    
def transpose_barcode(simplex_list, old_barcode, position, data_history_old):
    """
    Returns the barcode of a filtration with two neighbor simplices transposed
    """
    N = len(simplex_list)
    barcode = copy.copy(old_barcode)
    data_history = data_history_old
    
    if type(simplex_list[position]) == vertex:
        
        if type(simplex_list[position + 1]) == vertex:
            # CASE 1 (Vertex - Vertex transposition)
            print("CASE 1 (Vertex - Vertex transposition)")
            vertex1 = simplex_list[position]
            vertex2 = simplex_list[position+1]
            if barcode[vertex1.value] == 'inf':
                print("CASE 1.2 (First vertex persists to inf)")
                #CASE 1.2 (First vertex persists to inf)
                new_first = uf_ds()
                new_first.make_set(vertex2)
                data_history[position] = new_first
                edge2, m2 = barcode[vertex2.value]
                for i in range(m2, N) :
                    ufds = data_history[i]
                    ufds.parent_node[vertex1] = vertex2
                    ufds.parent_node[vertex2] = vertex2
                    
                return barcode, data_history
            else:
                edge1, m1 = barcode[vertex1.value]  # m1, m2 notation from the proof
                edge2, m2 = barcode[vertex2.value]
            if data_history[m2].op_find(vertex2) == vertex1:
                #CASE 1.3 Second vertex merges with first vertex
                print("CASE 1.3 Second vertex merges with first vertex")
                barcode[vertex1.value] = edge1, m1
                barcode[vertex2.value] = edge2, m2
                #Updating UF data structure 
                data_history[position] = copy.copy(data_history[position-1])
                data_history[position].make_set(vertex2)
                
                
                vertex3 = data_history[m1].op_find(vertex1) #The older vertex to which the first one merges to 

                for i in range(m2, N) :
                    ufds = data_history[i]
                    ufds.parent_node[vertex1] = vertex2
                    if  i >= m1:
                        ufds.parent_node[vertex2] = vertex3
                    else:
                        ufds.parent_node[vertex2] = vertex2
                
            else:
                #CASE 1.1 Both vertices merge with older 
                print("CASE 1.1 Both vertices merge with older ")
                barcode[vertex1.value] = edge2, m2
                barcode[vertex2.value] = edge1, m1
                # Updating the UF datastructure
                data_history[position] = copy.copy(data_history[position-1])
                data_history[position].make_set(vertex2)
                
                
            
        else:
            
            #CASE 2 - (Vertex and Edge transposition)
            print("CASE 2.1 Vertex, Edge transposition")
            vertex1 = simplex_list[position]
            edge1 = simplex_list[position + 1]
            v1,v2 = edge1.vertices
            e1, e2 = data_history[position-1].op_find(v1), data_history[position-1].op_find(v2)
            if vertex1 in edge1.vertices:
                raise Exception("Filtration rules do not allow for this transposition")
                
            if data_history[position-1].op_find(v1) != data_history[position-1].op_find(v2):
                # CASE 2.1,1 Vertex Edge transposition when the edge kills a component
                print("CASE 2.1.1 Vertex Edge transposition when the edge kills a component")
                # This is the case if the edge destroyed a component
                barcode[max(e1.value, e2.value)][1] -= 1
                barcode[vertex1.value + 1] = copy.copy(barcode[vertex1.value])
                barcode.pop(vertex1.value)
                data_history[position] = copy.copy(data_history[position-1])
                older, younger = sorted([e1,e2],key=lambda x: x.value, reverse=False)
                data_history[position].op_union(younger, older)
                
            else:
                print("CASE 2.1.2 Vertex Edge transposition when the edge does nothing")
                # if the edge did not destroy the component, we simply change the vertex part of the barcode
                barcode[vertex1.value + 1] = copy.copy(barcode[vertex1.value])
                barcode.pop(vertex1.value)
                data_history[position] = data_history[position-1]
    else:   
        # The first simplex is an edge
        edge1 = simplex_list[position]
        v1,v2 = edge1.vertices
        e1, e2 = data_history[position-1].op_find(v1), data_history[position-1].op_find(v2)
        
        if type(simplex_list[position + 1]) == vertex:
            # CASE 2.2 the first simplex is an edge
            print("CASE 2.2 Edge vertex transposition")
            vertex1 = simplex_list[position + 1]
            if data_history[position-1].op_find(v1) != data_history[position-1].op_find(v2):
                # This is the case if the edge destroyed a component
                print("CASE 2.2.1 Edge Vertex transposition when the edge kills a component")
                barcode[max(e1.value, e2.value)][1] += 1
                barcode[vertex1.value - 1] = copy.copy(barcode[vertex1.value])
                barcode.pop(vertex1.value)
                data_history[position] = copy.copy(data_history[position - 1])
                data_history[position].make_set(vertex1)
                
            else:
                # if the edge did not destroy the component, we simply change the vertex part of the barcode
                print("CASE 2.2.2 Edge Vertex transposition when the edge does nothing")
                barcode[vertex1.value - 1] = copy.copy(barcode[vertex1.value])
                barcode.pop(vertex1.value)
                data_history[position] = copy.copy(data_history[position + 1])
                data_history[position + 1] = data_history[position]
                
        else: 
            #CASE 3 - both simplices are edges
            print("CASE 3 Both simplices are edges")
            edge2 = simplex_list[position+1]
            v3,v4 = edge2.vertices
            if data_history[edge1.value-1].op_find(v1) != data_history[edge1.value-1].op_find(v2):
                if data_history[edge2.value-1].op_find(v3) == data_history[edge2.value-1].op_find(v4):
                    # CASE 3.2 if the first edge destroys a component but the second one does not
                    print("CASE 3.2 if the first edge destroys a component but the second one does not")
                    if data_history[edge2.value-2].op_find(v3) == data_history[edge2.value-2].op_find(v4):
                        # CASE 3.2.1
                        print("CASE 3.2.1 If the second edge does not connect the same components as the first edge")
                        barcode[max(v1.value, v2.value)][1] += 1
                        data_history[position] = data_history[position - 1]
                    else:
                        # CASE 3.2.2
                        print("CASE 3.2.2 If the second edge connects the same components as the first edge")
                        # nothing changes
                        pass
                else:
                    #CASE 3.4: if both edges kill a connected component
                    print("CASE 3.4: if both edges kill a connected component")
                    barcode[max(v1.value, v2.value)][1] += 1
                    barcode[max(v3.value, v4.value)][1] -= 1
                    # Updating the UF data structure
                    data_history[position] = copy.copy(data_history[position - 1])
                    e3, e4 = data_history[position].op_find(v3), data_history[position].op_find(v4)
                    older, younger = sorted([e3,e4],key=lambda x: x.value, reverse=False)
                    data_history[edge1.value].op_union(younger, older)
                    
                        
            else:
                if data_history[edge2.value-1].op_find(v3) != data_history[edge2.value-1].op_find(v4):
                    # CASE 3.3
                    print("CASE 3.3 If the second edge destroys a component, but the first does not")
                    barcode[max(v3.value, v4.value)][1] -= 1
                    data_history[position] = data_history[position + 1]
                else:
                    # CASE 3.1 Neither of the edges connects two components:
                    print("CASE 3.1 Neither of the edges connects different components")
                
        
                
    return barcode, data_history           


def test_barcode(simplex_list, position, vertices):
    
    barcode, data_history = kruskal_filtration(simplex_list, vertices)
    barcode_vine, new_data_history = transpose_barcode(simplex_list, barcode, position, data_history)
    
    simplex_list[position].value, simplex_list[position + 1].value = simplex_list[position+1].value, simplex_list[position].value
    simplex_list.sort(key=lambda x: x.value, reverse=False)
    vertices.sort(key=lambda x: x.value, reverse=False)
    
    barcode_kruskal, data_history = kruskal_filtration(simplex_list, vertices)
    
    if set(barcode_kruskal) == set(barcode_vine):
        return True
    else:

        return False

        
    
def test_history(simplex_list, position, vertices):
    barcode, data_history = kruskal_filtration(simplex_list, vertices)
    barcode_vine, vine_data_history = transpose_barcode(simplex_list, barcode, position, data_history)
    
    simplex_list[position].value, simplex_list[position + 1].value = simplex_list[position+1].value, simplex_list[position].value
    simplex_list.sort(key=lambda x: x.value, reverse=False)
    vertices.sort(key=lambda x: x.value, reverse=False)
    
    barcode_kruskal, kruskal_data_history = kruskal_filtration(simplex_list, vertices)
    
    if vine_data_history == kruskal_data_history:
        return True
    else:
        return False

        

def test(simplex_list, position, vertices):
    
    # Checking if the switch follows the rules of filtrations
    s1 = simplex_list[position]
    s2 = simplex_list[position + 1]
    if type(s1) == edge and type(s2) == vertex:
        if s2 in s1.vertices:
            print("Transposition not allowed")
            return True
    if type(s1) == vertex and type(s2) == edge:
        if s1 in s2.vertices:
            print("Transposition not allowed")
            return True
        
    
    barcode, data_history = kruskal_filtration(simplex_list, vertices)
    dcbarcode = copy.deepcopy(barcode)
    barcode_vine, vine_data_history = transpose_barcode(simplex_list, barcode, position, data_history)
    
    simplex_list[position].value, simplex_list[position+1].value = simplex_list[position+1].value, simplex_list[position].value
    simplex_list.sort(key=lambda x: x.value, reverse=False)
    vertices.sort(key=lambda x: x.value, reverse=False)
    
    barcode_kruskal, kruskal_data_history = kruskal_filtration(simplex_list, vertices)
    
    if set(barcode_kruskal) == set(barcode_vine):
        print("Success barcode")
        #return True
    else:
        print("original")
        print_barcode(dcbarcode)
        print("kruskal update")
        print_barcode(barcode_kruskal)
        print('vine update')
        print_barcode(barcode_vine)
        print("Fail barcode")
        #return False
    
    if vine_data_history == kruskal_data_history:
        print("Success history")
        #return True
    else:
        print("Fail history")
        for i, (h1, h2) in enumerate(zip(vine_data_history, kruskal_data_history)):
            print(h1 == h2)
            if h1 != h2:
                print(i)
        #return False
    if vine_data_history == kruskal_data_history and set(barcode_kruskal) == set(barcode_vine):
        return True
    else:
        return False
        
def random_test(simplex_list, vertices, number):
    
    for i in range(number):
        position = np.random.randint(20)
        simplex_list = preprocess(g, random = 1)
        vertices.sort(key=lambda x: x.value, reverse=False)
        if not test(simplex_list, position, vertices):
            print(position)
            raise Exception("Fail")


# CREATION AND PREPROCESSING
vertices = [vertex() for i in range(10)]
pair_vertices = itertools.permutations(vertices, 2)
edges = [edge(v1,v2) for v1,v2 in pair_vertices]
g = graph(vertices, edges)

simplex_list = preprocess(g, random = 1)
vertices.sort(key=lambda x: x.value, reverse=False)
position = 4


random_test(simplex_list, vertices, 10000)


#test(simplex_list, position, vertices)









