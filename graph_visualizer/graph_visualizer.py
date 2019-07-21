import matplotlib.pyplot as plt
import networkx as nx
import time
import sys


def print_graph(nodes, edges, nodelist_infected, edges_distance):

    """
    Function to draw graph
    :param nodes: node list of the graph
    :param edges: edge list of the graph
    :param nodelist_infected: node list of the infected node in the graph
    :param edges_distance: dictionary of edges as keys and weights as values
    :return: None
    """

    G = nx.Graph()
    G.add_nodes_from(nodes)
    G.add_edges_from(edges)

    position = nx.circular_layout(G)

    nx.draw_networkx_nodes(G, position, nodelist=nodes, node_color="y")
    nx.draw_networkx_nodes(G, position, nodelist=nodelist_infected, node_color="b")

    nx.draw_networkx_edges(G, position)
    nx.draw_networkx_labels(G, position)
    nx.draw_networkx_edge_labels(G, position, edge_labels=edges_distance, font_color='red')

    plt.show()


def infection_spread_adjacent(nodes, edges, nodelist_infected, edges_distance):

    """
    Function to draw the graph with infected nodes based on adjacent nodes
    :param nodes: node list of the graph
    :param edges: edge list of the graph
    :param nodelist_infected: node list of the infected node in the graph
    :param edges_distance: dictionary of edges as keys and weights as values
    :return: None
    """

    print_graph(nodes, edges, nodelist_infected, edges_distance)

    time.sleep(2)

    new_infected = []
    for infected in nodelist_infected:
        if len(new_infected) == len(nodelist_infected):
            break

        for node in nodelist_infected:
            if node not in new_infected:
                new_infected.append(node)
        for edge in edges:
            if infected in edge:
                if edge[1] not in nodelist_infected:
                    nodelist_infected.append(edge[1])
                if edge[0] not in nodelist_infected:
                    nodelist_infected.append(edge[0])

        print_graph(nodes, edges, nodelist_infected, edges_distance)
        time.sleep(2)

    print(nodelist_infected)


def get_absolute_distance(nodelist_infected, edges_distance):

    """
    Function to get absolute distance of each infected node from the infected origin
    :param nodelist_infected: node list of the infected node in the graph
    :param edges_distance: dictionary of edges as keys and weights as values
    :return: dictionary of infected nodes as keys and absolute distance as values
    """

    infect_dict = {nodelist_infected[0]: 0}
    new_infected = []

    for infected in nodelist_infected:
        if len(new_infected) == len(nodelist_infected):
            break

        for node in nodelist_infected:
            if node not in new_infected:
                new_infected.append(node)
        for edge in edges_distance:
            if infected in edge:
                # print(edge[1])
                if edge[1] not in nodelist_infected:
                    nodelist_infected.append(edge[1])
                    infect_dict[edge[1]] = infect_dict[infected] + edges_distance[edge]

                if edge[0] not in nodelist_infected:
                    nodelist_infected.append(edge[0])
                    infect_dict[edge[0]] = infect_dict[infected] + edges_distance[edge]

    return infect_dict


def infection_spread_distance(nodes, edges, edges_distance, speed, infect_dict):

    """
    Function to draw the graph with infected nodes based on infection spread speed
    :param nodes: node list of the graph
    :param edges: edge list of the graph
    :param edges_distance: dictionary of edges as keys and weights as values
    :param speed: speed of the infection spread
    :param infect_dict: dictionary of infected nodes as keys and absolute distance as values
    :return: Node
    """

    t = 0
    distance = 0
    infected_list = []

    while distance <= max(list(infect_dict.values()))+speed:

        for city in infect_dict.keys():
            if infect_dict[city] <= distance:
                infected_list.append(city)

        print('timestep: ', t)
        print_graph(nodes, edges, infected_list, edges_distance)
        infected_list.clear()

        t = t+1

        distance = distance + speed
        time.sleep(2)


def main():

    """
    Main Function
    :return: None
    """

    myfile = open(sys.argv[1])

    infection_type = eval(next(myfile))

    nodes = eval(next(myfile))
    edges = eval(next(myfile))
    edges_distance = eval(next(myfile))

    infected_city = eval(next(myfile))

    nodelist_infected = []

    print_graph(nodes, edges, nodelist_infected, edges_distance)

    time.sleep(2)
    nodelist_infected.append(infected_city)

    if infection_type == 'speed':
        speed = eval(next(myfile))

        infect_dict = get_absolute_distance(nodelist_infected, edges_distance)
        infection_spread_distance(nodes, edges, edges_distance, speed, infect_dict)
    else:
        infection_spread_adjacent(nodes, edges, nodelist_infected, edges_distance)


if __name__ == "__main__":

    main()

