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
from collections import defaultdict, deque


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


# layered topological sort
# Kahn's topo sort
# when there are multiple nodes with 0-indegree => their order is not deterministic

# if there's only 1 node with 0-indegree (deterministic order)
# 1->2, 1->3, 1->4, only node_1 has 0-indegree

# 1->2 alone, is not enough, if there's 3 node, let's add all the node into the in-degree map

# [] in_degree_0 = [...] => all of them has rank at least length of the rest of the node?
# no, single node (3) does not have reachables, and thus does not have a MIN RANK

# 1->3
# 2->3
# 3->4
# 3->5

# [] nodes in the same indegree group (3,4,5) are not reachable from each other
# no outgoing edges from 3,4,5 will reach 3,4,5 (since there's no incoming degree)
# INDUCTION: at the very first step => all of them are SOURCES

# [] if there's only 1 node in the indegree group, the rest is all reachable?
# for a node X, it must not be indegree 0 -> it has a parent -> traverse to parent, if parent is not source then it too has a parent
# or the otherway, current layer -> all node in next layer (since we only removed edges from source) -> continue
# NOTE: only include nodes with edges
# A->B, C
# if we remove C, yeah, B is reachable from A
# if we remove A...
# NOTE:not about removing in order
# always exame the indegree set in 1
# NOTE: Layered topological sort, level decomposition
# AT EACH STEP, WE ARE DEALING WITH SOURCES OF THE GRAPH


# 1->2
# 3->4
# the rest of the node all have indegree ++


def rank_players_linear(match_results, N):
    winner_graph = defaultdict(set)
    loser_graph = defaultdict(set)
    winner_indegree = defaultdict(int)
    loser_indegree = defaultdict(int)

    min_rank = defaultdict(int)
    max_rank = defaultdict(int)

    for winner, loser in match_results:
        winner_graph[winner].add(loser)
        winner_indegree[loser] += 1

        loser_graph[loser].add(winner)
        loser_indegree[winner] += 1

    # layered topological sort
    # first, we deal with winners
    # NOTE: also include nodes with
    winner_indegree_zero = []
    for i in range(1, N + 1):
        if winner_indegree[i] == 0:
            winner_indegree_zero.append(i)
    remaining_nodes = N

    # at each snapshot, exam the source[]
    while winner_indegree_zero:
        if len(winner_indegree_zero) == 1:
            min_rank[winner_indegree_zero[0]] = remaining_nodes
        # remove current layer
        remaining_nodes -= len(winner_indegree_zero)
        next_layer = []
        for node in winner_indegree_zero:
            for neighbor in winner_graph[node]:
                winner_indegree[neighbor] -= 1
                if winner_indegree[neighbor] == 0:
                    next_layer.append(neighbor)
        winner_indegree_zero = next_layer

    # for losers
    loser_indegree_zero = []
    for i in range(1, N + 1):
        if loser_indegree[i] == 0:
            loser_indegree_zero.append(i)
    remaining_nodes = N

    while loser_indegree_zero:
        if len(loser_indegree_zero) == 1:
            max_rank[loser_indegree_zero[0]] = remaining_nodes
        remaining_nodes -= len(loser_indegree_zero)
        next_layer = []
        for node in loser_indegree_zero:
            for neighbor in loser_graph[node]:
                loser_indegree[neighbor] -= 1
                if loser_indegree[neighbor] == 0:
                    next_layer.append(neighbor)
        loser_indegree_zero = next_layer

    return_value = 0
    for i in range(1, N + 1):
        if min_rank[i] + max_rank[i] == N + 1:
            return_value += 1

    return return_value


# NOTE: memoization with reachable node size does not work, but works with reachable node SET.
# DFS + memoization (once a node is visited and the total number of visited node is known)
# memoization, using set(so that we can dedup) not total count.
def rank_players_with_memo(match_results, N):
    graph = defaultdict(set)
    reverse_graph = defaultdict(set)
    for winner, loser in match_results:
        graph[winner].add(loser)
        reverse_graph[loser].add(winner)

    # memoization
    win_memo = {}  # key: node, value: set() of reachable nodes
    lose_memo = {}

    def dfs(node, memo, graph):
        if node in memo:
            return memo[node]
        else:
            reachable_node = set()
            for neighbor in graph[node]:
                # NOTE: running time, each node takes O(n) time
                reachable_node |= dfs(neighbor, memo, graph)
                reachable_node.add(neighbor)  # include self (child)
            memo[node] = (
                reachable_node  # NOTE: Once we finished exploring, the total node size does not increase.
            )
        # print("DFS from node", node, "reached:", memo[node])
        return memo[node]

    return_value = 0

    for i in range(1, N + 1):
        # explore
        win_against = dfs(i, win_memo, graph)
        lose_against = dfs(i, lose_memo, reverse_graph)

        # print(i, win_against, lose_against)
        if len(win_against) + len(lose_against) == N - 1:
            return_value += 1

    return return_value


