from typing import Protocol, TypeVar


class Comparable(Protocol):
    def __lt__(self, other: "Comparable") -> bool:
        ...


# Now, you can use Comparable as a type hint for function parameters
C = TypeVar("C", bound=Comparable)


def ranges_overlap(range: tuple[C, C], ranges: list[tuple[C, C]]) -> bool:
    START = 0
    FINISH = 1
    start = range[START]
    end = range[FINISH]
    for r in ranges:
        if start < r[FINISH] and end > r[START]:
            return True
    return False


def binary_search(ranges: list[tuple[C, C]], start_index: int):
    START = 0
    FINISH = 1

    lo = 0
    hi = start_index - 1

    # TODO: Verify that it's correct...what is this even doing?!
    while lo <= hi:
        mid = (lo + hi) // 2
        if ranges[mid][FINISH] <= ranges[start_index][START]:
            if ranges[mid + 1][FINISH] <= ranges[start_index][START]:
                lo = mid + 1
            else:
                return mid
        else:
            hi = mid - 1
    return -1
