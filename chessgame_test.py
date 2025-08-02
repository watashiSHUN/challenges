import unittest
from collections import defaultdict

from chessgame import rank_players


class TestRankPlayers(unittest.TestCase):

    def test_linear_ranking(self):
        """Test case where all players have precise rankings: 1>2>3>4"""
        match_results = [(1, 2), (2, 3), (3, 4)]
        N = 4
        result = rank_players(match_results, N)
        self.assertEqual(result, 4, "All 4 players should have precise rankings")

    def test_star_pattern(self):
        """Test case where only player 1 has precise ranking: 1 beats everyone"""
        match_results = [(1, 2), (1, 3), (1, 4)]
        N = 4
        result = rank_players(match_results, N)
        self.assertEqual(result, 1, "Only player 1 should have precise ranking")

    def test_no_games(self):
        """Test case with no games played"""
        match_results = []
        N = 3
        result = rank_players(match_results, N)
        self.assertEqual(result, 0, "No players should have precise rankings")

    def test_single_game(self):
        """Test case with only one game"""
        match_results = [(1, 2)]
        N = 3
        result = rank_players(match_results, N)
        self.assertEqual(result, 0, "No players should have precise rankings")

    def test_complex_tournament(self):
        """Test a more complex tournament structure"""
        match_results = [(1, 2), (1, 3), (2, 3), (2, 4), (3, 4)]
        N = 4
        result = rank_players(match_results, N)
        # This should give us a clear ranking: 1>2>3>4
        self.assertEqual(result, 4, "All players should have precise rankings")


if __name__ == "__main__":
    unittest.main()
