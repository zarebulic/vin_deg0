# -*- coding: utf-8 -*-
"""
Created on Tue Aug 30 10:25:39 2022

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

import matplotlib.pyplot as plt
import gudhi


def print_barcode(barcode):
    for [birth, death] in barcode:
        print(f'[{birth}, {death})')

def convert_filtration_to_gudhi(simplex_list):
    simplex_tree = gudhi.SimplexTree()
    for value,simplex in enumerate(simplex_list):
        if type(simplex) == vertex:
            simplex_tree.insert(simplex = [value], filtration = value)
        else:
            v1, v2 = simplex.vertices
            val1, val2 = v1.value, v2.value
            simplex_tree.insert(simplex = [val1,val2], filtration = value)
            
    return simplex_tree

def extract_barcode_from_simplex_tree(simplex_tree):
    result = simplex_tree.persistence(persistence_dim_max = False)
    barcode = [[key, value] for (nul, (key, value)) in result]
    return barcode


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
    
    barcode = []
    for key, value in barcode_vine.items():
        if value == 'inf':
            barcode.append([key, float('inf')])
        else:
            barcode.append([key, value[1]])
    simplex_tree = convert_filtration_to_gudhi(simplex_list)
    barcode_gudhi = extract_barcode_from_simplex_tree(simplex_tree)


    if not sorted(barcode_gudhi) == sorted(barcode):
        return False
    return True
    
   
def radnom_multiple_test( num_trans, num_tests):
    
    for i in range(num_tests):
        
        vertices = [vertex() for i in range(10)]
        pair_vertices = itertools.permutations(vertices, 2)
        edges = [edge(v1,v2) for v1,v2 in pair_vertices]
        edges = random.sample(edges, num_edges)
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

def test_barcode(simplex_list, vertices):
    barcode = []
    barcode_kruskal, data_history = main.kruskal_filtration(simplex_list, vertices)
    for key, value in barcode_kruskal.items():
        if value == 'inf':
            barcode.append([key, float('inf')])
        else:
            barcode.append([key, value[1]])

    simplex_tree = convert_filtration_to_gudhi(simplex_list)
    barcode_gudhi = extract_barcode_from_simplex_tree(simplex_tree)
    print(sorted(barcode_gudhi) == sorted(barcode))

    

num_edges = 10
vertices = [vertex() for i in range(10)]
pair_vertices = itertools.permutations(vertices, 2)
edges = [edge(v1,v2) for v1,v2 in pair_vertices]
edges = random.sample(edges, num_edges)
g = graph(vertices, edges)
simplex_list = main.preprocess(g, random = 1)
num_trans = 100
num_tests = 10000

radnom_multiple_test(num_trans, num_tests)

