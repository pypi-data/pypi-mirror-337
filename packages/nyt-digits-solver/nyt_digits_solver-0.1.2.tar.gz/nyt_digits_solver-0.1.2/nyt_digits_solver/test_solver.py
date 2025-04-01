import pytest

from .solver import describe_moves, solve_digits


@pytest.mark.parametrize(
    "moves,expected",
    [
        (
            [[1, 1], [2]],
            ["1+1"],
        ),
        (
            [[1, 1], [0]],
            ["1-1"],
        ),
        (
            [[2, 3], [6]],
            ["3*2"],
        ),
        (
            [[6, 2], [3]],
            ["6/2"],
        ),
        (
            [[1, 2, 5], [3, 5], [15]],
            ["2+1", "5*3"],
        ),

    ]
)
def test_moves(
        moves,
        expected,
):
    assert describe_moves(moves) == expected


@pytest.mark.parametrize(
    "numbers,target,solution",
    [
        (
            [1, 1],
            2,
            [[[1, 1], [2]]],
        ),
        (
            [2, 3],
            6,
            [[[2, 3], [6]]],
        ),
        (
            [2, 3],
            1,
            [[[2, 3], [1]]],
        ),
        (
            [3, 9],
            3,
            [[[3, 9], [3]]],
        )
    ]
)
def test_unique_single_steps(
        numbers,
        target,
        solution,
):
    assert solve_digits(numbers, target) == solution


@pytest.mark.parametrize(
    "numbers,target,solution",
    [
        (
            [1, 2, 4],
            12,
            [[[1, 2, 4], [3, 4], [12]]],
        ),
    ]
)
def test_unique_solution_multiple_steps(
        numbers,
        target,
        solution,
):
    assert solve_digits(numbers, target) == solution
