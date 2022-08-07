# -*- coding: utf-8 -*-
"""
Created on Fri Aug  5 18:27:25 2022

@author: zareb
"""
import numpy as np
import itertools


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
        barcode_vine, vine_data_history = main.transpose_barcode(simplex_list, barcode_vine, position, vine_data_history)
        simplex_list, vertices = transposition(simplex_list, vertices, position)
    
    barcode_kruskal, kruskal_data_history = main.kruskal_filtration(simplex_list, vertices)
    
    main.print_barcode(barcode_kruskal)
    main.print_barcode(barcode_vine)
    
    return barcode_kruskal == barcode_vine
        

vertices = [vertex() for i in range(10)]
pair_vertices = itertools.permutations(vertices, 2)
edges = [edge(v1,v2) for v1,v2 in pair_vertices]
g = graph(vertices, edges)
simplex_list = main.preprocess(g, random = 1)
vertices.sort(key=lambda x: x.value, reverse=False)
positions = [10,11]

print(test_multiple_transpositions(simplex_list, vertices, positions))
