import sys
from controllers import Controller


def main():
    sys.stdin = open("input.txt", "r")

    controller = Controller()
    controller.run()


if __name__ == "__main__":
    main()
