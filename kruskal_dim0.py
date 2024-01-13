# -*- coding: utf-8 -*-
"""
Created on Sun Jul 24 23:15:16 2022

@author: zareb
"""
import numpy as np
import itertools
import copy
import random

large = 1000

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
       for obj in other.parent_node:
           if obj not in self.parent_node:
               return False
           if other.op_find(obj) != self.op_find(obj):
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
            self.parent_node[u] = u

    def op_find(self, k):
        if self.parent_node[k] == k:
            return k
        return self.op_find(self.parent_node[k])

    def op_union(self, a, b):
        x = self.op_find(a)
        y = self.op_find(b)
        #[x,y] = sorted([x,y], key=lambda x: x.value, reverse = True)
        self.parent_node[x] = y
    


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
    
    vals = []
    if random:
        for vertex in graph.vertices:
            vertex.value = np.random.randint(0, large*graph.num_simplices)
            if vertex.value in vals:
                vertex.value += 0.1
            vals.append(vertex.value)
        for e in graph.edges:
            max_vertex = np.max([e.get_vertices()[0].value, e.get_vertices()[1].value])
            e.value = np.random.randint(max_vertex+1, large*graph.num_simplices)
            if e.value in vals:
                e.value += 0.1
            vals.append(e.value)
            
        graph = clean_procedure(graph)
        
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
    return graph

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
    
    for simplex in simplex_list:
        
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
        data_history.append(c)
                  
    result = display(vertices, data) 
    remaining = []
    for i in result:
        if i not in remaining:
            remaining.append(i)
            barcode[i.value] = 'inf'
            
            
    return barcode, data_history



# ALGORITHM FOR SWITCHING:
    
