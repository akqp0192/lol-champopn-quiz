# LOL Champion Quiz

리그 오브 레전드(League of Legends) 챔피언의 별명과 특징을 보고 정답을 맞히는 Python 콘솔 퀴즈 게임입니다.

## 프로젝트 목적

Python의 클래스, 반복문, 조건문, 예외 처리와 JSON 파일 입출력을 연습하기 위해 제작했습니다. 사용자가 직접 퀴즈를 추가하고, 프로그램을 다시 실행해도 퀴즈와 최고 점수를 유지할 수 있도록 구현했습니다.

## 개발 환경

- Python 3.12
- Git / GitHub
- JSON
- VS Code

## 주요 기능

1. 퀴즈 플레이: 4개의 보기 중 정답 번호 입력
2. 퀴즈 추가: 문제, 보기 4개, 정답 번호 등록
3. 퀴즈 목록: 등록된 문제와 선택지 확인
4. 최고 점수: 플레이 기록 중 가장 높은 점수 확인
5. 데이터 저장: 퀴즈와 최고 점수를 JSON 파일로 저장
6. 입력 검증: 공백, 문자, 범위를 벗어난 번호에 대한 재입력 처리
7. 오류 복구: JSON 파일이 손상되거나 형식이 잘못된 경우 기본 퀴즈로 복구

## 실행 방법

```bash
python main.py
```

## 테스트 실행

```bash
python -m unittest -v test_quiz
```

문법 검사는 다음과 같이 실행합니다.

```bash
python -m py_compile main.py quiz.py quiz_game.py test_quiz.py
```

## 파일 구조

```text
lol-champopn-quiz/
├── main.py
├── quiz.py
├── quiz_game.py
├── state.json
├── test_quiz.py
├── .gitignore
├── docs/
│   └── images/
│       ├── 01_environment/
│       ├── 02_git_github/
│       ├── 03_quiz_features/
│       ├── 04_json_save/
│       ├── 05_exception_handling/
│       ├── 06_branch_merge/
│       ├── 07_clone_pull/
│       └── 08_final_result/
└── README.md
```

## 데이터 파일 설명

`state.json`은 UTF-8 형식의 JSON 파일입니다.

- `quizzes`: 퀴즈 목록
- `question`: 문제 내용
- `choices`: 네 개의 선택지
- `answer`: 정답 번호(1~4)
- `best_score`: 최고 점수

프로그램을 종료하거나 퀴즈를 추가하면 데이터가 저장되고, 다음 실행 시 저장된 데이터를 불러옵니다.

## Git 개발 과정

- Git 저장소 초기화 및 GitHub 원격 저장소 연결
- 기능 개발을 위한 feature 브랜치 생성
- 퀴즈 기능과 JSON 저장 기능 구현 및 커밋
- feature 브랜치를 main에 병합
- GitHub 저장소를 별도 폴더에 clone
- clone 폴더에서 README를 수정하고 push
- 원본 저장소에서 pull하여 변경 사항 동기화
- 입력 검증, 데이터 검증 및 자동화 테스트 보완

## 설계 및 책임 분리

### 클래스의 역할

- `Quiz` 클래스(`quiz.py`): 퀴즈 한 문제의 데이터인 `question`, `choices`, `answer`를 보관하고, `show_question()`으로 문제와 선택지를 출력하며 `check_answer()`로 정답을 판정합니다.
- `QuizGame` 클래스(`quiz_game.py`): 여러 `Quiz` 객체와 게임 상태(`score`, `best_score`)를 관리합니다. 메뉴 실행, 퀴즈 추가·진행, 입력 검증, 데이터 저장·불러오기를 담당합니다.
- `main.py`: `QuizGame` 객체를 생성하고 실행하며, 예외적인 종료 상황에서도 마지막 저장을 수행합니다.

문제 하나의 정보와 동작은 `Quiz`에 모으고, 여러 문제를 운영하는 흐름은 `QuizGame`에 위임했습니다. 이처럼 객체의 상태와 관련 동작을 함께 관리하면 문제 판정이나 출력 기능을 재사용하기 쉽고, 게임 진행 코드와 문제 데이터 처리 코드를 독립적으로 수정하기 편리합니다. 함수만으로도 구현할 수 있지만, 문제별 상태와 게임 전체 상태가 늘어날수록 관련 데이터와 함수를 별도로 전달·관리해야 하므로 이 프로젝트에서는 클래스로 책임을 묶었습니다.

### 모듈 및 기능별 수정 위치

