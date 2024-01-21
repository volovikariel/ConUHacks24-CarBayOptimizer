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


# Returns index of range whose "end"/"finish"
# is before curr_idx; -1 when there is none
def get_nearest_prev_finish_time(ranges: list[tuple[C, C]], curr_idx: int) -> int:
    START = 0
    FINISH = 1
    other_range_idx = curr_idx - 1
    while other_range_idx >= 0:
        if ranges[other_range_idx][FINISH] <= ranges[curr_idx][START]:
            return other_range_idx
        else:
            other_range_idx -= 1
    return -1
