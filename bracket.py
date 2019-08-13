import sys
from graph import Graph, Vertex

def main():
    '''
    Main function to print the graph data into the console
    including: All The matches, a particular game match using
    Team 1 as an example, Teams that made it to the final, 
    Who won the championship, who was second place, and
    answering the question if two team played at all.
    '''
    g = Graph()
    filename = sys.argv[1]
    g.read_graph_from_file(filename)
    team1 = g.get_vertex('Team 1')
    team11 = g.get_vertex('Team 11')
    team10 = g.get_vertex('Team 10')
    team5 = g.get_vertex('Team 5')

    print('All the matches')
    print(g.get_edge_list())
    print('\n========================\n')

    print('A particular team match: ex: Team1')
    print(team1.neighbors)
    print('\n========================\n')

    print('What teams made it to the final 4 places?')
    possible = []
    max_clique = set()
    # runs 100 time clique and appends to possible clique
    for _ in range(100):
        clique = g.find_maximal_clique()
        possible.append(clique)
    # print(possible)
    for clique in possible:
        if len(clique) == 4:
            max_clique = clique
            
    print(max_clique)
    print('\n========================\n')

    print('Who won the tournament?')
    winner = None
    for vertex in max_clique:
       temp = g.breadth_first_search(vertex, 1, new=True)
       if len(temp) <= 4:
            winner = vertex
    print(winner.id)

    
    print('\n========================\n')

    print('Who was second place?')
    second = None
    for vertex in max_clique:
       temp = g.breadth_first_search(vertex, 1, new=True)
       if len(temp) >= 7:
            second = vertex
    print(second.id)

    
    print('\n========================\n')

    print('Did Team 5 played against Team 11?')
    find_out = g.find_shortest_path(team5.id, team11.id)
    if len(find_out) > 2:
        print(False)
    else:
        print(True)
    print('How can you tell?')
    print(f'Because the shortest path between Team 5 and Team 11 is {len(find_out)} and not 2')
    print('Shortest Path between Team 5 and Team 11')
    print(find_out)

    print('\n========================\n')

    print('Did Team 1 played against Team 10?')
    find_out_again = g.find_shortest_path(team1.id, team10.id)
    if len(find_out_again) > 2:
        print(False)
    else:
        print(True)
    print('How can you tell?')
    print(f'Because the shortest path between Team 1 and Team 10 is {len(find_out_again)}')
    print('Shortest Path between Team 1 and Team 10')
    print(find_out_again)


if __name__ == "__main__":
    main()
