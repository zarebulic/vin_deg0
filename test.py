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
    barcode_orig = copy.deepcopy(barcode)
    
    simplex_list_new = simplex_list
    
    for position in positions:
        
        # Checking if the switch follows the rules of filtrations
        s1 = simplex_list[position]
        s2 = simplex_list[position + 1]
        if type(s1) == edge and type(s2) == vertex:
            if s2 in s1.vertices:
                print("Transposition not allowed")
                if len(positions) <=3:
                    return True
                continue
        if type(s1) == vertex and type(s2) == edge:
            if s1 in s2.vertices:
                print("Transposition not allowed")
                if len(positions) <= 5:
                    return True
                continue  
        barcode_vine, vine_data_history = main.transpose_barcode(simplex_list, barcode_vine, position, vine_data_history)
        simplex_list_new, vertices_new = transposition(simplex_list_new, vertices, position)

    barcode_kruskal, kruskal_data_history = main.kruskal_filtration(simplex_list_new, vertices_new)

    
    for i in vertices:
        if i.value not in barcode_vine.keys() or i.value not in barcode_kruskal.keys():
            print("Key set error")
            print(positions)
            print("Original")
            main.print_barcode(barcode_orig) 
            
            print("Kruskal")  
            main.print_barcode(barcode_kruskal)
            print("Vine")
            main.print_barcode(barcode_vine)
            
            #print("Original")
            print(i.value, barcode[i.value])
            print(i.value,barcode_vine[i.value])
            print(i.value,barcode_kruskal[i.value])
            
            
            
        if barcode_vine[i.value] != barcode_kruskal[i.value]:
            print("fail")
            print("Original")
            main.print_barcode(barcode_orig)    
            
            print("Kruskal")  
            main.print_barcode(barcode_kruskal)
            print("Vine")
            main.print_barcode(barcode_vine)
            
            #print("Original")
            print(i.value, barcode_orig[i.value])
            print(i.value,barcode_vine[i.value])
            print(i.value,barcode_kruskal[i.value])
            
            print(positions)    
            #print(barcode[i.value][0].vertices[0].value, barcode[i.value][0].vertices[1].value)
            #print(barcode_vine[i.value][0].vertices[0].value, barcode_vine[i.value][0].vertices[1].value)
            #print(barcode_kruskal[i.value][0].vertices[0].value, barcode_kruskal[i.value][0].vertices[1].value)
    
    return barcode_kruskal == barcode_vine and kruskal_data_history == vine_data_history
        



def radnom_multiple_test(simplex_list, vertices, num_trans, num_tests, num_vertices, num_edges):
    

    for i in range(num_tests):
        positions = np.random.randint(0, len(simplex_list)-1, num_trans)
        vertices = [vertex() for i in range(num_vertices)]
        pair_vertices = itertools.permutations(vertices, 2)
        edges = [edge(v1,v2) for v1,v2 in pair_vertices]
        edges = random.sample(edges, num_edges)
        g = graph(vertices, edges)
        simplex_list = main.preprocess(g, random = 1)
        vertices.sort(key=lambda x: x.value, reverse=False)
        if not test_multiple_transpositions(simplex_list, vertices, positions):
            print("False")
            print(positions)
            raise Exception
        else:
            print("True")
 


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
    return times


    
num_edges = 99000
num_vertices = 1000

vertices = [vertex() for i in range(100)]
edges = [edge(random.choice(vertices), random.choice(vertices)) for i in range(500)]
g = graph(vertices, edges)
simplex_list = main.preprocess(g, random = 1)
vertices.sort(key=lambda x: x.value, reverse=False)

num_tests = 100
num_trans = 1000

#positions = np.random.randint(0, len(simplex_list)-1, num_trans)

#radnom_multiple_test(simplex_list, vertices, num_trans, num_tests, num_vertices, num_edges)


multiple_transpositions(simplex_list, vertices, num_trans)



