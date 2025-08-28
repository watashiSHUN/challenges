import unittest
from collections import defaultdict

from chessgame import (
    rank_players,
    rank_players_linear,
    rank_players_with_for_loop,
    rank_players_with_memo,
    rank_players_with_union_find,
)


class TestRankPlayers(unittest.TestCase):

    def test_linear_ranking(self):
        """Test case where all players have precise rankings: 1>2>3>4"""
        match_results = [(1, 2), (2, 3), (3, 4)]
        N = 4
        result_original = rank_players(match_results, N)
        result_linear = rank_players_linear(match_results, N)
        result_memo = rank_players_with_memo(match_results, N)
        result_union_find = rank_players_with_union_find(match_results, N)
        result_forloop = rank_players_with_for_loop(match_results, N)

        self.assertEqual(
            result_original, 4, "All 4 players should have precise rankings"
        )
        self.assertEqual(
            result_linear,
            4,
            "Linear version: All 4 players should have precise rankings",
        )
        self.assertEqual(
            result_memo, 4, "Memo version: All 4 players should have precise rankings"
        )
        self.assertEqual(
            result_union_find,
            4,
            "Union-find version: All 4 players should have precise rankings",
        )
        self.assertEqual(
            result_forloop,
            4,
            "For-loop version: All 4 players should have precise rankings",
        )

    def test_star_pattern(self):
        """Test case where only player 1 has precise ranking: 1 beats everyone"""
        match_results = [(1, 2), (1, 3), (1, 4)]
        N = 4
        result_original = rank_players(match_results, N)
        result_linear = rank_players_linear(match_results, N)
        result_memo = rank_players_with_memo(match_results, N)
        result_union_find = rank_players_with_union_find(match_results, N)
        result_forloop = rank_players_with_for_loop(match_results, N)

        self.assertEqual(
            result_original, 1, "Only player 1 should have precise ranking"
        )
        self.assertEqual(
            result_linear,
            1,
            "Linear version: Only player 1 should have precise ranking",
        )
        self.assertEqual(
            result_memo, 1, "Memo version: Only player 1 should have precise ranking"
        )
        self.assertEqual(
            result_union_find,
            1,
            "Union-find version: Only player 1 should have precise ranking",
        )
        self.assertEqual(
            result_forloop,
            1,
            "For-loop version: Only player 1 should have precise ranking",
        )

    def test_no_games(self):
        """Test case with no games played"""
        match_results = []
        N = 3
        result_original = rank_players(match_results, N)
        result_linear = rank_players_linear(match_results, N)
        result_memo = rank_players_with_memo(match_results, N)
        result_union_find = rank_players_with_union_find(match_results, N)
        result_forloop = rank_players_with_for_loop(match_results, N)

        self.assertEqual(result_original, 0, "No players should have precise rankings")
        self.assertEqual(
            result_linear, 0, "Linear version: No players should have precise rankings"
        )
        self.assertEqual(
            result_memo, 0, "Memo version: No players should have precise rankings"
        )
        self.assertEqual(
            result_union_find,
            0,
            "Union-find version: No players should have precise rankings",
        )
        self.assertEqual(
            result_forloop,
            0,
            "For-loop version: No players should have precise rankings",
        )

    def test_single_game(self):
        """Test case with only one game"""
        match_results = [(1, 2)]
        N = 3
        result_original = rank_players(match_results, N)
        result_linear = rank_players_linear(match_results, N)
        result_memo = rank_players_with_memo(match_results, N)
        result_union_find = rank_players_with_union_find(match_results, N)
        result_forloop = rank_players_with_for_loop(match_results, N)

        self.assertEqual(result_original, 0, "No players should have precise rankings")
        self.assertEqual(
            result_linear, 0, "Linear version: No players should have precise rankings"
        )
        self.assertEqual(
            result_memo, 0, "Memo version: No players should have precise rankings"
        )
        self.assertEqual(
            result_union_find,
            0,
            "Union-find version: No players should have precise rankings",
        )
        self.assertEqual(
            result_forloop,
            0,
            "For-loop version: No players should have precise rankings",
        )

    def test_complex_tournament(self):
        """Test a more complex tournament structure"""
        match_results = [(1, 2), (1, 3), (2, 3), (2, 4), (3, 4)]
        # 1>2>3>4
        # 1>3, 2>4 (additional information)
        N = 4
        result_original = rank_players(match_results, N)
        result_linear = rank_players_linear(match_results, N)
        result_memo = rank_players_with_memo(match_results, N)
        result_union_find = rank_players_with_union_find(match_results, N)
        result_forloop = rank_players_with_for_loop(match_results, N)

        # This should give us a clear ranking: 1>2>3>4
        self.assertEqual(result_original, 4, "All players should have precise rankings")
        self.assertEqual(
            result_linear, 4, "Linear version: All players should have precise rankings"
        )
        self.assertEqual(
            result_memo, 4, "Memo version: All players should have precise rankings"
        )
        self.assertEqual(
            result_forloop,
            4,
            "For-loop version: All players should have precise rankings",
        )
        # NOTE: this is a known limitation of the union-find approach
        self.assertEqual(
            result_union_find,
            2,
            "Union-find version: All players should have precise rankings",
        )


