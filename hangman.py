import pandas as pd
import numpy as np
import os
import re
from datetime import datetime


class Hangman:
    """
    Get ready with some Hangman fun with the Hangman game class!
    Interpreting from the given problem specification, the Hangman game consists of
    one word only.
    """

    def __init__(self):
        # Prompt user for name
        self.username = self.getName(user=True)
        # To also give the stickman a name!
        self.hangman_name = self.getName(user=False)
        # Answers to the Hangman game
        self.answer = self.getAnswer(os.path.join(os.getcwd(), 'DATA', 'answers.csv'))
        # Scoreboard data
        self.scoreboard = self.loadScoreboard(
            os.path.join(os.getcwd(), 'DATA', 'scoreboard.csv')
        )
        # User's answer
        self.user_answer = None
        # User Interaction data
        try:
            self.ux_data = pd.read_csv(os.path.join(os.getcwd(), 'DATA', 'ux_data.csv'))
        except:
            self.ux_data = None
        # Log starting the game
        self.addActionData('sg')

    @staticmethod
    def checkValidName(name):
        """
        Checks that the inputted name from the user is a valid name (i.e. one which contains
        alphabetic characters only. The regular expression warrants the user putting in their first
        (and surname).
        Names are also restricted to 50 characters maximum so that, when it comes to
        storing names into a SQL database, we can ensure that name string will not go ad finitum.
        :param
        name: String
            Inputted name from user
        :return
        Tuple of Booleans
            1) If inputted name matches regular expression.
            2) If length of the name is under 50 characters
        """

        return bool(re.fullmatch(pattern=r'([a-zA-Z]+[ -]?)+', string=name)), len(name) <= 50

    def getName(self, user=True):
        """
        Prompts user for both their name and the stickman's name, which will be stored throughout the game.
        The method also checks that input name string is a valid name (i.e. does not
        contain numbers, etc.)

        :param
        user : Boolean
            Flag to switch between user and stickman name entry

        :return
        name : String
            Name of the user
        """

        # Tracker variable for while loop to track if inputted name is valid
        valid = False
        name = None

        while not valid:
            if user:
                s = 'Your'
            else:
                s = 'Stickman\'s'

            name = str(input('{} Name >> '.format(s)))

            v1, v2 = self.checkValidName(name)
            valid = v1 and v2
            if name == 'quit':
                # Adding action data to say that user has quit game.
                self.quitGame()
                break
            if not v1:
                print('Please type a valid name (e.g. Joe Blogs or Joe)')
            if not v2:
                print('The name you have given is too long. Please write a shorter name!')

        return name

    @staticmethod
    def getAnswer(answer_path):
        """
        Reads answer file
        :return
        answers : List of Strings
            Answers to the Hangman game
        """

        answers = pd.read_csv(answer_path, index_col=0)
        # Randomly shuffles answers to add variation to the game instances
        answers = answers.sample(frac=1)
        # Selecting the first answer in the shuffled dataframe.
        answer = answers.iloc[0, 0]

        return answer

    # -----
    # GAMEPLAY
    # -----

    def setUpRound(self):

        # To -1 character to remove final space
        user_answer = re.sub(string=self.answer, pattern=r'\w', repl='_ ')[:-1]
        print(user_answer)

        return user_answer

    def inputChar(self):
        """
        Asks user for next character guess in the game and checks whether the text input is valid
        (i.e. one character long and is a alphabetic character.)

        :return
        char : String
            Valid character
        """

        char = None

        while char is None:
            char = str(input('>>>'))
            if len(char) != 1:
                # Either entered 0 or 2+ characters
                char = None
                print('Please insert only one character!')
                if char == 'quit':
                    self.quitGame()
                    break
            elif char.isdigit():
                char = None
                print('Please insert a letter from the alphabet!')

        return char

    def updateUserAnswer(self, user_chars):
        """
        Checks whether the most recent guess of character is in the answer or not.

        :param
        user_chars: List of characters (string)
            List of attempted characters
        :return
        correct : Boolean
            Is the most recent character guess in the word or not?
        """

        unique_answer_chars = set(list(self.answer))

        # Checking most recent character guess against unique set of characters in answer.
        if user_chars[-1] in unique_answer_chars:
            # Correct guess
            # update self.user_answer to include character
            correct_chars = list(set(user_chars).intersection(unique_answer_chars))
            new_user_answer = re.sub(string=self.answer.lower(),
                                     pattern=r'[^{}]'.format(''.join(correct_chars)),
                                     repl='_')
            new_user_answer = ' '.join(list(new_user_answer))

            self.user_answer = new_user_answer.upper()
            correct = True
        else:
            # Incorrect guess
            correct = False

        return correct

    def updateHangmanGraphic(self, incorrect_guesses):

        pictures = ["""========
                       +------+
                       |      |
                       O      |
                      /|\     |
                      / \     |
                              |
                       ========
                            """,
                    """========
                       +------+
                       |      |
                       O      |
                      /|\     |
                      /       |
                              |
                       ========
                            """,
                    """========
                       +------+
                       |      |
                       O      |
                      /|\     |
                              |
                              |
                       ========
                            """,
                    """========
                       +------+
                       |      |
                       O      |
                      /|      |
                              |
                              |
                       ========
                            """,
                    """========
                       +------+
                       |      |
                       O      |
                              |
                              |
                              |
                       ========
                            """,
                    """========
                       +------+
                       |      |
                              |
                              |
                              |
                              |
                       ========
                            """]

        print(pictures[incorrect_guesses])

    def game(self):

        # Number of incorrect guesses, as specified.
        incorrect_guesses = 6
        # Stores all character guesses
        user_guesses = []
        # The current answer presented to the user.
        self.user_answer = self.setUpRound()

        while self.user_answer.count('_') > 0 and incorrect_guesses <= 0:
            # Ask user for a valid character
            char = self.inputChar()

            # Log action into database
            self.addActionData('i{}'.format(char))

            if char in user_guesses:
                print('''You have already guessed {} (along with {}!)
                , please try another character.'''.format(char,
                                                          ', '.join(list(set(user_guesses) - set(char)))))
                continue
            else:
                # Adding user guess to user_guesses list
                user_guesses.append(char)

            correct = self.updateUserAnswer(user_guesses)

            if not correct:
                print('Poor {}!!! {} is not in the word(s)! Sorry, {}'.format(self.hangman_name,
                                                                              user_guesses[-1],
                                                                              self.username))
                incorrect_guesses -= 1
                self.updateHangmanGraphic(incorrect_guesses)
            else:
                print('{} is in the word(s)! Good job, {}!'.format(user_guesses[-1], self.username))

        if incorrect_guesses <= 0:
            print("""Uh oh!! It looks like {} is dead! Sorry, {},
            maybe you can save {} next time!!""".format(self.username, self.hangman_name,
                                                        self.hangman_name))
        elif self.user_answer.count('_') == 0:
            print("""WELL DONE {}!!! {} can live for another day!""".format(self.username, self.hangman_name))
            self.updateScoreboard()

        self.quitGame()

    def quitGame(self):
        self.addActionData('qg')
        self.saveActionData()
        self.showTop10()
        print('Goodbye, {}!'.format(self.username))

    # -----
    # ACTION DATA
    # -----

    def addActionData(self, action=''):
        """
        Updates Action entry to self.user_data
        :param
        action: String
            Two-character long reference to game action
        """

        entry = [datetime.today(), self.username, action]
        try:
            entry = pd.concat([self.ux_data, np.array(entry)], axis=0)
        except:
            self.ux_data = pd.DataFrame(entry, columns=['Time', 'Username', 'Action'])

    def saveActionData(self):
        """
        Saves self.user_data when the user completes of quits the game.
        :return:
        """

        self.ux_data.to_csv(os.path.join(os.getcwd(), "DATA", 'ux_data.csv'))

    # -----
    # SCOREBOARD
    # -----

    @staticmethod
    def loadScoreboard(scoreboard_path):

        try:
            scoreboard = pd.read_csv(scoreboard_path, index_col=0)
            scoreboard.loc[:, 'Points'] = scoreboard.loc[:, 'Points'].astype(int)
        except:
            scoreboard = None

        return scoreboard

    def updateScoreboard(self):

        # Adding 1 to the user's score to reduce space complexity.
        try:
            self.scoreboard.at[self.username, 'Points'] += 1
        except IndexError:
            self.scoreboard = pd.concat([self.scoreboard, [self.username, 1]])
        except ValueError:
            self.scoreboard = pd.DataFrame([self.username, 1], columns=['Username', 'Points'])
            self.scoreboard = self.scoreboard.set_index('Username')

    def showTop10(self):
        """
        Presents top 10 scoring users on the terminal

        :return:
        """

        pointsPerGame = 10

        # Sorting entries by Points, with highest first.
        self.scoreboard = self.scoreboard.sort_values('Points', ascending=False)
        # Multiplying by points per game to get total points.
        self.scoreboard.loc[:, 'Points'] = self.scoreboard.loc[:, 'Points'] * pointsPerGame

        # Showing top 10 scorers.
        print(self.scoreboard.head(10))