def transpose_barcode(simplex_list, barcode, position, data_history):
    """
    Returns the barcode of a filtration with two neighbor simplices transposed
    """
    
    if type(simplex_list[position]) == vertex:
        vertex1 = simplex_list[position]
        if type(simplex_list[position + 1]) == vertex:
            # CASE 1 (Vertex - Vertex transposition)
            #print("CASE 1 Vertex - Vertex transposition")
            vertex2 = simplex_list[position+1]
            if barcode[vertex1.value] == 'inf':
                if barcode[vertex2.value] == 'inf':
                    print("CASE 1.1 Both vertices persists to inf")
                    #Barcode does not change
                    data_history[position] = copy.copy(data_history[position-1]) if position != 0 else uf_ds()
                    data_history[position].make_set(vertex2)
                else:
                    #print("CASE 1.2 First vertex persists to inf but the second does not")
                    edge2, m2 = barcode[vertex2.value]
                    if data_history[m2].op_find(vertex2) != vertex1:
                        print("CASE 1.2.1 Second vertex merges with an older vertex")
                        barcode[position + 1] = 'inf'
                        barcode[position] = [edge2, m2]
                        data_history[position] = copy.copy(data_history[position-1]) if position != 0 else uf_ds()
                        data_history[position].make_set(vertex2)
                    else:
                        print("CASE 1.2.2 Second vertex merges with the first vertex")
                        #Barcode does not change
                        data_history[position] = copy.copy(data_history[position-1]) if position != 0 else uf_ds()
                        data_history[position].make_set(vertex2)
                        
                        for ufds in data_history[m2:]:
                            ufds.parent_node[vertex1] = vertex2
                            ufds.parent_node[vertex2] = vertex2
                            
            else:
                edge1, m1 = barcode[vertex1.value]
                if barcode[vertex2.value] == 'inf':
                    print("CASE 1.3 Only the second vertex persists to inf")
                    barcode[position + 1] = [edge1,m1]
                    barcode[position] = 'inf'
                    data_history[position] = copy.copy(data_history[position-1]) if position != 0 else uf_ds()
                    data_history[position].make_set(vertex2)
                else:
                    #print("CASE 1.4 Neither one of the vertices persists to infinity")
                    edge2, m2 = barcode[vertex2.value]
                    if data_history[m2].op_find(vertex2) == vertex1:
                        #CASE 1.3 Second vertex merges with first vertex
                        print("CASE 1.4.2 Second vertex merges with the first vertex")
                        #Barcode does not change
                        data_history[position] = copy.copy(data_history[position-1])
                        data_history[position].make_set(vertex2) 
                        
                        for t, ufds in enumerate(data_history[m2:m1]):
                            ufds.parent_node[vertex1] = vertex2
                            ufds.parent_node[vertex2] = vertex2

                    else:
                       
                        print("CASE 1.4.1 Both vertices merge with older vertices")
                        barcode[vertex1.value] = [edge2, m2]
                        barcode[vertex2.value] = [edge1, m1]
                        
                        data_history[position] = copy.copy(data_history[position-1])
                        data_history[position].make_set(vertex2)
                        
        else:
            
            #CASE 2 - (Vertex and Edge transposition)
            #print("CASE 2.1 Vertex, Edge transposition")
            edge1 = simplex_list[position + 1]
            v1,v2 = edge1.vertices
            e1, e2 = data_history[position].op_find(v1), data_history[position].op_find(v2)
            if vertex1 in edge1.vertices:
                raise Exception("Filtration rules do not allow for this transposition")
                
            if e1 != e2:
                # CASE 2.1.1 Vertex Edge transposition when the edge kills a component
                print("CASE 2.1.1 Vertex Edge transposition when the edge kills a component")
                # This is the case if the edge destroyed a component
                barcode[max(e1.value, e2.value)][1] -= 1
                barcode[vertex1.value + 1] = barcode[vertex1.value]
                barcode.pop(vertex1.value)
                data_history[position] = copy.copy(data_history[position-1])
                older, younger = sorted([e1,e2],key=lambda x: x.value, reverse=False)
                data_history[position].op_union(younger, older)
                
            else:
                print("CASE 2.1.2 Vertex Edge transposition when the edge does nothing")
                # if the edge did not destroy the component, we simply change the vertex part of the barcode
                barcode[vertex1.value + 1] = barcode[vertex1.value]
                barcode.pop(vertex1.value)
                data_history[position] = copy.copy(data_history[position-1])
    else:   
        # The first simplex is an edge
        edge1 = simplex_list[position]
        v1,v2 = edge1.vertices
        e1, e2 = data_history[position-1].op_find(v1), data_history[position-1].op_find(v2)
        
        if type(simplex_list[position + 1]) == vertex:
            # CASE 2.2 the first simplex is an edge
            #print("CASE 2.2 Edge vertex transposition")
            vertex1 = simplex_list[position + 1]
            if e1 != e2:
                # This is the case if the edge destroyed a component
                print("CASE 2.2.1 Edge Vertex transposition when the edge kills a component")
                barcode[max(e1.value, e2.value)][1] += 1
                barcode[vertex1.value - 1] = barcode[vertex1.value]
                barcode.pop(vertex1.value)
                data_history[position] = copy.copy(data_history[position - 1])
                data_history[position].make_set(vertex1)
                
            else:
                # if the edge did not destroy the component, we simply change the vertex part of the barcode
                print("CASE 2.2.2 Edge Vertex transposition when the edge does nothing")
                barcode[vertex1.value - 1] = barcode[vertex1.value]
                del barcode[vertex1.value]
                data_history[position].make_set(vertex1)

                
        else: 
            #CASE 3 - both simplices are edges
            #print("CASE 3 Both simplices are edges")
            edge2 = simplex_list[position+1]
            v3,v4 = edge2.vertices
            e3, e4 = data_history[position-1].op_find(v3), data_history[position-1].op_find(v4)
            if e1 != e2:
                if data_history[position].op_find(v3) == data_history[position].op_find(v4):
                    # CASE 3.2 if the first edge destroys a component but the second one does not
                    #print("CASE 3.2 if the first edge destroys a component but the second one does not")
                    if data_history[position-1].op_find(v3) == data_history[position-1].op_find(v4):
                        # CASE 3.2.1
                        print("CASE 3.2.1 If the second edge does not connect the same components as the first edge")
                        barcode[max(e1.value, e2.value)][1] += 1
                        data_history[position] = copy.copy(data_history[position - 1])
                    else:
                        # CASE 3.2.2
                        print("CASE 3.2.2 If the second edge connects the same components as the first edge")
                        barcode[max(e1.value, e2.value)][0] = edge2
                else:
                    #CASE 3.4: if both edges kill a connected component
                    #print("CASE 3.4: if both edges kill different connected components")
                    e1, e2 = data_history[position-1].op_find(v1), data_history[position-1].op_find(v2)
                    if (e1 == e3 or e1 == e4) and e1.value == max(e2.value, e3.value, e4.value):
                        print("CASE 3.4.1: if both edges kill 3 different connected components")
                        barcode[e1.value][0] = edge2
                        second_max = max(e2.value + e3.value - e1.value, e2.value + e4.value -e1.value, e3.value + e4.value - e1.value)
                        barcode[second_max][0] = edge1
                        #History
                        other = e3 if e1==e4 else e4
                        data_history[position] = copy.copy(data_history[position-1])
                        data_history[position].op_union(e1, other)
                    
                    elif (e2 == e3 or e2 == e4) and e2.value == max(e1.value, e3.value, e4.value):
                        print("CASE 3.4.1: if both edges kill 3 different connected components")
                        barcode[e2.value][0] = edge2
                        second_max = max(e1.value + e3.value - e2.value, e1.value + e4.value -e2.value, e3.value + e4.value - e2.value)
                        barcode[second_max][0] = edge1
                        #History
                        other = e3 if e2==e4 else e4
                        data_history[position] = copy.copy(data_history[position-1])
                        data_history[position].op_union(e2, other)
                    
                    else:
                        print("CASE 3.4.2: if both edges kill 4 different connected components")
                        barcode[max(e1.value, e2.value)][1] += 1
                        barcode[max(e3.value, e4.value)][1] -= 1
                        # Updating the UF data structure
                        data_history[position] = copy.copy(data_history[position - 1])
                        older, younger = sorted([e3,e4],key=lambda x: x.value, reverse=False)
                        data_history[edge1.value].op_union(younger, older)
                        
            else:
                if data_history[position].op_find(v3) != data_history[position].op_find(v4):
                    # CASE 3.3
                    print("CASE 3.3 If the second edge destroys a component, but the first edge does not")
                    barcode[max(e3.value, e4.value)][1] -= 1
                    data_history[position] = copy.copy(data_history[position + 1])
                else:
                    # CASE 3.1 Neither of the edges connects two components:
                    print("CASE 3.1 Neither of the edges connects different components")
                    pass
        
                
    return barcode, data_history           




def print_barcode(barcode):
    for key, value in barcode.items():
        if value=='inf':
            print("[" + str(key) + ", inf )" )
        else:
            print("[" + str(key) + ", " + str(value[1]) + " )")
            

def display(u, uf_data):
    return([uf_data.op_find(i) for i in u])

def print_uf(u, uf_data):
    for i in u:
        if i in uf_data.parent_node:
            print(uf_data.op_find(i).value)





    