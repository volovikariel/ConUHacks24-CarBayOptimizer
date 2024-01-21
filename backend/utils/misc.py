from typing import Protocol, TypeVar


class Comparable(Protocol):
    def __lt__(self, other: "Comparable") -> bool:
        ...


# Now, you can use Comparable as a type hint for function parameters
C = TypeVar("C", bound=Comparable)


def ranges_overlap(range: tuple[C, C], ranges: list[tuple[C, C]]) -> bool:
    start = range[0]
    end = range[1]
    for r in ranges:
        if start < r[1] and end > r[0]:
            return True
    return False


def binarySearch(ranges: list[tuple[C, C]], start_index: int):
    lo = 0
    hi = start_index - 1

    START = 0
    FINISH = 1

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
