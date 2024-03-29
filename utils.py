# -*- coding:utf-8 -*-

import sys
import scipy.io
import numpy as np
from time import time

__all__ = [
    "nodes_to_array",
    "dict_to_array",
    "connect_array",
    "is_square",
    "diag_zero",
    "to_binary",
    "remove_double_edges",
    "remove_double_edges_rand",
    "remove_weighted_double_edges",
    "to_natural",
    "th_weights",
]



def nodes_to_array(M):
    '''Returns an array of nodes.
    '''
    nodes = []
    for i in range(len(M)):
        nodes.append([i])
    return nodes

#Dictionary to array:
def dict_to_array(dict):
    Arr = []
    for i in range(len(dict)):
        Arr.append(dict[i])
    return Arr

#Connect array:
def connect_array(x):
    y = []
    for i in range(len(x)):
        for j in range(len(x[i])):
            y.append(x[i][j])
    return y

#Check if a matrix is square.
def is_square(M):
    if len(M[:,0]) == len(M[0,:]):
        return True
    else:
        return False

#Fill the diagonal with zeros.
def diag_zero(M):
    '''
    M: an adjacency matrix.
    Return: M with a null diagonal.
    '''
    for i in range(len(M)):
        M[i, i] = 0
    return M

#Convert a weighted matrix to a binary matrix.
def to_binary(M):
    '''Returns a binary matrix.
    M: a weighted adjacency matrix.
    Return: a binary adjacency matrix.
    '''
    for i in range(len(M)):
        for j in range(len(M)):
            if(M[i, j] > 0):
                M[i, j] = 1
            else:
                M[i, j] = 0
    return M


def normalize_weights(M):
    '''Returns a normalized weighted matrix.
    M: a weighted adjacency matrix.
    Return: a binary adjacency matrix.
    '''
    return M


#Remove double edges
def remove_double_edges(M):
    for i in range(len(M)):
        for j in range(len(M)):
            if M[i, j] !=0 and M[j,i] != 0:
                M[j,i] = 0
    return M

#Randomly removes double edges.
def remove_double_edges_rand(G):
    A = nx.adjacency_matrix(G)
    M = A.todense()
    for i in range(len(M)):
        for j in range(len(M)):
            if i != j and M[i,j] != 0 and M[j,i] !=0:
                r = random.choice([i,j])
                M[r, abs(r - (i+j))] = 0
    H = nx.from_numpy_matrix(M, create_using=nx.DiGraph())
    return H

#Remove double edges based on their weights.
def remove_weighted_double_edges(M):
    for i in range(len(M)):
        for j in range(len(M)):
            if M[i, j] !=0 and M[j,i] != 0:
                if M[i,j] >= M[j,i]:
                    M[j,i] = 0
                else:
                    M[i,j] = 0
    return M

#Convert real numbers to natural numbers
def to_natural(M):
    for i in range(len(M)):
        for j in range(len(M)):
            M[i, j] = round(100*M[i, j])
    return M

#Set an additional threshold to the weights
def th_weights(M, th):
    for i in range(len(M)):
        for j in range(len(M)):
            if(M[i, j] < th):
                M[i, j] = 0
            else:
                pass
    return M
