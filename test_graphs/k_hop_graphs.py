import networkx as nx

# Replace every edge with a copy of the alt graph.
def __util_edge_replacement__(graph, alt_graph):

    assert graph.is_directed() == alt_graph.is_directed()

    DIRECTED = graph.is_directed()

    v1 = sorted([n for n in graph.nodes()])
    if v1[0] != 0 or v1[-1] != len(v1) - 1:
        raise RuntimeError("Error! Can only call __util_edge_replacement__()" +\
                           " on graphs with nodes labeled 0 - V-1.")
    v1 = len(v1)
    e1 = len([e for e in graph.edges()])

    v2 = sorted([n for n in alt_graph.nodes()])
    if v2[0] != 0 or v2[-1] != len(v2) - 1:
        raise RuntimeError("Error! Can only call __util_edge_replacement__()" +\
                           " on graphs with nodes labeled 0 - V-1.")
    v2 = len(v2)
    e2 = len([e for e in alt_graph.edges()])

    v3 = v1 + e1 * v2
    e3 = e1 * (e2 + 2 * v2)

    inner_edges = e1 * e2
    outer_edges = e1 * (2 * v2)

    old_edges = []
    alt_old_edges = []
    old_edges_lists = [old_edges, alt_old_edges]
    graphs = [graph, alt_graph]
    for i in range(0, 2):
        OE = old_edges_lists[i]
        G = graphs[i]
        for a in G.nodes():
            if DIRECTED:
                neighbors = G.successors(a)
                OE += [(a, b) for b in neighbors]
            else:
                neighbors = G.neighbors(a)
                for b in neighbors:
                    if b > a:
                        OE.append((a, b))

    assert len(old_edges) == e1
    assert len(alt_old_edges) == e2

    if DIRECTED:
        new_graph = nx.DiGraph()
    else:
        new_graph = nx.Graph()
    for i in range(0, v3):
        new_graph.add_node(i)

    for i in range(0, e1):
        (a, b) = old_edges[i]

        # Create the i'th subgraph.
        for j in range(0, e2):
            (c, d) = alt_old_edges[j]

            sub_c = v1 + c + (i * v2)
            sub_d = v1 + d + (i * v2)
            new_graph.add_edge(sub_c, sub_d)

        # Connect a and b in the overall graph via the i'th subgraph.
        for k in range(0, v2):
            sub_v = v1 + (i * v2) + k
            new_graph.add_edge(a, sub_v)
            new_graph.add_edge(sub_v, b)

    return new_graph

def k2_graph():
    nodes = [0, 1, 2, 3, 4, 5, 6, 7]
    edges = [(0, 1), (0, 2), (0, 4), (1, 2), (1, 3), (2, 3), (3, 7), (4, 5), (4, 6), (5, 6), (5, 7), (6, 7)]
    G = nx.Graph()
    for n in nodes:
        G.add_node(n)
    for (a, b) in edges:
        G.add_edge(a, b)
    return G 

def k3_graph():
    k2 = k2_graph()
    return __util_edge_replacement__(k2, k2)

def k4_graph():
    return __util_edge_replacement__(k3_graph(), k2_graph())
