# Explanation for Day 17

## Introduction

This puzzle states that a probe will initiate on a starting origin of (0,0), and an initial velocity for both *x* and *y* directions can be defined. The probe will follow the directions in such a manner:

- In the **first step**, the probe will move along the **x axis** in a **positive** direction, in the amount specified by the x velocity.

- In the **first step**, the probe will also move along the **y axis**, where the **direction and the amount** is determined by the y velocity.

- The **x velocity** will decrease by 1.

- The **y velocity** will also decrease by 1.

- The second step will initiate and follow the same steps as above.

However, a limitation exists where **the velocity for x cannot decrease below 0**. The velocity for y has no such limitation. For this reason, the graph below (taken from the  [Advent of Code problem specification](https://adventofcode.com/2021/day/17)) is seen when the initial velocity is (6, 3):

```
target area: x=20..30, y=-10..-5 (labelled as 'T')
S is the starting point (0,0)
# is the location of the probe after each step
...............#..#............
...........#........#..........
...............................
......#..............#.........
...............................
...............................
S....................#.........
...............................
...............................
...............................
.....................#.........
....................TTTTTTTTTTT
....................TTTTTTTTTTT
....................TTTTTTTTTTT
....................TTTTTTTTTTT
....................T#TTTTTTTTT
....................TTTTTTTTTTT
```

## Part 1:

Part 1 asks what the **maximum possible height** is for any trajectory to achieve. In order to do achieve this, it must be recognized that:

- There is a limit to the x velocity, because the x velocity cannot decrease beyond 0. Specifically, this limit is defined as:
  
  - x + (x-1) + (x-2) + ... + 1 + 0
  
  Or alternatively, using the [Gauss Sum](https://en.wikipedia.org/wiki/Gauss_sum)
  
  - (x * (x + 1)) / 2
  
  Therefore, as long as the y velocity hits the target area, the x velocity does not matter. This means that, for part 1, **only the y velocity matters**.

- For the y velocity, it is important to notice that the **same y coordinates that were visited on the upward trajectory will be visited on the downward trajectory**. This can be seen in the graph from the introduction.
  
  This is not a coincidence. Rather, this is the result of the y velocity decreasing by 1 for each step. For example, the y velocity used in the graph (from the introduction section) is 3, indicating that:
  
  - For step 1, y = **3**
  
  - For step 2, y = 3 + (3 - 1) = **5**
  
  - For step 3, y = 5 + (3 - 2) = **6**
  
  - For step 4, y = 6 + (3 - 3) = **6**
  
  - For step 5, y = 6 + (3 - 4) = **5**
  
  - For step 6, y = 6 + (3 - 5) = **3**
  
  This example illustrates that because the height velocity **decreases by 1 indefinitely**, and **because there will always be a step where the height velocity does not increase** (step 4 in this example), the same set of y coordinates will be visited on the upward and downward trajectory.
  
  Therefore, **the maximum height is achieved when the "final step" is equal to the lowest coordinate in the target area**. The "final step" is defined as the downward trajectory step immediately after y = 0 is reached.
  
  Because the height velocity decreases to 0 until its peak (steps 1-3 in the example), the height of the peak is:
  
  - y + (y-1) + ... + 1 + 0
  
  Which is yet another Gauss sum of:
  
  - (y * (y + 1)) / 2

Therefore the answer to part 1 is:

- (a * (a + 1)) / 2
  
  Where a is the absolute value of the minimum y value in the target area, minus 1.

## Part 2:

Part 2 is a brute force approach, but here is how the maximum and minimum limits for the x and y velocities were decided:

- x velocities:
  
  - The maximum velocity is easy. The maximum velocity is the maximum x coordinate of the target area. Any velocity higher than that will overshoot the target area
  
  - As discussed in Part 1, the total distance travelled along the x axis is the Gauss Sum of the initial x velocity. The first integer where the Gauss Sum is greater than the minimum x coordinate of the target area is defined as the minimum x coordinate.

- y velocities:
  
  - The minimum velocity is also easy. The minimum velocity is the minimum y coordinate of the target area (for this number there is no upward trajectory as the minimum y value is negative).
  
  - The maximum velocity is absolute value of the minimum y coordinate in the target area, minus 1. This is because any value higher than this will overshoot the target area on the downward trajectory. Please see the explanation for Part 1 for more details.


