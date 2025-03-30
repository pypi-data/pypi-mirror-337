from dataclasses import dataclass
from typing import Never

from effect.effect import Effect
from effect.identity import IdentifiedValue
from effect.sugar import Existing, LifeCycle, New, existing, just, mutated, new


@dataclass(kw_only=True, frozen=True, slots=True)
class A(IdentifiedValue[str]):
    id: str
    line: str


@dataclass(kw_only=True, frozen=True, slots=True)
class X(IdentifiedValue[str]):
    id: str
    a: A | None
    number: int


type SomeX = (
    Existing[X]  # No effects / changes
    | New[X]  # Only `New[X]`
    | Effect[X, A, Never, X]  # `New[A]` and `Mutated[X]`
)


def some_x_when(*, x: X | None, number: int) -> SomeX:
    if x is None:
        return new(X(id="X", a=None, number=number))

    if x.a is not None:
        return existing(x)

    a = new(A(id="A", line=str()))
    xx = mutated(X(
        id=x.id,
        number=number,
        a=just(a),
    ))

    return a & xx


def test_some_x() -> None:
    x = X(id="X", number=4, a=None)
    some_x: LifeCycle[X | A] = some_x_when(x=x, number=8)

    assert tuple(some_x.new_values) == (A(id="A", line=""),)
    assert tuple(some_x.mutated_values) == (X(id="X", a=A(id="A", line=""), number=8),)
    assert tuple(some_x.dead_values) == tuple()
