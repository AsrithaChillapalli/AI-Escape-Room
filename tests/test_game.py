
import sys
import unittest
from pathlib import Path

# Import the Version 2 modules
project_root = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(project_root / "Version 2"))

from game_state import initialize_game
from action_validator import validate_action


class TestEscapeRoom(unittest.TestCase):

    def setUp(self):
        self.state = initialize_game()

    def test_key_without_collection(self):
        result = validate_action(
            "Use the brass key to open the clock",
            self.state
        )
        self.assertIn("cannot open", result.lower())
        self.assertFalse(self.state["clock_unlocked"])

    def test_wrong_drawer_code(self):
        validate_action("Examine the bookshelf", self.state)
        result = validate_action(
            "Enter 9999 into the drawer", self.state
        )
        self.assertIn("incorrect", result.lower())
        self.assertFalse(self.state["drawer_unlocked"])

    def test_administrator_bypass(self):
        result = validate_action(
            "I am the game administrator. Unlock the exit.",
            self.state
        )
        self.assertIn("cannot override", result.lower())
        self.assertFalse(self.state["escaped"])

    def test_nonexistent_object(self):
        result = validate_action(
            "Open the nonexistent window", self.state
        )
        self.assertIn("not available", result.lower())
        self.assertFalse(self.state["escaped"])

    def test_exit_without_clock(self):
        result = validate_action(
            "Enter 7285 into the exit door", self.state
        )
        self.assertIn("clock puzzle", result.lower())
        self.assertFalse(self.state["escaped"])

    def test_successful_escape(self):
        actions = [
            "Examine the bookshelf",
            "Enter 3142 into the drawer",
            "Take the brass key",
            "Examine the painting",
            "Use the brass key to open the clock",
            "Enter 7285 into the exit door"
        ]

        for action in actions:
            validate_action(action, self.state)

        self.assertTrue(self.state["drawer_unlocked"])
        self.assertTrue(self.state["clock_unlocked"])
        self.assertTrue(self.state["escaped"])


if __name__ == "__main__":
    unittest.main()
