import time
import typing
from collections import deque


def generate_next_moves(
        move: typing.List[int]) -> typing.List[int]:
     for i in range(len(move)):
        for j in range(i + 1, len(move)):
            remainders = [
                move[k] for k in range(len(move)) if k not in [i, j]
            ]
            operations = {
                "+": lambda x, y: x + y,
                "-": lambda x, y: abs(x - y),
                "*": lambda x, y: x * y,
            }
            if move[j] != 0 and move[i] % move[j] == 0:
                operations["/"] = lambda x, y: x // y
            if move[i] != 0 and move[j] % move[i] == 0:
                operations["/"] = lambda x, y: y // x
            for op_sym, op in operations.items():
                next_move_candidate = sorted(
                    remainders + [op(move[i], move[j])])
                op_description = (
                    f"{max(move[i], move[j])}"
                    f"{op_sym}"
                    f"{min(move[i], move[j])}"
                )

                yield next_move_candidate, op_description


def describe_moves(moves: typing.List[typing.List[int]]) -> typing.List[str]:
    descriptions = []
    for move, next_move in zip(moves, moves[1:]):
        for next_move_candidate, op_descr in generate_next_moves(move):
            if next_move_candidate == next_move:
                descriptions.append(op_descr)
                break
    return descriptions


def solve_digits(
        numbers: typing.List[int],
        target: int,
        how_many_sols=1) -> typing.List:
    numbers.sort()

    todo = deque([[numbers]])
    solutions = []
    while todo:
        act = todo.popleft()
        tip = act[-1]
        for new_tip, _ in generate_next_moves(tip):
            if len(new_tip) > 1:
                new_act = act[::]
                new_act.append(new_tip)
                todo.append(new_act)
            elif new_tip[0] == target:
                new_sol_candidate = act + [new_tip]
                if new_sol_candidate not in solutions:
                    solutions.append(new_sol_candidate)
                    if how_many_sols and len(solutions) >= how_many_sols:
                        return solutions
    return solutions


def solve_digits_with_moves(numbers: typing.List[int],
                            target: int,
                            how_many_sols=1) -> typing.List:
    return [
        describe_moves(solution)
        for solution in solve_digits(numbers, target, how_many_sols)
    ]

