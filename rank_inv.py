# -*- coding: utf-8 -*-
"""
Created on Wed Aug 17 10:10:51 2022

@author: zareb
"""
large = 10e5
import numpy as np
import itertools
import random
import copy

import kruskal_dim0 as main
from kruskal_dim0 import vertex
from kruskal_dim0 import edge
from kruskal_dim0 import graph


def build_bifiltration(graph, nx, ny):
    values1 = []
    values2 = []
    for vertex in graph.vertices:
            vertex.value1 = np.random.randint(0, large*graph.num_simplices)
            vertex.value2 = np.random.randint(0, large*graph.num_simplices)
            if vertex.value1 in values1:
                vertex.value += 0.1
            if vertex.value2 in values2:
                vertex.value += 0.15
            values1.append(vertex.value1)
            values2.append(vertex.value2)
    for e in graph.edges:
            max_vertex_val1 = np.max([e.get_vertices()[0].value1, e.get_vertices()[1].value1])
            max_vertex_val2 = np.max([e.get_vertices()[0].value2, e.get_vertices()[1].value2])
            e.value1 = np.random.randint(max_vertex_val1+1, large*graph.num_simplices)
            e.value2 = np.random.randint(max_vertex_val2+1, large*graph.num_simplices)
            if e.value1 in values1:
                e.value += 0.1
            if e.value2 in values2:
                e.value += 0.15
            values1.append(e.value1)
            values2.append(e.value2)
            
    values1.sort()
    values2.sort()
    simplex_list = list(np.concatenate(graph.simplices).flat)
    
    bifiltration = np.array([[[main.vertex() for i in range(nx)] for i in range(ny)] for k in range(2)])
    
    for simplex in simplex_list:
        simplex.value1 = values1.index(simplex.value1)
        simplex.value2 = values2.index(simplex.value2)
    
    simplex_list_list = [[copy.copy(simplex_list) for i in range(nx)] for i in range(ny)]
      
    for i in range(nx):
        for j in range(ny):
            if i == nx-1 or j == nx-1:
                bifiltration[0][i,j] = 0
                bifiltration[1][i,j] = 0
            else:
                simplex1 = min(simplex_list_list[i][j], key=lambda x: x.value1)
                simplex2 = min(simplex_list_list[i][j], key=lambda x: x.value2)
                for row in simplex_list_list[i+2:]:
                    for element in row[j+1:]:
                        if simplex1 in element:
                            element.remove(simplex1)
                for row in simplex_list_list[i+1:]:  
                    for element in row[j+2:]:
                        if simplex2 in element:
                            element.remove(simplex2)
                bifiltration[0][i,j] = simplex1
                bifiltration[1][i,j] = simplex2
    
    for i in range(nx-1):
        simplex1 = min(simplex_list_list[i][nx-1], key=lambda x: x.value1)
        for row in simplex_list_list[nx-1:]:
            if element in row[i+1:]:
                if simplex1 in element:
                    element.remove(simplex1)
        bifiltration[0][i,nx-1] = simplex1
    
    for i in range(nx-1):
        simplex1 = min(simplex_list_list[nx-1][i], key=lambda x: x.value2)
        for row in simplex_list_list[i+1:]:
            for element in row[nx-1:]:
                if simplex1 in element:
                    element.remove(simplex1)
        bifiltration[1][nx-1,i] = simplex1
    
    return bifiltration
            

def compute_rank_from_barcode(x,y, barcode):
    rank = 0
    for birth, death  in barcode.items():
        if death == 'inf':
            if x >= birth:
               rank += 1
        else:
            death = death[1]
            if x >= birth and y >= death :
                rank += 1
    return rank

def extract_simplex_list(path):
    simplex_list = [element for position, element in path]
    for simplex in simplex_list:
        simplex.value = simplex_list.index(simplex)
    return simplex_list


def compute_rank_invariant(nx, ny, bifiltration, vertices):
    rank_invariant = np.zeros(shape = [nx,ny,nx,ny])

    initial_path = [[[i,0],element] for i, element in enumerate(bifiltration[0][:,0])] +  [[[nx-1,i],element] for i, element in enumerate(bifiltration[1][nx-1,:])]
    simplex_list = extract_simplex_list(initial_path)
    check_list(simplex_list)
    barcode, data_history = main.kruskal_filtration(simplex_list, vertices)

    #Computing the known rank invariants from the initial paht
    for (x, (position1, simplex1)), (y, (position2, simplex2)) in itertools.combinations(enumerate(initial_path), 2):
        rank_invariant[position1[0], position1[1],position2[0], position2[1]] = compute_rank_from_barcode(x,y, barcode)
    
    
    return rank_invariant


def check_list(simplex_list):
    print(len(set(simplex_list)) == len(simplex_list))
   
def print_non_zero_rank(rank_invariant, size):
    for i in range(size):
        for j in range(size):
            for k in range(size):
                for l in range(size):
                    if rank_invariant[i,j,k,l] != 0:
                        #print(i,j,k,l, rank_invariant[i,j,k,l])
                        3


num_edges = 1
num_vertices = 2
num_simplex = num_edges + num_vertices
vertices = [vertex() for i in range(num_vertices)]
pair_vertices = itertools.permutations(vertices, 2)
edges = [edge(v1,v2) for v1,v2 in pair_vertices]
edges = random.sample(edges, num_edges)
g = graph(vertices, edges)

bifiltration = build_bifiltration(g, num_simplex, num_simplex)
print(bifiltration)
#print(compute_rank_invariant(num_simplex, num_simplex, bifiltration, vertices))
#rank = compute_rank_invariant(num_simplex, num_simplex, bifiltration, vertices)
#print_non_zero_rank(rank, num_simplex)





