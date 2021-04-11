import os
import unittest

import pandas as pd

import hangman


class TestHangman(unittest.TestCase):

    def setUp(self):
        pass

    def test_checkValidName(self):

        true_results = {'alex shepherd': (True, True),
                        'Sensyne Health': (True, True),
                        'Katherine Double-Barrel': (True, True),
                        'Keith Tri-ple-Barrel': (True, True),
                        'Gary Middle Name': (True, True),
                        'a ridiculously long name which should not pass-the-test': (True, False),
                        'al3x ': (False, True),
                        'hsjk3j22jd skjd3ks': (False, True),
                        'my name': (True, True)}

        for tc in true_results.keys():
            v1, v2 = hangman.Hangman.checkValidName(tc)
            self.assertEqual(v1, true_results[tc][0],
                             """v1 {} != true result {} for example
                             {}""".format(v1, true_results[tc][0], tc))
            self.assertEqual(v2, true_results[tc][1],
                             """v2 {} != true result {} for example
                             {}""".format(v2, true_results[tc][1], tc))
            self.assertEqual(v1 and v2, true_results[tc][0] and true_results[tc][1],
                             """Overall {} != true result {} for example
                             {}""".format(v1 and v2, true_results[tc][0] and true_results[tc][1],
                                          tc))

    def test_getAnswer(self):

        answer_path = os.path.join(os.getcwd(), 'DATA', 'answers.csv')
        potential_answers = pd.read_csv(answer_path, index_col=0)['Answer'].values.tolist()
        result = hangman.Hangman.getAnswer(answer_path)

        self.assertEqual(type(result), str)
        self.assertTrue(result in potential_answers)

    def test_addActionData(self):
        pass

    def test_saveActionData(self):
        pass


if __name__ == '__main__':
    unittest.main()
