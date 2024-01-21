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
