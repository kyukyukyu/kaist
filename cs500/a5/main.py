import numpy as np

#PROBLEM 15 . a) - pit(f, n, d) & pit_repeater(f, n, d, N)  
def pit(f, n, d):
    """
    Conducts polynomial identity test on the given funtion f once then
    decides whether a function f is nonzero polynomial or not.
    @param f:
    A function to check if it is nonzero polynomial or not.
    @param n:
    The number of variables the function f takes.
    @param d:
    The degree of the function f. 
    @return: 
    True if the function f is nonzero polynomial, False, otherwise.
    """
    i = d + 1
    while i > 0:
        vars = np.random.randint(-16, 16, size=n)
        res = f(vars)
        if res != 0:
            return True
        i -= 1
    return False
    
    
def pit_repeater(f, n, d, N):
    """
    Repeats polynomial identity test on the given funtion f up to an error bounds 2^-N
    @param f:
    A function to check if it is non zero polynomial or not.
    @param n:
    The number of variables the function f takes.
    @param d:
    The degree of the function f.
    @param N:
    Repeat count of polynomial identity testing.
    @return:
    True if the function f is nonzero polynomial, False, otherwise.
    """
    i = d * (2 ** -N)
    while i > 0:
        if True == pit(f, n, d):
            return True
        i -= 1
    return False


#PROBLEM 15 . b) - generate_polynomial_function(graph) & has_perfect_matching(graph)
def generate_polynomial_function(graph):
    """    
    @param graph:
    A two dimensional list (matrix) representing an undirected graph.
    Element 0 indicates no edge exists between two vertices, and
    Element 1 indicates an edge exists between two vertices.
    @return (f, n, d):   
    f is a polynomial function calculating the determinant of a Tutte matrix from the graph.
    f takes one list of n variables.
    Since Tutte matrix is symbolic 
    the polynomial function f 
    takes integer values (in one list) and 
    assigns them to variables then 
    calculates and returns the integer determinant.
    n is the number of variables in the polynomial function f.
    d is the degree of the polynomial function f.
    @note: 
    You are recommended to use an external library like `Link numpy <http://www.numpy.org/>`.
    Otherwise, you can write a function calculating the determinant of a matrix on your own. 
    """
    graph = np.array(graph)
    graph_triu = np.triu(graph)
    def f(variables):
        tutte = np.zeros_like(graph)
        tutte[graph_triu == 1] = variables
        tutte -= tutte.T
        
        return np.linalg.det(tutte)
    
    n = np.count_nonzero(graph_triu)
    d = graph.shape[0]

    return (f, n, d)


def has_perfect_matching(graph):
    """
    Checks if the given graph can (probably) have a perfect matching or not.
    @return: True if the graph can have a perfect matching, False, otherwise.
    """
    f, n, d = generate_polynomial_function(graph)
    return pit_repeater(f, n, d, 300)

    
#PROBLEM 15 . c) - generate_random_graph(n, m)
def generate_random_graph(n, m):
    """
    Generates a random graph with 
    n vertices and 
    m undirected edges randomly and uniformly distributed.
    @param n:
    The number of vertices.
    @param m:
    The number of edges.
    @return:
    A 2 dimensional list (matrix) representing an undirected graph with 
    n vertices and 
    m undirected edges.
    Element 0 indicates no edge exists between two vertices, and
    Element 1 indicates an edge exists between two vertices.
    """

    # implement here
        
    return graph


#PROBLEM 15 . d) - estimate_perfect_matching()
def estimate_perfect_matching():
    """
    Estimates how many perfect matchings exist in 
    arbitrary graphs with 100 vertices and 350 or 200 edges
    out of 50 trials.
    @return (n_pm_350, n_pm_200):
    A pair of the numbers of perfect matching out of 50 trials when using a randomly generated graph 
    with 100 vertices and 350 edges randomly and uniformly distributed and 
    with 100 vertices and 200 edges randomly and uniformly distributed. 
    """
    
    # implement here
            
    return (n_pm_350, n_pm_200)
