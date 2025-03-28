from enum import Enum, auto


class WorkerRole(Enum):
    HEAD = auto()
    MID = auto()
    TAIL = auto()


if __name__ == "__main__":
    head = WorkerRole.HEAD
    print(head)
