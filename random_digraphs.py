'''
Random Digraph Models
'''

import numpy as np
import statistics as st
import networkx as nx
import random
from random import choice, seed
from math import comb
from utils import *


__all__ = [
    "random_weights",
    "directed_kregular_model",
    "directed_erdos_renyi_Gnp_model",
    "directed_erdos_renyi_GnM_model",
    "directed_watts_strogatz_model",
    "weighted_directed_watts_strogatz_model",
    "directed_barabasi_albert_model",
    "maslov_sneppen_rewiring",
    "lattice_rewiring",
    "random_3_clique_model",
    "random_3_clique_model",
    "include_exclude_edges",
    "dynamic_random_digraph_model",
    "MonteCarloSimulation",
]


def random_weights(M):
    '''Returns a weighted adjacency matrix.
    Parameters
    ----------
    M: (NumPy matrix) adjacency matrix.
    '''
    for i in range(len(M)):
        for j in range(len(M)):
            if i != j and M[i, j] > 0:
                '''
                Weights are randomly chosen from a uniform
                distribution over the half-open interval [0.00001, 1).
                '''
                M[i, j] = round(np.random.uniform(0.00001, 1), 4)
    return M
                      
                

#---------- k-Regular Random Model ----------

def directed_kregular_model(n, k, weight=False):
    """Returns a weighted k-Regular random digraph.
    Parameters:
    ----------
    n : Number of nodes (integer). 
    k : Number of in- and out- degree (integer).
    Notes:
    Havel-Hakimi Algorithm
    """
    r = tuple([k]*n)
    H = nx.directed_havel_hakimi_graph(r,r)
    W = nx.to_numpy_matrix(H)
    
    if weight==True:
        Wd = random_weights(W)
        return diag_zero(Wd)
    else:
        return diag_zero(W)
    

#---------- Erdős–Rényi-Gilbert Random Model (G(n, p)) ----------

def directed_erdos_renyi_Gnp_model(n, p, weight=False):
    """Returns a weighted binomial random digraph.
    Parameters:
    ----------
    n : Number of nodes (integer).    
    p : Probability of add a directed edge (i,j).
    """
    A = np.zeros((n,n))  #null matrix (no connections).           
    for i in range(n):
        for j in range(n):
            if i != j:
                A[i, j] = np.random.binomial(1, p) #add a directed edge with probability p.
    
    if weight==True:
        W = random_weights(A)
        return diag_zero(W)
    else:
        return diag_zero(A)
   

#---------- Erdős–Rényi Random Model (G(n, M)) ----------

def directed_erdos_renyi_GnM_model(n, M, weight=False):
    """Returns a weighted Erdős–Rényi random digraph.
    Parameters:
    ----------
    n : Number of nodes (integer).   
    M : Number of edges (i,j).
    """
    if M > comb(n, 2)*2:
        print("Error. M must be <= comb(n, 2)*2.")
        
    A = np.ones((n,n)) - np.diag(np.diag(np.ones((n,n)))) 
    S = n*n-n
    
    while S > M:
        i = random.randint(0,n-1)
        j = random.randint(0,n-1)
        if i != j and A[i, j] > 0:
            A[i, j] = 0
            S -= 1
        else:
            pass
    
    if weight==True:
        W = random_weights(A)
        return diag_zero(W)
    else:
        return diag_zero(A)



#---------- Watts–Strogatz Random Model ----------

