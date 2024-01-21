def ranges_overlap(range: tuple[int, int], ranges: list[tuple[int, int]]) -> bool:
    start = range[0]
    end = range[1]
    for r in ranges:
        if start < r[1] and end > r[0]:
            return True
    return False