| 변경하려는 기능 | 수정할 파일 | 주요 클래스·함수 |
|---|---|---|
| 문제 문구·보기·정답 표현 변경 | `quiz.py` | `Quiz.__init__()`, `show_question()`, `check_answer()` |
| 기본 퀴즈 추가·수정 | `quiz_game.py` | `QuizGame.load_default_quizzes()` |
| 메뉴 및 게임 진행 흐름 변경 | `quiz_game.py` | `show_menu()`, `run()`, `play_quiz()` |
| 퀴즈 등록 및 입력 규칙 변경 | `quiz_game.py` | `add_quiz()`, `play_quiz()` |
| 저장 형식·불러오기·복구 변경 | `quiz_game.py` | `save_data()`, `load_data()` |
| 프로그램 시작·종료 처리 변경 | `main.py` | `main()` |
| 기능 회귀 테스트 추가·수정 | `test_quiz.py` | `TestQuiz`, `TestQuizGame` |

입력 검증은 메뉴 선택, 퀴즈 정답 입력, 새 퀴즈 등록처럼 입력을 받는 기능 가까이에서 수행합니다. 데이터 입출력은 `QuizGame.load_data()`와 `QuizGame.save_data()`에 모아 게임 진행 로직이 파일 형식에 직접 의존하지 않도록 구분했습니다.

## 데이터 구조 및 저장 방식 설계

### JSON 필드 설계 이유

- `quizzes`: 여러 문제를 순서대로 보관하는 배열입니다. 문제 수가 늘어나도 동일한 구조의 항목을 반복해 저장할 수 있습니다.
- `question`: 각 문제의 질문 문장을 저장합니다.
- `choices`: 보기 4개를 배열로 저장합니다. 보기의 순서를 유지하고 반복문으로 출력·검증하기 쉽습니다.
- `answer`: 정답 보기의 번호(1~4)를 정수로 저장합니다. 보기 배열의 순번과 대응하므로 별도의 정답 문장을 중복 저장하지 않습니다.
- `best_score`: 최고 점수를 퀴즈 목록과 분리된 최상위 필드로 저장해 점수만 간단히 조회·갱신할 수 있습니다.

JSON은 사람이 읽기 쉬운 텍스트 형식이고 Python의 기본 `json` 모듈로 별도 패키지 없이 처리할 수 있으며, 다른 프로그래밍 언어에서도 널리 지원됩니다. YAML은 주석과 사람이 직접 작성하는 설정 파일에 편리하지만, 이 프로젝트처럼 단순한 객체·배열 데이터를 프로그램에서 반복적으로 읽고 쓰는 경우 JSON의 표준 라이브러리 지원과 구조의 명확성이 적합하다고 판단했습니다.

### JSON 저장 방식의 한계와 복구 정책

현재 프로젝트는 전체 퀴즈 목록과 최고 점수를 `state.json` 파일 하나에 읽고 쓰는 소규모 저장 방식입니다. 데이터가 매우 커지면 파일 전체를 메모리에 읽고 다시 직렬화해야 하므로 저장 시간이 늘고 메모리 사용량도 커질 수 있습니다. 여러 사용자가 동시에 수정하거나 일부 데이터만 자주 변경하는 환경에도 적합하지 않습니다. 데이터 규모와 동시 접근이 커지면 SQLite 같은 데이터베이스를 고려하고, 대용량 순차 처리에는 스트리밍 방식의 처리를 검토할 수 있습니다.

현재 `load_data()`는 파일이 없으면 기본 퀴즈를 사용하고, JSON 파싱 오류·필수 필드 누락·자료형 오류·파일 입출력 오류 등이 발생하면 기본 퀴즈와 최고 점수 0으로 복구합니다. 다만 현재 구현에는 별도 백업 파일을 생성하거나 손상된 이전 데이터를 자동 복원하는 기능은 없습니다. 실제 서비스 수준으로 확장할 경우 저장 전에 기존 파일을 `state.json.bak`으로 보관하고, 임시 파일에 새 데이터를 기록한 뒤 정상 기록이 확인되면 원본과 교체하는 원자적 저장 방식을 도입하는 것이 안전합니다. 복구 순서는 **백업 파일 유효성 검사 → 백업에서 복원 → 백업도 유효하지 않으면 기본 데이터 초기화**로 설계할 수 있습니다.

## Git 브랜치 및 커밋 관리

### 브랜치 분리와 병합 기준

기능 개발은 `main`에 바로 반영하기보다 별도 작업 브랜치(예: `feature/quiz-menu`, `feature/json-save`)에서 진행하면 실험 중인 코드와 안정된 코드를 분리할 수 있고, 기능별 변경 내용을 검토하기 쉽습니다. 기능이 완성되고 기본 실행 및 관련 테스트가 통과한 뒤 `main`에 병합하는 것을 기준으로 합니다. 병합 전에는 변경 파일과 충돌 여부를 확인하고, 병합 후에는 다시 테스트를 실행해 기존 기능이 정상 동작하는지 확인합니다.

