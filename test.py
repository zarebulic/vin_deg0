
"""
Created on Fri Aug  5 18:27:25 2022

@author: zareb
"""

import numpy as np
import itertools
import random
import time

import kruskal_dim0 as main
from kruskal_dim0 import vertex
from kruskal_dim0 import edge
from kruskal_dim0 import graph
import copy


def transposition(simplex_list, vertices, position):
    simplex_list == copy.copy(simplex_list)
    vertices = copy.copy(vertices)
    
    simplex_list[position].value, simplex_list[position+1].value = simplex_list[position+1].value, simplex_list[position].value
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
                #print("Transposition not allowed")
                if len(positions) <=3:
                    return True
                continue
        if type(s1) == vertex and type(s2) == edge:
            if s1 in s2.vertices:
                #print("Transposition not allowed")
                if len(positions) <= 5:
                    return True
                continue  
            
        barcode_vine, vine_data_history = main.transpose_barcode(simplex_list, barcode_vine, position, vine_data_history)
        simplex_list_new, vertices_new = transposition(simplex_list, vertices, position)

    barcode_kruskal, kruskal_data_history = main.kruskal_filtration(simplex_list_new, vertices_new)
            
    return barcode_kruskal == barcode_vine and kruskal_data_history == vine_data_history
        
def radnom_multiple_test(simplex_list, vertices, num_trans, num_tests):
    

    for i in range(num_tests):
        
        vertices = [vertex() for i in range(1000)]
        edges = [edge(random.choice(vertices), random.choice(vertices)) for i in range(5000)]
        g = graph(vertices, edges)
        simplex_list = main.preprocess(g, random = 1)
        vertices.sort(key=lambda x: x.value, reverse=False)
        positions = np.random.randint(0, len(simplex_list)-1, num_trans)
        
        if not test_multiple_transpositions(simplex_list, vertices, positions):
            print("False")
            print(positions)
            raise Exception
        else:
            print("True")
            pass
 
       
def multiple_transpositions(simplex_list, vertices, num_trans):
    times = []
    positions = np.random.randint(0, len(simplex_list)-1, num_trans)
    
    barcode, data_history = main.kruskal_filtration(simplex_list, vertices)
    barcode_vine, vine_data_history = barcode, data_history
    
    for position in positions:
        
        # Checking if the switch follows the rules of filtrations
        s1 = simplex_list[position]
        s2 = simplex_list[position + 1]
        if type(s1) == edge and type(s2) == vertex:
            if s2 in s1.vertices:
                #print("Transposition not allowed")
                if len(positions) <=3:
                    return True
                continue
        if type(s1) == vertex and type(s2) == edge:
            if s1 in s2.vertices:
                #print("Transposition not allowed")
                if len(positions) <= 5:
                    return True
                continue  
            
        start = time.time()
        barcode_vine, vine_data_history = main.transpose_barcode(simplex_list, barcode_vine, position, vine_data_history)
        end = time.time()
        print(end - start)  
        times.append(end - start)
        simplex_list_new, vertices_new = transposition(simplex_list, vertices, position)
      
    print(np.mean(times))
    return barcode_vine


       
num_edges = 1
num_vertices = 10

vertices = [vertex() for i in range(10000)]
edges = [edge(random.choice(vertices), random.choice(vertices)) for i in range(50000)]
g = graph(vertices, edges)
simplex_list = main.preprocess(g, random = 1)
vertices.sort(key=lambda x: x.value, reverse=False)

num_tests = 10
num_trans = 10000

positions = np.random.randint(0, len(simplex_list)-1, num_trans)

multiple_transpositions(simplex_list, vertices, num_trans)

#print(test_multiple_transpositions(simplex_list, vertices, positions))
#radnom_filtration_test(simplex_list, vertices, num_tests)
#radnom_multiple_test(simplex_list, vertices, num_trans, num_tests)


