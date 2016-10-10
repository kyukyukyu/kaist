# CS548 Advanced Information Security HW 1

KAIST SoC 20163204 남상규 (Sanggyu Nam)

## Problems

1. Write a program which computes XDT for S-boxes of DES.
2. Verify that 1/234 is the best iterative characteristic of DES.

## Results

Here is my solution for problem 1 only. I tried to solve problem 2, but I
couldn't.

I wrote the program mentioned in problem 1 in C. If you are on \*nix
environment, you can build this program just by typing `make` on your shell.
Then a binary file named `xdt` will be created. If you run this binary file,
eight CSV files will be created on this directory whose names are `xdt1.csv`,
`xdt2.csv`, ..., and `xdt8.csv`. Each file contains XDT for each S-box in DES,
where each line represents each row with comma-separated 16 numbers.

For convenience of grading, I created an Excel spreadsheet file named
`xdt.xlsx` which contains these eight tables.
