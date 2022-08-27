# -*- coding: utf-8 -*-
"""
Created on Wed Aug 17 10:10:51 2022

@author: zareb
"""
import numpy as np
import itertools
import random


import kruskal_dim0 as main
from kruskal_dim0 import vertex
from kruskal_dim0 import edge
from kruskal_dim0 import graph


def compute_rank_from_barcode(x,y, barcode):
    rank = 0
    for vertex_value,(edge, edge_value) in barcode.items():
        if x >= vertex_value and y >= edge_value :
            rank += 1
    return rank


def compute_rank_invariant(nx, ny, bifiltration):
    rank_invariant = np.zeros(shape = [nx,ny,nx,ny])
    
    