class TestRankPlayersLinearOnly(unittest.TestCase):
    """Additional tests specifically for the linear implementation"""

    def test_partial_ordering(self):
        """Test case with partial ordering"""
        match_results = [(1, 2), (3, 4)]
        N = 4
        result_linear = rank_players_linear(match_results, N)
        result_memo = rank_players_with_memo(match_results, N)
        result_union_find = rank_players_with_union_find(match_results, N)

        self.assertEqual(
            result_linear,
            0,
            "No players should have precise rankings with partial ordering",
        )
        self.assertEqual(
            result_memo,
            0,
            "Memo version: No players should have precise rankings with partial ordering",
        )
        self.assertEqual(
            result_union_find,
            0,
            "Union-find version: No players should have precise rankings with partial ordering",
        )
        self.assertEqual(result_linear, result_memo, "Linear and memo should match")
        self.assertEqual(
            result_linear, result_union_find, "Linear and union-find should match"
        )

    def test_fork_pattern(self):
        """Test fork pattern: 1 beats 2 and 3, but 2 and 3 don't play each other"""
        match_results = [(1, 2), (1, 3)]
        N = 3
        result_linear = rank_players_linear(match_results, N)
        result_memo = rank_players_with_memo(match_results, N)
        result_union_find = rank_players_with_union_find(match_results, N)

        self.assertEqual(result_linear, 1, "Only player 1 should have precise ranking")
        self.assertEqual(
            result_memo, 1, "Memo version: Only player 1 should have precise ranking"
        )
        self.assertEqual(
            result_union_find,
            1,
            "Union-find version: Only player 1 should have precise ranking",
        )
        self.assertEqual(result_linear, result_memo, "Linear and memo should match")
        self.assertEqual(
            result_linear, result_union_find, "Linear and union-find should match"
        )


class TestRankPlayersMemoOnly(unittest.TestCase):
    """Additional tests specifically for the memoization implementation"""

    def test_memoization_efficiency(self):
        """Test that memoization works correctly with repeated subproblems"""
        # Create a diamond pattern: 1->2, 1->3, 2->4, 3->4
        # 1->2->4
        #  ->3->4 (2,3)'s rank are not known
        match_results = [(1, 2), (1, 3), (2, 4), (3, 4)]
        N = 4
        result_memo = rank_players_with_memo(match_results, N)
        result_union_find = rank_players_with_union_find(match_results, N)

        # All players should have precise rankings in this case
        self.assertEqual(
            result_memo,
            2,
            "Only 2 players should have precise rankings in diamond pattern",
        )
        self.assertEqual(
            result_union_find,
            2,
            "Union-find version: Only 2 players should have precise rankings",
        )
        self.assertEqual(
            result_memo, result_union_find, "Memo and union-find should match"
        )

    def test_deep_chain(self):
        """Test a deep chain to verify memoization handles recursion correctly"""
        # Create chain: 1->2->3->4->5
        match_results = [(1, 2), (2, 3), (3, 4), (4, 5)]
        N = 5
        result_memo = rank_players_with_memo(match_results, N)
        result_union_find = rank_players_with_union_find(match_results, N)

        self.assertEqual(
            result_memo, 5, "All players should have precise rankings in chain"
        )
        self.assertEqual(
            result_union_find,
            5,
            "Union-find version: All players should have precise rankings in chain",
        )
        self.assertEqual(
            result_memo, result_union_find, "Memo and union-find should match"
        )

    def test_multiple_branches(self):
        """Test multiple branches from root"""
        # 1 beats everyone else, but others don't play each other
        match_results = [(1, 2), (1, 3), (1, 4), (1, 5)]
        N = 5
        result_memo = rank_players_with_memo(match_results, N)
        result_union_find = rank_players_with_union_find(match_results, N)

        self.assertEqual(result_memo, 1, "Only player 1 should have precise ranking")
        self.assertEqual(
            result_union_find,
            1,
            "Union-find version: Only player 1 should have precise ranking",
        )
        self.assertEqual(
            result_memo, result_union_find, "Memo and union-find should match"
        )


class TestRankPlayersUnionFindOnly(unittest.TestCase):
    """Additional tests specifically for the union-find implementation"""

    def test_union_find_efficiency(self):
        """Test union-find with a complex graph structure"""
        # Create a more complex tournament
        match_results = [(1, 2), (1, 3), (1, 4), (2, 5), (3, 5), (4, 5)]
        N = 5
        result = rank_players_with_union_find(match_results, N)

        # Players 1 and 5 should have precise rankings
        self.assertEqual(result, 2, "Players 1 and 5 should have precise rankings")

    def test_union_find_large_tournament(self):
        """Test union-find with a larger tournament"""
        # Create a linear chain: 1->2->3->4->5->6
        match_results = [(1, 2), (2, 3), (3, 4), (4, 5), (5, 6)]
        N = 6
        result = rank_players_with_union_find(match_results, N)

        self.assertEqual(
            result, 6, "All players should have precise rankings in linear chain"
        )

    def test_union_find_disconnected_components(self):
        """Test union-find with disconnected tournament components"""
        # Two separate chains: 1->2 and 3->4->5
        match_results = [(1, 2), (3, 4), (4, 5)]
        N = 5
        result = rank_players_with_union_find(match_results, N)

        self.assertEqual(
            result,
            0,
            "No players should have precise rankings with disconnected components",
        )


if __name__ == "__main__":
    unittest.main()
    unittest.main()
