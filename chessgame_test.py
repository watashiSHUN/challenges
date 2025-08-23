import unittest
from collections import defaultdict

from chessgame import rank_players, rank_players_linear


class TestRankPlayers(unittest.TestCase):

    def test_linear_ranking(self):
        """Test case where all players have precise rankings: 1>2>3>4"""
        match_results = [(1, 2), (2, 3), (3, 4)]
        N = 4
        result_original = rank_players(match_results, N)
        result_linear = rank_players_linear(match_results, N)
        self.assertEqual(result_original, 4, "All 4 players should have precise rankings")
        self.assertEqual(result_linear, 4, "Linear version: All 4 players should have precise rankings")
        self.assertEqual(result_original, result_linear, "Both functions should return same result")

    def test_star_pattern(self):
        """Test case where only player 1 has precise ranking: 1 beats everyone"""
        match_results = [(1, 2), (1, 3), (1, 4)]
        N = 4
        result_original = rank_players(match_results, N)
        result_linear = rank_players_linear(match_results, N)
        self.assertEqual(result_original, 1, "Only player 1 should have precise ranking")
        self.assertEqual(result_linear, 1, "Linear version: Only player 1 should have precise ranking")
        self.assertEqual(result_original, result_linear, "Both functions should return same result")

    def test_no_games(self):
        """Test case with no games played"""
        match_results = []
        N = 3
        result_original = rank_players(match_results, N)
        result_linear = rank_players_linear(match_results, N)
        self.assertEqual(result_original, 0, "No players should have precise rankings")
        self.assertEqual(result_linear, 0, "Linear version: No players should have precise rankings")
        self.assertEqual(result_original, result_linear, "Both functions should return same result")

    def test_single_game(self):
        """Test case with only one game"""
        match_results = [(1, 2)]
        N = 3
        result_original = rank_players(match_results, N)
        result_linear = rank_players_linear(match_results, N)
        self.assertEqual(result_original, 0, "No players should have precise rankings")
        self.assertEqual(result_linear, 0, "Linear version: No players should have precise rankings")
        self.assertEqual(result_original, result_linear, "Both functions should return same result")

    def test_complex_tournament(self):
        """Test a more complex tournament structure"""
        match_results = [(1, 2), (1, 3), (2, 3), (2, 4), (3, 4)]
        N = 4
        result_original = rank_players(match_results, N)
        result_linear = rank_players_linear(match_results, N)
        # This should give us a clear ranking: 1>2>3>4
        self.assertEqual(result_original, 4, "All players should have precise rankings")
        self.assertEqual(result_linear, 4, "Linear version: All players should have precise rankings")
        self.assertEqual(result_original, result_linear, "Both functions should return same result")


class TestRankPlayersLinearOnly(unittest.TestCase):
    """Additional tests specifically for the linear implementation"""
    
    def test_partial_ordering(self):
        """Test case with partial ordering"""
        match_results = [(1, 2), (3, 4)]
        N = 4
        result = rank_players_linear(match_results, N)
        self.assertEqual(result, 0, "No players should have precise rankings with partial ordering")
    
    def test_fork_pattern(self):
        """Test fork pattern: 1 beats 2 and 3, but 2 and 3 don't play each other"""
        match_results = [(1, 2), (1, 3)]
        N = 3
        result = rank_players_linear(match_results, N)
        self.assertEqual(result, 1, "Only player 1 should have precise ranking")


if __name__ == "__main__":
    unittest.main()
