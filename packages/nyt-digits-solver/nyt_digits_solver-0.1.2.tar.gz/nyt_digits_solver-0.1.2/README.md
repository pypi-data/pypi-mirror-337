# NYT_digits_solver
Puzzle solver algorithm for the popular (former) digits game
https://www.nytimes.com/games/digits (no longer exists).

## Utilization

```
In [1]: import nyt_digits_solver as solver

In [2]: solver.solve_digits([1,2,3], 6)
Out[2]: [[[1, 2, 3], [3, 3], [6]]]

In [3]: solver.solve_digits_with_moves([1,2,3], 6)
Out[3]: [['2+1', '3+3']]
```
