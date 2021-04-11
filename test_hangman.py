import unittest
import hangman


class TestHangman(unittest.TestCase):

    def setUp(self):
        pass

    def test_checkValidName(self):

        true_results = {'alex shepherd' : True,
                   'al3x ' : False,
                   'hsjk3j22jd skjd3ks' : False,
                   'my name' : True,
                   'Sensyne Health' : True}

        for tc in true_results.keys():
            method_result = hangman.Hangman.checkValidName(tc)
            self.assertEqual(method_result, true_results[tc],
                             """Method result {} != true result {} for example
                             {}""".format(method_result, true_results[tc], tc))

    def test_readAnswers(self):
        pass

    def test_addActionData(self):
        pass

    def test_saveActionData


if __name__ == '__main__':
    unittest.main()