def rank_players_with_for_loop(match_results, N):
    # first build graph and reversegraph
    graph = defaultdict(set)
    reverse_graph = defaultdict(set)
    for winner, loser in match_results:
        graph[winner].add(loser)
        reverse_graph[loser].add(winner)

    # return a dictionary where the key is the node, value is reachable node sets:
    def helper(graph):
        # build a topological order of the nodes
        in_degree = defaultdict(int)  # node:in_degree(0)
        for i in range(1, N + 1):
            for dest in graph[i]:
                in_degree[dest] += 1

        # Kahn's algorithm for topological sorting
        topo_order = []
        zero_in_degree = deque()
        for i in range(1, N + 1):
            if in_degree[i] == 0:
                zero_in_degree.append(i)

        while zero_in_degree:
            node = zero_in_degree.popleft()
            topo_order.append(node)
            for neighbor in graph[node]:
                in_degree[neighbor] -= 1
                if in_degree[neighbor] == 0:
                    zero_in_degree.append(neighbor)

        return_value = defaultdict(set)
        for i in reversed(topo_order):
            for dest in graph[i]:
                return_value[i] |= return_value[dest]  # union two sets
                return_value[i].add(dest)  # add self
        return return_value

    win_dict = helper(graph)
    lose_dict = helper(reverse_graph)

    return_value = 0
    for i in range(1, N + 1):
        win_against = win_dict[i]
        lose_against = lose_dict[i]

        # print(i, win_against, lose_against)
        if len(win_against) + len(lose_against) == N - 1:
            return_value += 1
    return return_value


# Can we use union-find to solve the repeated node issue?
# have the memo set, contains all the node that's reachable
# (including self, undirected), join a new set is not that expensive.


class DisjointSetUnion:
    def __init__(self, n):
        # Initialize all the A->A, adding all the dots.
        # [0]'s position is not used.
        self.parent = list(range(n + 1))
        self.size = [1] * (n + 1)

    def find(self, x):
        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x])
        return self.parent[x]

    def union(self, x, y):
        rootX = self.find(x)
        rootY = self.find(y)
        if rootX != rootY:
            if self.size[rootX] >= self.size[rootY]:
                # NOTE, next find will flatten less nodes since Y is smaller, and X has already been flattened.
                self.parent[rootY] = rootX
                self.size[rootX] += self.size[rootY]
                self.size[rootY] = 0
            else:
                self.parent[rootX] = rootY
                self.size[rootY] += self.size[rootX]
                self.size[rootX] = 0

    def print(self, x):
        # return all the reachable nodes from x, and x's parent
        root = self.find(x)
        reachable = [i for i in range(1, len(self.parent)) if self.find(i) == root]
        print(
            "For node",
            x,
            "reachable nodes are:",
            reachable,
            "root is:",
            root,
        )


def rank_players_with_union_find(match_results, N):
    graph = defaultdict(set)
    reverse_graph = defaultdict(set)
    for winner, loser in match_results:
        graph[winner].add(loser)
        reverse_graph[loser].add(winner)

    # memoization
    win_memo = DisjointSetUnion(N)
    lose_memo = DisjointSetUnion(N)

    # return a node
    # TODO: handle visited
    # return (root, size_when_first_visited)
    # root is used when exploring its parent, size_when_first_visited is used for final result
    def dfs(node, memo, graph, visited):
        if node in visited:
            # return node, so we don't do repeated calculation
            # NOTE: this only works if when we are exploring, we are adding edges from existing set to new node (adding new parent)
            # it doesn't work if we are adding nodes that are parallel (these parallel nodes will then become falsely connected)
            return (memo.find(node), visited[node])
        for neighbor in graph[node]:
            memo.union(dfs(neighbor, memo, graph, visited)[0], node)
        memo.print(node)
        visited[node] = memo.size[
            memo.find(node)
        ]  # NOTE, DAG, we don't need visited before `for neighbors`, because we will not loop back to stack
        return (memo.find(node), memo.size[memo.find(node)])

    return_value = 0

    win_visited = {}
    lose_visited = {}
    for i in range(1, N + 1):
        # explore
        win_against = dfs(i, win_memo, graph, win_visited)[1]
        # DFS is already doing topological ordering, but it still doesn't work with union_find
        # 1->2, 1->3, 1->4
        # reverse = 1, 4->1, 3->1, 2->1
        lose_against = dfs(i, lose_memo, reverse_graph, lose_visited)[1]

        print(i, win_against, lose_against)
        if win_against + lose_against == N + 1:
            return_value += 1

    return return_value
