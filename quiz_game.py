
import json
import os

from quiz import Quiz


class QuizGame:
    def __init__(self):
        self.quizzes = []
        self.score = 0
        self.best_score = 0
        self.state_file = "state.json"
        self.load_default_quizzes()
        self.load_data()

    def load_default_quizzes(self):
        self.quizzes = [
            Quiz(
                "구미호라는 별명을 가진 챔피언은?",
                ["아리", "럭스", "애쉬", "징크스"],
                1
            ),
            Quiz(
                "눈먼 수도승이라는 별명을 가진 챔피언은?",
                ["야스오", "리 신", "가렌", "티모"],
                2
            ),
            Quiz(
                "난폭한 말괄량이라는 별명을 가진 챔피언은?",
                ["애쉬", "럭스", "징크스", "아리"],
                3
            ),
            Quiz(
                "데마시아의 힘으로 알려진 챔피언은?",
                ["가렌", "티모", "리 신", "야스오"],
                1
            ),
            Quiz(
                "날쌘 정찰병이라는 별명을 가진 챔피언은?",
                ["럭스", "티모", "아리", "애쉬"],
                2
            )
        ]

    def load_data(self):
        if not os.path.exists(self.state_file):
            print("저장된 데이터가 없습니다. 기본 퀴즈를 사용합니다.")
            return

        try:
            with open(self.state_file, "r", encoding="utf-8") as file:
                data = json.load(file)

            saved_quizzes = data.get("quizzes", [])

            if isinstance(saved_quizzes, list):
                loaded_quizzes = []

                for item in saved_quizzes:
                    loaded_quizzes.append(
                        Quiz(
                            item["question"],
                            item["choices"],
                            item["answer"]
                        )
                    )

                if loaded_quizzes:
                    self.quizzes = loaded_quizzes

            saved_score = data.get("best_score", 0)

            if isinstance(saved_score, int) and saved_score >= 0:
                self.best_score = saved_score
            else:
                self.best_score = 0
            print("저장된 데이터를 불러왔습니다.")

        except (json.JSONDecodeError, KeyError, TypeError, ValueError):
            print("저장 데이터에 문제가 있습니다. 기본 퀴즈를 사용합니다.")

    def save_data(self):
        data = {
            "quizzes": [
                {
                    "question": quiz.question,
                    "choices": quiz.choices,
                    "answer": quiz.answer
                }
                for quiz in self.quizzes
            ],
            "best_score": self.best_score
        }

        try:
            with open(self.state_file, "w", encoding="utf-8") as file:
                json.dump(data, file, ensure_ascii=False, indent=4)

            print("퀴즈 데이터를 저장했습니다.")

        except OSError:
            print("데이터 저장에 실패했습니다.")

    def show_menu(self):
        print("\n===== 롤 캐릭터 맞추기 =====")
        print("1. 퀴즈 플레이")
        print("2. 퀴즈 추가")
        print("3. 퀴즈 목록")
        print("4. 최고 점수 확인")
        print("5. 종료")
    def run(self):
        while True:
            self.show_menu()

            choice = input("메뉴를 선택하세요 (1~5): ").strip()

            if choice == "1":
                self.play_quiz()

            elif choice == "2":
                self.add_quiz()

            elif choice == "3":
                self.list_quizzes()

            elif choice == "4":
                self.show_best_score()

            elif choice == "5":
                print("게임을 종료합니다.")
                break

            else:
                print("1~5 사이의 번호를 입력해 주세요.")
    def add_quiz(self):
        print("\n===== 퀴즈 추가 =====")

        while True:
            question = input("문제를 입력하세요: ").strip()

            if question:
                break

            print("문제는 비워둘 수 없습니다. 다시 입력하세요.")

        choices = []

        for number in range(1, 5):
            while True:
                choice = input(f"{number}번 보기 입력: ").strip()

                if choice:
                    choices.append(choice)
                    break

                print("보기는 비워둘 수 없습니다. 다시 입력하세요.")

        while True:
            answer = input("정답 번호를 입력하세요 (1~4): ").strip()

            if answer.isdigit() and 1 <= int(answer) <= 4:
                answer = int(answer)
                break

            print("1~4 사이의 숫자를 입력하세요.")

        new_quiz = Quiz(question, choices, answer)
        self.quizzes.append(new_quiz)

        self.save_data()
        print("새로운 퀴즈가 추가되었습니다!")

    def list_quizzes(self):
        print("\n===== 퀴즈 목록 =====")

        if not self.quizzes:
            print("등록된 퀴즈가 없습니다.")
            return

        for number, quiz in enumerate(self.quizzes, start=1):
            print(f"\n[{number}] {quiz.question}")

            for choice_number, choice in enumerate(quiz.choices, start=1):
                print(f"  {choice_number}. {choice}")

        print(f"\n총 {len(self.quizzes)}개의 퀴즈가 등록되어 있습니다.")
    def show_best_score(self):
        print(f"현재 최고 점수: {self.best_score}")

    def play_quiz(self):
        if not self.quizzes:
            print("등록된 퀴즈가 없습니다.")
            return

        self.score = 0

        for quiz in self.quizzes:
            quiz.show_question()

            while True:
                answer = input("정답 번호를 입력하세요 (1~4): ").strip()

                if not answer.isdigit():
                    print("숫자를 입력해 주세요.")
                    continue

                answer = int(answer)

                if answer < 1 or answer > 4:
                    print("1~4 사이의 번호를 입력해 주세요.")
                    continue

                break

            if quiz.check_answer(answer):
                print("정답입니다!")
                self.score += 1
            else:
                print(f"오답입니다. 정답은 {quiz.answer}번입니다.")

        print(f"\n최종 점수: {self.score}/{len(self.quizzes)}")

        if self.score > self.best_score:
            self.best_score = self.score
            print("최고 점수를 갱신했습니다!")

        self.save_data()