### 커밋 메시지 규칙

커밋은 하나의 목적을 가진 작고 검토 가능한 변경 단위로 나눕니다. 예를 들어 메뉴 기능 구현, JSON 저장 기능 구현, 입력 검증 보완, 문서 수정은 각각 별도 커밋으로 기록합니다.

권장 형식은 `<type>: <작업 내용>`입니다.

- `feat: 퀴즈 추가 기능 구현` — 새로운 기능 추가
- `fix: 정답 입력 범위 검증 수정` — 오류 수정
- `test: JSON 복구 테스트 추가` — 테스트 추가·수정
- `docs: README 실행 방법 보완` — 문서 수정
- `refactor: 입력 검증 로직 정리` — 동작 변경 없는 구조 개선

### 커밋 이력 확인

GitHub 저장소의 커밋 이력은 [Commits 페이지](https://github.com/akqp0192/lol-champopn-quiz/commits/main)에서 확인할 수 있습니다. 작업 환경에서는 다음 명령어로 커밋 수와 상세 로그를 확인할 수 있습니다.

```bash
git rev-list --count HEAD
git log --oneline --decorate
git branch -a
```

현재 GitHub의 `main` 브랜치에서 확인되는 커밋은 **16개**입니다. 커밋 이력은 기능 변경과 문서 보완 과정을 추적하기 위한 근거로 활용할 수 있습니다.

## 실행 화면 및 개발 과정 증거

아래는 개발 환경 설정부터 Git 협업 과정, 퀴즈 기능 구현 및 최종 실행까지의 스크린샷입니다.

### 1. 환경 설정

![파이썬 및 Git 버전 확인](docs/images/01_environment/파이썬,깃%20버전확인.png)

![프로젝트 파일 이름](docs/images/01_environment/파일이름.png)

### 2. Git 및 GitHub

![Git 기능 커밋](docs/images/02_git_github/git%20기능%20커밋.png)

### 3. 퀴즈 기능 구현

![Quiz 클래스 정의](docs/images/03_quiz_features/class정의.png)

![퀴즈 기능 1](docs/images/03_quiz_features/퀴즈%20기능1.png)

![퀴즈 기능 2](docs/images/03_quiz_features/퀴즈%20기능2.png)

![퀴즈 기능 3](docs/images/03_quiz_features/퀴즈기능3.png)

![퀴즈 기능 4](docs/images/03_quiz_features/퀴즈%20기능%204.png)

![퀴즈 기능 5](docs/images/03_quiz_features/퀴즈%20기능%205.png)

![퀴즈 게임 클래스](docs/images/03_quiz_features/퀴즈게임%20클래스.png)

### 4. JSON 데이터 저장

![JSON 저장](docs/images/04_json_save/저장.png)

### 5. 예외 처리 및 오류 복구

![예외 처리](docs/images/05_exception_handling/예외처리.png)

![손상된 JSON 오류 복구](docs/images/05_exception_handling/손상된%20JSON오류복구.png)

![잘못된 JSON 복구 화면](docs/images/05_exception_handling/잘못된%20JSON%20복귀화면.png)

### 6. 브랜치 생성 및 병합

![Feature 브랜치 생성](docs/images/06_branch_merge/feature브랜치생성.png)

![브랜치 커밋 및 병합](docs/images/06_branch_merge/브랜치%20커밋,%20브랜치%20병합.png)

![GitHub 병합 결과](docs/images/06_branch_merge/GitHib병합결과.png)

### 7. Clone 및 Pull

![Git Clone](docs/images/07_clone_pull/GitClone.png)

![Git Clone 추가 화면](docs/images/07_clone_pull/GitClone2.png)

![Clone 폴더 수정 및 Push](docs/images/07_clone_pull/Clone에서수정및Push.png)

![Git Pull](docs/images/07_clone_pull/GitPull.png)

### 8. 최종 실행 결과

![퀴즈 플레이](docs/images/08_final_result/1.퀴즈%20플레이.png)

![퀴즈 추가](docs/images/08_final_result/2.퀴즈%20추가.png)

![퀴즈 목록](docs/images/08_final_result/3.퀴즈%20목록.png)

![최고 점수 확인](docs/images/08_final_result/4.최고%20점수%20확인.png)

![종료 및 데이터 저장](docs/images/08_final_result/5.종료%20및%20이전데이터%20저장.png)

## 저장소

https://github.com/akqp0192/lol-champopn-quiz
