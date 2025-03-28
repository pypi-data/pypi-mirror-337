from ..basic import subtraction

type Vector = list[float]


def subtract_vec(vec1: Vector, vec2: Vector) -> Vector:
    return [subtraction.subtract(x, y) for x, y in zip(vec1, vec2)]
