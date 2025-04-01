import time

import click

from solver import solve_digits_with_moves 


@click.command()
@click.option(
    "-n", "--numbers", type=str,
    help="Comma-separated list of numbers")
@click.option(
    "-t", "--target", type=int,
    help="target number to be built")
@click.option(
    "-c", "--how_many_solutions", type=int,
    help="The number of solutions the solver should return (None=find all)",
    default=None)
def main(numbers, target, how_many_solutions):
    numbers = [int(number) for number in numbers.split(",")]
    t0 = time.time()
    solutions = solve_digits_with_moves(
        numbers, target, how_many_sols=how_many_solutions)
    t1 = time.time()
    print(
        f"Found {len(solutions)} solution{'' if len(solutions) == 1 else 's'}. Took {round(t1 - t0, 2)} seconds.")
    for sol in solutions:
        for move in sol:
            print(move)
        print("\n")


if __name__ == "__main__":
    main()
