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
rows_in_cols = []
for col in range(0, cols):
    row = np.size(test_real[col])
    rows_in_cols.append(row)
    print(rows_in_cols)
rows_in_cols = np.array(rows_in_cols)
l=1
print(test_real[1:-1*l])
class Panel:
    def __init__(self):
        self.x_length = None
        self.y_length = 0
    
    def size(self, foo):
        self.x_length = len(foo)
        for col in range(0,cols):
            if np.size(foo[col]) > self.y_length:
                self.y_length = np.size(foo[col])

class Button:
    def __init__(self):
        self.x = 0
        self.y = 0
        self.number = None
    
    def coord(self, x_length, y_length, foo):
        self.cols = len(foo)
        self.x_length = x_length
        self.y_length = y_length
        rows_in_cols = []
        for col in range(0, self.cols):
            rows = np.size(test_real[col])
            rows_in_cols.append(row)
            print(rows_in_cols)
        rows_in_cols = np.array(rows_in_cols)
        self.leftcol = rows_in_cols[0]
        self.rightcol = rows_in_cols[-1]
        self.midcol = rows_in_cols[1:-1]
        for col in self.midcol:
            if col > self.leftcol and col > self.rightcol:
                col_norm = foo[-1]

            
panel = Panel()
panelsize = panel.size(test_real)
#print(panel.x_length, panel.y_length)