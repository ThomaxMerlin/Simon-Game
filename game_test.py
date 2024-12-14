import unittest
from unittest.mock import patch
from main import Game

class TestSimonGame(unittest.TestCase):
    def setUp(self):
        """Set up the game instance before each test."""
        self.game = Game()
        self.game.draw_rects()

    def test_add_to_pattern(self):
        """Test that a new color is added to the pattern."""
        initial_length = len(self.game.pattern)
        self.game.add_to_pattern()
        self.assertEqual(len(self.game.pattern), initial_length + 1)
        self.assertIn(self.game.pattern[-1], self.game.colors)

    def test_check_input_correct(self):
        """Test that correct input advances the game."""
        self.game.pattern = ["red", "blue"]
        self.game.next_color = 0
        self.game.check_input("red")
        self.assertEqual(self.game.next_color, 1)
        self.assertFalse(self.game.waiting_for_input)

    def test_check_input_incorrect(self):
        """Test that incorrect input triggers game over."""
        self.game.pattern = ["red", "blue"]
        self.game.next_color = 0
        with patch.object(self.game, "gameover_sound") as mock_game_over:
            self.game.check_input("green")
            mock_game_over.play.assert_called_once()

    def test_update_highscore(self):
        """Test that high scores are updated correctly."""
        self.game.high_scores = [50, 40, 30]
        self.game.score = 35
        self.game.update_highscore()
        self.assertEqual(self.game.high_scores, [50, 40, 35, 30])

        # Test that only top 10 scores are kept
        self.game.high_scores = [100] * 10
        self.game.score = 90
        self.game.update_highscore()
        self.assertEqual(len(self.game.high_scores), 10)
        self.assertNotIn(90, self.game.high_scores)

    def test_game_over(self):
        """Test that game over resets necessary variables."""
        self.game.score = 5
        self.game.pattern = ["red", "blue"]
        self.game.next_color = 1

        with patch.object(self.game, "update_highscore") as mock_update_highscore:
            self.game.game_over()
            mock_update_highscore.assert_called_once()
            self.assertEqual(self.game.score, 0)
            self.assertEqual(self.game.pattern, [])
            self.assertEqual(self.game.next_color, 0)

if __name__ == "__main__":
    unittest.main()
