# -*- coding: utf-8 -*-
"""
Created on Wed Oct 18 00:11:16 2017

@author: Onat
"""

import cplex
import numpy as np
from selenium import webdriver

# Step1: Open up web browser and go to www.websudoku.com
driver = webdriver.Chrome('chromedriver')
driver.get('https://nine.websudoku.com/?level=4')

driver.implicitly_wait(10)

"""
driver.switch_to.frame("topwindow")
driver.get('https://www.websudoku.com/?level=4')
"""

# Step2: Get puzzle data from website
table = np.empty((9, 9), int)

for i in range(0, 9):
    for j in range(0, 9):
        cell = 'f' + str(j) + str(i)
        cell_value = driver.find_element_by_id(cell).get_attribute('value')     
        if cell_value == '':
            table[i][j] = 0
        else:
            table[i][j] = cell_value

# Step3: Create the mathematical model using puzzle data         
with open('sudoku_model.lp', 'w') as outfile:
    outfile.write('Minimize\n')
    outfile.write('x001\n')
    outfile.write('Subject To\n')    
    
    # Each cell must only have 1 value
    for i in range(0, 9):
        # If cell has a value, constraint is the value
        for j in range(0, 9):
            if table[i][j] != 0:
                constraint = 'x' + str(i) + str(j) + str(table[i][j]) + ' = 1\n'
                outfile.write(constraint)
            
            else:
                constraint = ''
                for k in range(1, 10):
                    constraint += 'x' + str(i) + str(j) + str(k) + ' + '
                constraint = constraint[:-2] + '= 1\n'
                outfile.write(constraint)
    
    # A number must occur only once in a row            
    for i in range(0, 9):
        for k in range(1, 10):
            constraint = ''
            for j in range(0,9):
                constraint += 'x' + str(i) + str(j) + str(k) + ' + '
            constraint = constraint[:-2] + '= 1\n'
            outfile.write(constraint)
    
    # A number must occur only once in a column         
    for j in range(0, 9):
        for k in range(1, 10):
            constraint = ''
            for i in range(0,9):
                constraint += 'x' + str(i) + str(j) + str(k) + ' + '
            constraint = constraint[:-2] + '= 1\n'
            outfile.write(constraint)
                                
    # A number must occur only once in a 3x3 sub-table
    for m in range(0, 9, 3):
        for n in range(0, 9 , 3):
            for k in range(1,10):
                constraint = ''
                for i in range(m, m + 3):
                    for j in range(n, n + 3):                
                        constraint += 'x' + str(i) + str(j) + str(k) + ' + '
                constraint = constraint[:-2] + '= 1\n'              
                outfile.write(constraint)
    
    # Each variable is binary
    outfile.write('\nBin\n')
    for i in range(0, 9):
        for j in range(0, 9):
            for k in range(1, 10):
                variable = 'x' + str(i) + str(j) + str(k)
                outfile.write(variable + '\n')
    
    # End of model
    outfile.write('\nEnd')

# Step4: Solve the sudoku model using CPLEX optimizer
cpx = cplex.Cplex('sudoku_model.lp')
cpx.solve()

solved_table = np.empty((9, 9), int)
for i in range(0, 9):
        for j in range(0, 9):
            for k in range(1, 10):
                variable = 'x' + str(i) + str(j) + str(k)
                if cpx.solution.get_values(variable) == 1:
                    solved_table[i][j] = k

# Step5: Populate the initial table with solved table
for i in range(0, 9):
        for j in range(0, 9):
            if solved_table[i][j] != table[i][j]:
                cell = 'f' + str(j) + str(i)
                cell_to_populate = driver.find_element_by_id(cell)
                cell_to_populate.send_keys(str(solved_table[i][j]))





