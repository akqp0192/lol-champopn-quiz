import json
import os
import tempfile
import unittest

from quiz import Quiz
from quiz_game import QuizGame


class TestQuiz(unittest.TestCase):
    def test_check_correct_answer(self):
        quiz = Quiz("문제", ["A", "B", "C", "D"], 2)
        self.assertTrue(quiz.check_answer(2))

    def test_check_wrong_answer(self):
        quiz = Quiz("문제", ["A", "B", "C", "D"], 2)
        self.assertFalse(quiz.check_answer(1))

    def test_question_and_choices(self):
        quiz = Quiz("문제", ["A", "B", "C", "D"], 2)
        self.assertEqual(quiz.question, "문제")
        self.assertEqual(len(quiz.choices), 4)


class TestQuizGame(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.original_dir = os.getcwd()
        os.chdir(self.temp_dir.name)

    def tearDown(self):
        os.chdir(self.original_dir)
        self.temp_dir.cleanup()

    def test_default_quizzes(self):
        game = QuizGame()
        self.assertGreaterEqual(len(game.quizzes), 5)

    def test_save_and_load_data(self):
        game = QuizGame()
        game.best_score = 5
        game.save_data()

        loaded_game = QuizGame()
        self.assertEqual(loaded_game.best_score, 5)
        self.assertEqual(len(loaded_game.quizzes), len(game.quizzes))

    def test_corrupt_json_recovers_defaults(self):
        with open("state.json", "w", encoding="utf-8") as file:
            file.write("{ invalid json")

        game = QuizGame()
        self.assertGreaterEqual(len(game.quizzes), 5)
        self.assertEqual(game.best_score, 0)

    def test_invalid_quiz_data_recovers_defaults(self):
        invalid_data = {
            "quizzes": [
                {
                    "question": "잘못된 문제",
                    "choices": ["하나", "둘"],
                    "answer": 1
                }
            ],
            "best_score": 0
        }
        with open("state.json", "w", encoding="utf-8") as file:
            json.dump(invalid_data, file, ensure_ascii=False)

        game = QuizGame()
        self.assertGreaterEqual(len(game.quizzes), 5)
        self.assertEqual(game.quizzes[0].question, "구미호라는 별명을 가진 챔피언은?")


if __name__ == "__main__":
    unittest.main()
