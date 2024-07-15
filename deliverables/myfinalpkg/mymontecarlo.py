import random
import pandas as pd
import numpy as np

class Die:
    """
    This class may look threatening, but it's just an n-sided die. 
    How many faces does it have? N. What are the weights of those faces? W.
    """
    
    def __init__(self, faces, weights=None):
        """ Number of faces on the die. Just count them. You can do it. 
        Pass a list of unique strings or integers as faces."""
        
        if not isinstance(faces, np.ndarray):
            raise TypeError("Faces must be a numpy array. Didn't I mention that?")        
        if faces.dtype not in [int, float, str]:
            raise TypeError("Faces must be strings or integers. Okay, that one I *know* I told you about.")
        if len(faces) != len(set(faces)):
            raise ValueError("Faces must be distinct. I know, I know, it's a lot to ask.")
        self.faces = faces
        weights = np.ones(len(faces)) / len(faces)
        self.weights = weights
        self.__die_hard = pd.DataFrame({'weights': self.weights}, index=faces)
        
    
    def change_weight(self, face_to_change, new_weight):
        """The function to change the weight of a single face.
        Parameters:
            face (str or int): The face value to be changed.
            new_weight (int or float): The new weight."""
            
        if face_to_change not in self.__die_hard.index:
            raise IndexError("Face value not found in die.")
        try:
            new_weight = float(new_weight)
        except ValueError:
            raise TypeError("Weight must be numeric.")
        self.__die_hard.at[face_to_change, 'weights'] = new_weight
        

    def roll(self, num_rolls=1):
        """The function to roll the die a given number of times.
        Parameters:
        num_rolls (int): The number of times to roll the die."""
        return np.random.choice(self.faces, size = num_rolls, p=self.__die_hard['weights'])
    
    
    def show_state(self):
        """The function to show the die's current state."""
        return self.__die_hard.copy()

class Game:
    """ This class is a game. It represents a game of rolling one or more similar dice.

    Attributes:
        dice (list): A list of Die objects.
        results (list): The results of the most recent play."""

    def __init__(self, dice, num_rolls):
        """This is the constructor for Game class. It initializes the dice and results attributes.
        Parameters:
            similar dice (list): A list of Die objects.
        """
        if not all(isinstance(d, Die) for d in dice):
            raise TypeError("All dice must be Die objects. Last one, I promise :)")
        self.dice = dice
        self.results = None
        self.num_rolls = num_rolls
        

    def play(self, num_rolls):
        """
        Roll all of the dice a given number of times. PLAY THE GAME!

        Parameters:
            num_rolls (int): The number of times to roll the dice.
        """
        
        roll_results = [die.roll(num_rolls) for die in self.dice]
        self.results = np.array(roll_results)
        roll_results = np.transpose(roll_results)
        return self.results
    
    def show_results(self):
        """Shows the results of the game."""
        if self.results is None:
            raise ValueError("No results to show. Play the game first.")
        return self.results
        
class Analyzer:
    """A class representing an analyzer for the results of a game of rolling dice.

    Attributes:
        game (Game): The game to analyze."""

    def __init__(self, game):
        """The constructor for Analyzer class. Do not destroy."""
        self.game = game
    
    def face_counts_per_roll(self):
        results = self.game.show_results()
        face_counts = pd.DataFrame(results).apply(pd.Series.value_counts, axis=1).fillna(0).astype(int)
        return face_counts
        
    def jackpot(self):
        """The function to compute the number of jackpots in the game.

        Returns:
            int: The number of jackpots."""
        results = self.game.show_results()
        jackpots = sum(1 for result in results if len(set(result)) == 1)
        return jackpots
        
        
    def face_counts_per_roll(self):
        """The function to compute the face counts per roll.

        Returns:
            DataFrame: A DataFrame where each row corresponds to a roll,
            each column corresponds to a face, 
            and each cell contains the count of that face in that roll. """
        results = self.game.show_results()
        face_counts = [pd.Series(result).value_counts() for result in results]
        results_df = pd.DataFrame(face_counts).fillna(0)
    
    def combo_count(self):
        """
        The function to compute the distinct combinations of faces rolled, along with their counts.

        Returns:
            DataFrame: A DataFrame with a MultiIndex of distinct combinations and a column for the associated counts.
        """
        results = self.game.show_results()
        combos = pd.Series(tuple(sorted(result)) for result in results).value_counts().to_frame('count')
        combos.index.name = 'combination'
        return combos
    
    def permutation_count(self):
        """
        The function to compute the distinct permutations of faces rolled, along with their counts.

        Returns:
            DataFrame: A DataFrame with a MultiIndex of distinct permutations and a column for the associated counts.
        """
        results = self.game.show_results()
        permutations = pd.Series(tuple(result) for result in results).value_counts().to_frame()
        return permutations
    
    
