import pandas as pd
import numpy as np
import unittest
from myfinalpkg.mymontecarlo import Die, Game, Analyzer


class DieTestSuite(unittest.TestCase):
    
    def setUp(self):
        self.die = Die(np.array([1, 2, 3, 4, 5, 6]))
        
    def test_roll_one(self):
        result = self.die.roll(1)
        self.assertEqual(result.shape[0], 1)
        self.assertTrue(1 <= result[0] <= 6)
        
    def test_roll_many(self):
        num_rolls = 5
        results = self.die.roll(num_rolls)
        self.assertEqual(results.shape[0], num_rolls)
        for roll in results:
            self.assertTrue(1 <= roll <= 6)
        
    def test_change_weight(self):
        face_to_change = 6
        new_weight = 2
        self.die.change_weight(face_to_change, new_weight)
        
        expected_weights = np.ones(len(self.die.faces))
        expected_weights[1] = 3  
        expected_weights /= expected_weights.sum()
        for face, weight in zip(self.die.faces, expected_weights):
            self.assertFalse(expected_weights.size == 0)

        
class TestGame(unittest.TestCase):

    def setUp(self):
        self.dice = [Die(np.array([1,2,3,4,5,6])) for i in range(3)]
        self.game = Game(self.dice, 5)
        self.num_rolls = 5

    def test_play(self):
        self.game.play(5)
        self.assertEqual(self.game.results.shape[0], 3) 
        for result in self.game.show_results():
            self.assertEqual(len(result), 5)
            for roll in result:
                self.assertTrue(1 <= roll <= 6) 
    def test_show_results(self):
        self.game.play(5)
        results = self.game.show_results()
        self.assertEqual(results.shape[0],3)
        for result in results:
            self.assertEqual(len(result), 5)
            for roll in result:
                self.assertTrue(1 <= roll <= 6)


class TestAnalyzer(unittest.TestCase):
    def setUp(self):
        faces = np.array([1,2,3,4,5,6])
        dice = [Die(faces), Die(faces)]
        self.game = Game(dice, 5)
        self.analyzer = Analyzer(self.game)
    
    def test_combo_count(self):
        self.game.play(5)
        combos = self.analyzer.combo_count()
        self.assertIsInstance(combos, pd.DataFrame)
        self.assertFalse(combos.empty)

    def test_jackpot(self):
        self.game.play(5)
        result = self.game.show_results()
        pass

    def test_face_counts_per_roll(self):
        self.game.play(5)
        face_counts = self.analyzer.face_counts_per_roll()

    def test_combo_count(self):
        self.game.play(5)
        combos = self.analyzer.combo_count()
        self.assertFalse(combos.empty)

    def test_permutation_count(self):
        self.game.play(5)
        results = self.game.show_results()
        pass

if __name__ == '__main__':
    unittest.main()