def directed_watts_strogatz_model(n, k, p):
    """Returns a Watts–Strogatz small-world digraph.
    Parameters:
    ----------
    n : Number of nodes (integer).    
    k : Number of nearest neighbors (integer).
    p : Probability of rewiring each edge (float).
    
    The directions of the edges in the initial ring are arranged in
    a counter-clockwise manner.
    
    Note: This code is a direct modification of the Watts–Strogatz Model
    implemented in Networkx.
        """
    if k > n:
        raise nx.NetworkXError("k>n, choose smaller k or larger n")

    H = nx.DiGraph()
    nodes = list(range(n)) 
    for j in range(1, k // 2 + 1):
        targets = nodes[j:] + nodes[0:j]  
        H.add_edges_from(zip(nodes, targets))      
   
    for j in range(1, k // 2 + 1):  
        targets = nodes[j:] + nodes[0:j]  

        for u, v in zip(nodes, targets):
            if np.random.binomial(1, p) != 0:
                w = choice(nodes)

                while w == u or H.has_edge(u, w):
                    w = choice(nodes)
                    if H.degree(u) >= n - 1:
                        break 
                else:
                    H.remove_edge(u, v)
                    H.add_edge(u, w)
    
    W = nx.to_numpy_matrix(H)
    W = np.array(W)
    return diag_zero(W)


def weighted_directed_watts_strogatz_model(n, k, p):
    """Returns a weighted Watts–Strogatz small-world digraph.
    Parameters:
    n : Number of nodes (integer);     
    k : Number of nearest neighbors (integer);
    p : Probability of rewiring each edge (float).
    """
    W = directed_watts_strogatz_model(n, k, p)
    for i in range(n):
        for j in range(n):
            if W[i, j] > 0:
                '''
                Weights are randomly chosen from a uniform
                distribution over the half-open interval [0.00001, 1).
                '''
                W[i, j] = np.random.uniform(0.00001, 1) 
    return W


#----- Barabási-Albert Random Model -----

def directed_barabasi_albert_model(n, alpha, beta, gamma, delta_in, delta_out, weight=False):
    """Returns a weighted Barabási-Albert digraph (see [1]).
    Parameters (see [2]):
    n : Number of nodes (integer);     
    alpha : Probability for adding a new node connected to an existing node
            chosen randomly according to the in-degree distribution (float).
    beta : Probability for adding an edge between two existing nodes.
           One existing node is chosen randomly according the in-degree
           distribution and the other chosen randomly according to the out-degree
           distribution.
    gamma : Probability for adding a new node connected to an existing node
            chosen randomly according to the out-degree distribution (float).
    delta_in : Bias for choosing nodes from in-degree distribution (float).
    delta_out : Bias for choosing nodes from out-degree distribution (float).
    --------
    References:
    [1] B. Bollobás, C. Borgs, J. Chayes, and O. Riordan, Directed scale-free graphs, Proceedings of the fourteenth 
    annual ACM-SIAMSymposium on Discrete Algorithms, 132–139, 2003.
    [2] https://networkx.org/documentation/stable/reference/generated/networkx.generators.directed.scale_free_graph.html
    """
    SF = nx.scale_free_graph(n, alpha=alpha, beta=beta, gamma=gamma, delta_in=delta_in, delta_out=delta_out, create_using=None, seed=None)
    W = nx.to_numpy_matrix(SF)
    
    if weight==True:
        for i in range(n):
            for j in range(n):
                if W[i, j] > 0:
                    '''
                    Weights are randomly chosen from a uniform
                    distribution over the half-open interval [0.00001, 1).
                    '''
                    W[i, j] = np.random.uniform(0.00001, 1) 
        return diag_zero(W)
    else:
        return diag_zero(W)
    


#---------- Maslov-Sneppen Rewiring and Lattice Rewiring ----------
    
def maslov_sneppen_rewiring(M):
    '''Returns a digraph
    Parameters
    ---------
    M: matrix
    '''
    Dg = nx.from_numpy_matrix(M, create_using=nx.DiGraph())
    Dg_wde = remove_double_edges_rand(Dg)
    Gr = nx.Graph(Dg_wde)
    MS = nx.random_reference(Gr, niter=1, connectivity=True, seed=None)
    D = nx.DiGraph(MS)
    MSW = remove_double_edges_rand(D)
    return MSW


def lattice_rewiring(M):
    '''Returns
    Parameters
    ---------
    M: matrix
    '''
    Dg = nx.from_numpy_matrix(M, create_using=nx.DiGraph())
    Dg_wde = remove_double_edges_rand(Dg)
    Gr = nx.Graph(Dg_wde)
    L = nx.lattice_reference(Gr, niter=5, D=None, connectivity=True, seed=None)
    D = nx.DiGraph(L)
    LW = remove_double_edges_rand(D)
    return LW


#------------ Random k-Clique Digraph Model -------------

def random_2_clique_model(n, d):
    '''
    Parameters:
    n: (integer) Number of nodes.
    d: "density" (number of iterations).
    '''
    M = np.zeros((n, n))
    for l in range(0, int(100*d)):
        i = random.randint(0,n-1)
        j = random.randint(0,n-1)
        k = random.randint(0,n-1)
        if i != j and j != k and i != k:
            M[i,j] = M[j,k] = M[i,k] = 1
        else:
            pass

    Wd = random_weights(M)
    return diag_zero(Wd)


def random_3_clique_model(n, d):
    '''
    Parameters:
    n: number of nodes.
    d: "density" (number of iterations).
    '''
    M = np.zeros((n, n))
    for m in range(0, int(100*d)):
        i = random.randint(0,n-1)
        j = random.randint(0,n-1)
        k = random.randint(0,n-1)
        l = random.randint(0,n-1)
        if i != j and j != k and i != k and l != j and l != k and i != l:
            M[i,j] = M[i,k] = M[i,l] = M[j,l] = M[l,k] = M[j,k] = 1
        else:
            pass

    Wd = random_weights(M)
    return diag_zero(Wd)


#------------ Dynamic Random Digraph Model -------------

def include_exclude_edges(L, p1, p2):
    '''
    Parameters:
    L: The underlying adjacent matrix
    p1: probability that edge (i,j) exists at time t.
    p2: probability that a non-existent edge (i,j) arises at time t.
    '''
    M = np.zeros((len(L), len(L)))
    for i in range (len(L)):
        for j in range (len(L)):
            if L[i, j] != 0:
                M[i, j] = np.random.binomial(1, p1)*np.random.uniform(0.00001, 1) 
            if L[i, j] == 0:
                M[i, j] = np.random.binomial(1, p2)*np.random.uniform(0.00001, 1) 
    return diag_zero(M)

def dynamic_random_digraph_model(M, p1, p2, t):
    '''Returns a weighted dynamic random digraph.
    Parameters:
    L: The underlying adjacent matrix
    p1: probability that edge (i,j) exists at time t.
    p2: probability that a non-existent edge (i,j) arises at time t.
    t: time range.
    '''
    D=[]
    for i in range(t):
        D.append(np.zeros((len(M),len(M))))

    D[0]=M
    for k in range(1,t):
        D[k] = include_exclude_edges(D[k-1], p1, p2)
    return D
    

#------------ Monte Carlo Simulation -------------
    
def MonteCarloSimulation(num_simulations, digraph_model, n):
    '''Returns an array of random matrices.
    Parameters
    ---------
    num_simulations: (integer) number of digraphs.
    digraph_model: (string) model.
    n: (integer) number of nodes.
    '''
    all_kr_digraphs=[]
    all_erp_digraphs=[]
    all_erM_digraphs=[]
    all_ws_digraphs=[]
    all_ba_digraphs=[]
    K=[]
    Per=[]
    Pws=[]

    if digraph_model == 'regular':
        for i in range(num_simulations):
            #k-Regular random digraphs:
            k = int(np.random.uniform(1,10))
            KR = directed_kregular_model(n, k, weight=False)
            KR = remove_double_edges(KR)
            K.append(k)
            all_kr_digraphs.append(KR)
        return all_kr_digraphs

    if digraph_model == 'erdos-renyi_Gnp':
        for i in range(num_simulations):
            p = np.random.uniform(0,1)
            ERp = directed_erdos_renyi_Gnp_model(n, p, weight=False)
            ERp = remove_double_edges(ERp)
            all_erp_digraphs.append(ERp)
        return all_erp_digraphs

    if digraph_model == 'erdos-renyi_GnM':
        for i in range(num_simulations):
            #Erdos-Renyi random digraphs:
            per = int(np.random.uniform(0,190))
            ERM = directed_erdos_renyi_GnM_model(n, per, weight=False)
            ERM = remove_double_edges(ERM)
            Per.append(per)
            all_erM_digraphs.append(ERM)
        return all_erM_digraphs

    if digraph_model == 'watts_strogatz':
        for i in range(num_simulations):
            #Watts-Strogatz random digraphs:
            pws = round(np.random.uniform(0,1), 4)
            WS = directed_watts_strogatz_model(n, 10, pws)
            WS = remove_double_edges(WS)
            Pws.append(pws)
            all_ws_digraphs.append(WS)
        return all_ws_digraphs
    
    if digraph_model == 'barabasi_albert':
        for i in range(num_simulations):
            pba = round(np.random.uniform(0,1), 4)
            BA = directed_barabasi_albert_model(n, alpha=0.41, beta=0.54, gamma=0.05, delta_in=pba, delta_out=0, weight=False)
            BA = remove_double_edges(BA)
            all_ba_digraphs.append(BA)
        return all_ba_digraphs
    
    
    