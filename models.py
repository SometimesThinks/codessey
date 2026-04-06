import os
import json
from random import sample, choice
from utils import get_num_input, get_text_input
from constants import FILE_PATH, DEFAULT_QUIZZES
from datetime import datetime


class Quiz:
    def __init__(self, question, choices, answer):
        self.question = question
        self.choices = choices
        self.answer = answer
        # 정답을 제외한 나머지 선택지 중 하나를 힌트로 저장
        self.hint = choice(
            [i + 1 for i in range(len(choices)) if str(i + 1) != str(answer)]
        )

    def display_quiz(self):
        print(self.question)
        for i, choice in enumerate(self.choices):
            print(f"{i + 1}. {choice}")

    def check_answer(self, answer):
        return self.answer == answer


class QuizGame:
    def __init__(self):
        self.quizzes = []
        self.best_score = None
        self.history = []

    # 현재 사용할 퀴즈 리스트를 결정(내 퀴즈가 있으면 내 걸, 없으면 기본 퀴즈 반환)
    def get_current_quizzes(self):
        if self.quizzes:
            return self.quizzes
        return DEFAULT_QUIZZES

    # 메뉴 출력
    def show_menu(self):
        print("=" * 30)
        print("파이썬 기초 문법 퀴즈")
        print("=" * 30)
        print("1. 퀴즈 풀기")
        print("2. 퀴즈 추가")
        print("3. 퀴즈 삭제")
        print("4. 퀴즈 목록")
        print("5. 최고 점수 확인")
        print("6. 퀴즈 풀이 기록")
        print("7. 종료")
        print("=" * 30)

    # 퀴즈 불러오기
    def load_quizzes(self):
        if os.path.isfile(FILE_PATH):
            try:
                with open(FILE_PATH, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    self.quizzes = data.get("quizzes", [])
                    self.best_score = data.get("best_score", None)
                    self.history = data.get("history", [])
            except Exception:
                print("파일을 불러오는 중 오류가 발생했습니다.")

    # 퀴즈 풀기
    def play_quiz(self):
        # 퀴즈 원본
        all_quizzes = self.get_current_quizzes()
        # 퀴즈 수 입력 받기
        count = get_num_input(
            f"총 {len(all_quizzes)}개의 퀴즈 중 풀고 싶은 퀴즈 수를 입력하세요: ",
            1,
            len(all_quizzes),
        )
        # 퀴즈 셔플
        quizzes_to_play = sample(all_quizzes, int(count))
        # 퀴즈 시작
        print("=" * 30)
        print("퀴즈를 시작합니다!")
        print("=" * 30)
        score = 0
        try:
            for quiz in quizzes_to_play:
                quiz = Quiz(**quiz)
                quiz.display_quiz()
                used_hint = False

                while True:
                    answer = get_num_input("정답(힌트 보기는 0번 입력): ", 0, 4)
                    if answer == "0":
                        print(f"힌트: {quiz.hint}번은 정답이 아닙니다!")
                        used_hint = True
                    else:
                        break
                # 정답 확인 및 점수 부여
                if quiz.check_answer(answer):
                    if used_hint:
                        score += 5
                        print("정답입니다! (힌트 사용: +5점)")
                    else:
                        score += 10
                        print("정답입니다! (힌트 미사용: +10점)")
                    self.update_best_score(score)
                else:
                    print("아쉽지만 오답입니다...")
                print()
        except KeyboardInterrupt:
            print("\n퀴즈가 중단되었습니다.")
            raise
        except EOFError:
            print("\n퀴즈가 중단되었습니다.")
            raise
        finally:
            record = {
                "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "score": score,
                "total_questions": len(quizzes_to_play),
            }
            self.history.append(record)
            print("=" * 30)
            print(f"총 점수: {score}점")
            # 최고 점수 업데이트
            if self.update_best_score(score):
                print("최고 점수 갱신!")
            print("=" * 30)

    # 퀴즈 추가
    def add_quiz(self):
        print("=" * 30)
        print("퀴즈를 추가합니다!")
        print("=" * 30)
        question = get_text_input("문제: ")
        choices = []
        for i in range(4):
            choice = get_text_input(f"{i + 1}. ")
            choices.append(choice)
        answer = get_num_input("정답: ", 1, 4)
        self.quizzes.append(
            {"question": question, "choices": choices, "answer": answer}
        )
        # 퀴즈 변경 사항 저장(추가, 삭제)
        if self.save_quizzes():
            print("퀴즈가 추가되었습니다!")
        else:
            self.quizzes.pop()
            print("퀴즈 추가에 실패했습니다.")

    # 퀴즈 변경 사항 저장(추가, 삭제)
    def save_quizzes(self):
        try:
            data = {
                "best_score": self.best_score,
                "quizzes": self.quizzes,
                "history": self.history,
            }
            with open(FILE_PATH, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=4)
            return True
        except Exception:
            return False

    # 퀴즈 삭제
    def delete_quiz(self):
        # 퀴즈가 없을 경우
        if not self.quizzes:
            print("등록된 퀴즈가 없습니다.")
            return
        # 퀴즈 삭제 시작
        print("=" * 30)
        print("퀴즈를 삭제합니다.")
        print("=" * 30)
        self.show_quizzes()
        index = get_num_input("삭제할 퀴즈 번호를 입력하세요: ", 1, len(self.quizzes))
        popped = self.quizzes.pop(int(index) - 1)
        if self.save_quizzes():
            print("퀴즈가 삭제되었습니다!")
        else:
            self.quizzes.insert(int(index) - 1, popped)
            print("퀴즈 삭제에 실패했습니다.")

    # 퀴즈 목록
    def show_quizzes(self):
        quizzes_to_show = self.get_current_quizzes()
        print("=" * 30)
        print("퀴즈 목록")
        print("=" * 30)
        for i, quiz in enumerate(quizzes_to_show):
            print(f"{i + 1}. {quiz['question']}")
            for j, choice in enumerate(quiz["choices"]):
                print(f"   {j + 1}. {choice}")
            print(f"   정답: {quiz['answer']}")
            print()
        print("=" * 30)

    # 점수 확인
    def show_best_score(self):
        print("=" * 30)
        if self.best_score is None:
            print("아직 퀴즈 풀이 기록이 없습니다.")
        else:
            print(f"최고 점수 : {self.best_score}")
        print("=" * 30)

    # 최고 점수 업데이트
    def update_best_score(self, score):
        if self.best_score is None or score > self.best_score:
            self.best_score = score
            return True
        return False

    # 퀴즈 풀이 기록
    def show_history(self):
        print("=" * 30)
        print("퀴즈 풀이 기록")
        print("=" * 30)
        if not self.history:
            print("아직 퀴즈 풀이 기록이 없습니다.")
            return
        for i, record in enumerate(self.history):
            print(
                f"{i + 1}. {record['date']} - {record['score']}점 ({record['total_questions']}문제)"
            )
        print("=" * 30)
