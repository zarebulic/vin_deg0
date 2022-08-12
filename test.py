"""
Created on Fri Aug  5 18:27:25 2022

@author: zareb
"""
import numpy as np
import itertools
import random


import kruskal_dim0 as main
from kruskal_dim0 import vertex
from kruskal_dim0 import edge
from kruskal_dim0 import graph
import copy


def transposition(simplex_list, vertices, position):
    
    simplex_list[position].value, simplex_list[position + 1].value  = simplex_list[position + 1].value,  simplex_list[position].value
    simplex_list.sort(key=lambda x: x.value, reverse=False)
    vertices.sort(key=lambda x: x.value, reverse=False)
    
    return simplex_list, vertices


def test_multiple_transpositions(simplex_list, vertices, positions):
    
    barcode, data_history = main.kruskal_filtration(simplex_list, vertices)
    barcode_vine, vine_data_history = copy.copy(barcode), copy.copy(data_history)
    
    for position in positions:
        
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
            
        barcode_vine, vine_data_history = main.transpose_barcode(simplex_list, barcode_vine, position, vine_data_history)
        simplex_list, vertices = transposition(simplex_list, vertices, position)

      
    barcode_kruskal, kruskal_data_history = main.kruskal_filtration(simplex_list, vertices)

    
    for i in vertices:
        if barcode_vine[i.value] != barcode_kruskal[i.value]:
            print("fail")
            print("Original")
            main.print_barcode(barcode) #Debugging
            
            print("Kruskal")  
            main.print_barcode(barcode_kruskal)
            print("Vine")
            main.print_barcode(barcode_vine)
            
            #print("Original")
            print(i.value, barcode[i.value])
            print(i.value,barcode_vine[i.value])
            print(i.value,barcode_kruskal[i.value])
            
            print(positions)
            #print(barcode[i.value][0].vertices[0].value, barcode[i.value][0].vertices[1].value)
            #print(barcode_vine[i.value][0].vertices[0].value, barcode_vine[i.value][0].vertices[1].value)
            #print(barcode_kruskal[i.value][0].vertices[0].value, barcode_kruskal[i.value][0].vertices[1].value)
    
    return barcode_kruskal == barcode_vine
        
def radnom_multiple_test(simplex_list, vertices, num_trans, num_tests):
    
    for i in range(num_tests):
        positions = np.random.randint(0, len(simplex_list)-1, num_trans)
        simplex_list = main.preprocess(g, random = 1)
        vertices.sort(key=lambda x: x.value, reverse=False)
        if not test_multiple_transpositions(simplex_list, vertices, positions):
            print("False")
            raise Exception
        else:
            print("True")
 

def radnom_filtration_test(simplex_list, vertices, num_tests):
    
    for i in range(num_tests):
        simplex_list = main.preprocess(g, random = 1)
        vertices.sort(key=lambda x: x.value, reverse=False)
        barcode, history = main.kruskal_filtration(simplex_list, vertices)
        #main.print_barcode(barcode)
        if any(list(barcode.values()).count(x) > 1 and x != "inf" for x in list(barcode.values())):
            print("FAIL")
            raise Exception
        

        
        
num_edges = 10
vertices = [vertex() for i in range(10)]
pair_vertices = itertools.permutations(vertices, 2)
edges = [edge(v1,v2) for v1,v2 in pair_vertices]
edges = random.sample(edges, num_edges)
g = graph(vertices, edges)
simplex_list = main.preprocess(g, random = 1)
vertices.sort(key=lambda x: x.value, reverse=False)
positions = [7]
num_tests = 1000000
num_trans = 1



#print(test_multiple_transpositions(simplex_list, vertices, positions))
#radnom_multiple_test(simplex_list, vertices, num_trans, num_tests)
#radnom_filtration_test(simplex_list, vertices, num_tests)
radnom_multiple_test(simplex_list, vertices, num_trans, num_tests)





