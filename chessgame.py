"""
A beats B, we know the ranking of A is higher (number is smaller than B)

total of N players, ranking 1 (best player) to N (worst player)

input, result of M games: [(winner, loser), ...]: [(1, 2), (2, 3), (1, 3), ...]
return the precise ranking of the players

"""

# node->neighbors (people I beat)
# node itself have value (my minimum ranking, # of people I beat)

# short edge can be extended to long edge, A>C, A>B, B>C(add this means A>B>C, and remove A>C)
# [] how?
# constant time to check if A, B share ancestor?
# DFS

# long edge should not be shortened, A>B>C, A>C (add this is noop)
# [] how?
# [] constant time to check if C is a descendent?

# if we can get before(total number of nodes that's higher ranked) and after, if they overlap, that would work
# A>B>C, C is at most 3rd

# union_set?
# add to A->C, affect all of A's
# build the graph first, then dfs to traverse


# A,BC...

# edge is not important, node is important
# full traversal -> n*n


# [(1,2), (2,3), (3,4)], 4 => result shoould be 4 -> everyone has ranking
# [(1,2), (1,3), (1,4)], 4 => result is 1, only player1 has ranking
from collections import defaultdict


def rank_players(match_results, N):
    # brute force
    graph = defaultdict(set)
    reverse_graph = defaultdict(set)
    for winner, loser in match_results:
        graph[winner].add(loser)
        reverse_graph[loser].add(winner)

    # there will be no cycles, A>B>A, not possible
    def dfs(node, visited, g):
        if node in visited:
            return
        visited.add(node)
        for neighbor in g[node]:
            dfs(neighbor, visited, g)

    return_value = 0

    for i in range(1, N + 1):
        # each player
        # get its minimum ranking
        people_behind = set()  # including self
        dfs(i, people_behind, graph)

        people_infront = set()
        dfs(i, people_infront, reverse_graph)

        # get its maximum ranking
        if len(people_behind) + len(people_infront) - 1 == N:
            return_value += 1

    return return_value
