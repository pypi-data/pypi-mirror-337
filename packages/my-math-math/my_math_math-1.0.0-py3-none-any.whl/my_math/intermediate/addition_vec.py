from ..basic import addition

type Vector = list[float]


def add_vec(vec1: Vector, vec2: Vector) -> Vector:
    return [addition.add(x, y) for x, y in zip(vec1, vec2)]
