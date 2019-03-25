import networkx as nx
from networkx import edge_betweenness_centrality
import matplotlib.pyplot as plt

mapping = {0: 'Mr. Hi', 33: 'Officer'}  # gives mr Hi and officer explicit names in graph
G = nx.relabel_nodes(nx.karate_club_graph(), mapping)  # generates graph
color_map = []
for node in G:  # iterate through data and color each node for its club
    if G.node[node]['club'] == 'Mr. Hi':
        color_map.append('red')
    elif G.node[node]['club'] == 'Officer':
        color_map.append('green')
    else:
        print "error in determining club"

i = 0
while i < 11:
    edge_color_map = []  # declares edge color map, empty for each new iteration
    centrality = edge_betweenness_centrality(G)  # get list of edge strengths
    max_centrality = max(centrality, key=centrality.get)  # find strongest edge
    for edge in G.edges():  # color the edge that is about to be deleted
        if edge == max_centrality:
            edge_color_map.append('red')
        else:
            edge_color_map.append('black')
    nx.draw(G, node_color=color_map, edge_color=edge_color_map, with_labels=True)
    plt.show()  # draw graph with to-be removed edge in red

    G.remove_edge(max_centrality[0], max_centrality[1])  # remove max_centrality edge
    i += 1

print "final graph"
nx.draw(G, node_color=color_map, with_labels=True)
plt.show()
