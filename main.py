from quiz_game import QuizGame


def main():
    game = QuizGame()

    try:
        game.run()

    except (KeyboardInterrupt, EOFError):
        print("\n사용자가 프로그램을 종료했습니다.")

    finally:
        game.save_data()
        print("게임을 안전하게 종료합니다.")


if __name__ == "__main__":
    main()