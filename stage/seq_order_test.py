#############
# Imports
import numpy as np

#Input: List of collumns of elevator button number labels
#Output: Proposed corrected list of collumns of elevator button number labels
#Description: This script implements a method of reordering evator button labels in accordance to most probable arrangements
#Requisities: all buttons were detected, buttons are ordered from bottom to top
#Notes:
#############
test_real = np.array([[2,5,8,11],[1,3,6,9,12],[4,7,10]])
test = np.array([[2,5,8,11],[3,6,9,12],[4,7,10,13]])
cols = len(test_real)
rows = []
for col in range(0, cols):
    row = np.size(test_real[col])
    rows.append(row)
rows = np.array(rows)
print(rows)

class Template:
    def __init__(self,rows,cols,lenght):
        # Initialize templates
        self.temp_left_right_up = np.array([])
        self.temp_right_left_up = np.array([])
        self.temp_up_left_right = np.array([])
        self.temp_up_right_left = np.array([])
    
    def create(self, foo):
        #cols may not be stable
        self.cols = len(foo)
        self.rows = []
        for col in range(0, cols):
            row = len(test_real[col])
            self.rows.append(row)
        self.vect = np.array(self.rows)