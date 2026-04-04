import os
from constants import FILE_PATH, DEFAULT_QUIZZES


class Quiz:
    def __init__(self, question, choices, answer):
        self.question = question
        self.choices = choices
        self.answer = answer

    def display_quiz(self):
        print(self.question)
        for i, choice in enumerate(self.choices):
            print(f"{i + 1}. {choice}")

    def check_answer(self, answer):
        return self.answer == answer


class QuizGame:
    def __init__(self):
        self.quizzes = []
        self.best_score = 0

    def show_menu(self):
        print("=" * 30)
        print("파이썬 기초 문법 퀴즈")
        print("=" * 30)
        print("1. 퀴즈 풀기")
        print("2. 퀴즈 추가")
        print("3. 퀴즈 목록")
        print("4. 점수 확인")
        print("5. 종료")
        print("=" * 30)

    def load_quizzes(self):
        if os.path.isfile(FILE_PATH):
            try:
                pass
            except Exception:
                pass
        if not self.quizzes:
            self.quizzes = [Quiz(**quiz) for quiz in DEFAULT_QUIZZES]
