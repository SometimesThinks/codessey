import sys
from app import run


def main():
    # input.txt 파일로 입력 받기(개발용)
    sys.stdin = open("input.txt", "r")
    run()


if __name__ == "__main__":
    main()
