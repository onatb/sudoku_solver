# Sudoku solving program

This program is designed to solve evil sudoku puzzles for www.websudoku.com within seconds using IBM CPLEX Optimizer and Selenium WebDriver.

Steps:
1. Program opens Chrome web browser automatically using Selenium WebDriver, loads www.websudoku.com and collects the sudoku data,
2. Creates a linear model with 729 variables and more than 324 constraints
3. Solves this integer programming model using IBM CPLEX solver and 
4. Populates the original sudoku table with the optimal results.

Mathematical model can be found in "Mathematical Model.pdf" file

Video:
[![Watch the video](https://i.imgur.com/WB9X1lU.png)](https://www.dropbox.com/s/1ye39eflesanla8/HOWA8208.MP4?dl=0)
