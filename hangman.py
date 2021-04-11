import pandas as pd
import numpy as np
import os
import re
import time

class Hangman:
    """
    Get ready with some Hangman fun with the Hangman game class!
    """

    def __init__(self):
        # Prompt user for name
        self.username = self.getName()
        # Number of points the user has in the game
        self.points = 0
        # Answers to the Hangman game
        self.answers = self.readAnswers(os.path.join(os.getcwd(), 'DATA', 'answers.csv'))
        self.scoreboard = self.loadScoreboard(
            os.path.join(os.getcwd(), 'DATA', 'scoreboard.csv')
        )
        # User Interaction data
        try:
            self.user_data = pd.read_csv(os.path.join(os.getcwd(), 'DATA', 'user_data.csv'))
        except:
            self.user_data = None

    def checkValidName(self, name):
        """
        Checks that the inputted name from the user is a valid name (i.e. one which contains
        alphabetic characters only. The regular expression warrants the user putting in their first
        (and surname).
        Names are also restricted to 50 characters maximum so that, when it comes to
        storing names into a SQL database, we can ensure that name string will not go ad infinitum.
        :param
        name: String
            Inputted name from user
        :return
        Tuple of Booleans
            1) If inputted name matches regular expression.
            2) If length of the name is under 50 characters
        """

        return re.match(pattern=r'([a-zA-Z]+[ -]?)+', string=name), len(name) <= 50

    def getName(self):
        """
        Prompts user for name, which will be stored throughout the game.
        The method also checks that input name string is a valid name (i.e. does not
        contain numbers, etc.)

        :return
        name : String
            Name of the user
        """

        # Tracker variable for while loop to track if inputted name is valid
        valid = False

        while not valid:
            name = str(input('Name >> '))
            v1, v2 = self.checkValidName(name)
            valid = v1 and v2
            if name == 'quit':
                # Adding action data to say that user has quit game.
                self.addActionData('qg')
                break
            if not v1:
                print('Please type a valid name (e.g. Joe Blogs or Joe)')
            if not v2:
                print('The name you have given is too long. Please write a shorter name!')

        return name

    def readAnswers(self, answer_path):
        """
        Reads answer file
        :return:
        answers : List of Strings
            Answers to the Hangman game
        """

        answers = pd.read_csv(answer_path, index_col=0)
        # Randomly shuffles answers to add variation to the game instances
        answers = answers.sample(frac=1)

        return answers

    # -----
    # ACTION DATA
    # -----

    def addActionData(self, action=''):
        """
        Adds Action entry to self.user_data
        :param action:
        :return:
        """

        pass

    def saveActionData(self):
        """
        Saves self.user_data when the user completes of quits the game.
        :return:
        """

        pass

class Round(Hangman):

    def __init__(self, answer):
        """

        :param
        answer: String
            Answer to be guessed by user
        """

        self.word = answer

    def setUpRound(self):



"""
  +---+
  |   |
  O   |
 /|\  |
 / \  |
      |
"""