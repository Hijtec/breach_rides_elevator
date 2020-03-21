#############
#Imports
import numpy as np
from math import floor as rounddown
#Input: Raw detections of buttons, button width and height
#Output: Proposed corrected numpy array of elevator panel
#Description: 
#Requisities: all labeled buttons were detected, buttons are ordered from bottom to top
#Notes:
#############
dtype = [('x', float),( 'y', float),( 'n', int)]
data = np.array([(0.625,0.11,1),
                (0.12,0.35,2),(0.39,0.36,3),(0.61,0.38,4),(0.89,0.32,5),
                (0.14,0.53,8),(0.40,0.52,7),(0.62,0.56,8),(0.90,0.58,9),
                (0.11,0.72,10),(0.35,0.71,11),(0.58,0.74,12),(0.82,0.71,13),
                (0.10,0.93,14),(0.37,0.88,15)],
                dtype=dtype)
but_w = 0.25
but_h = 0.2

class Detection:
    def __init__(self,detected,but_w,but_h):
        self.detected = detected
        self.buttons = []
        self.but = (but_w,but_h)
        self.max_rows = rounddown(1/but_h)
        self.max_cols = rounddown(1/but_w)
        self.adj_cooef = 1
    def create_button(self,detected):
        for i in detected:
            x_raw = i[0]
            y_raw = i[1]
            n_raw = i[2]
            self.buttons.append(Button(x_raw,y_raw,n_raw))
        return self.buttons
    """
    def create_dividers(self):
        #obsolete
        div_x = []
        div_y = []
        for i in range(0,self.max_rows):
            div_y.append(self.but[1]*i + self.but[1]/2)
        for i in range(0,self.max_cols):
            div_x.append(self.but[0]*i + self.but[0]/2)
        return (div_x, div_y)
    """
    def find_classes(self,axis):
        if axis == "row":
            axis = 1
        elif axis == "col":
            axis = 0
        else:
            raise NameError("argument must be row or col")

        i = -1
        sames = []
        comp_val_history = []
        for c in data:
            i +=1
            compare_val = data[i][axis]
            same_class = []
            j = -1
            for d in data:
                j +=1
                val = d[axis]
                if abs(val-compare_val) < self.but[axis]/2:
                    same_class.append(j)
                    compare_val = compare_val + (val-compare_val)/self.adj_cooef
            sames.append(same_class)
            comp_val_history.append(rounddown(compare_val*10))
        sames = np.array(sames)
        sames_unique = np.unique(sames)
        return sames_unique, sames, comp_val_history

    def order_unique_coord(self,coord,comp_hist,type):
        rearranged = []
        out = []
        indexing = np.argsort(comp_hist)
        for j in indexing:
            rearranged.append(coord[j])
        _, idx = np.unique(rearranged, return_index=True)
        for j in np.sort(idx):
            out.append(rearranged[j])
        if type == "cols":
            self.cols = out
        elif type == "rows":
            self.rows = out
        else:
            raise NameError("type must be a (rows) or (cols)")
        return out

class Button:
    def __init__(self,x_raw,y_raw,n_raw):
        self.x_raw = x_raw
        self.y_raw = y_raw
        self.n_raw = n_raw
        self.n_mis = 0
        self.n_corr = None
        self.col = None
        self.row = None
    
class Panel:
    def __init__(self,buttons,rows,cols):
        self.buttons = buttons
        #assign rows and cols
        i = 0
        for row in rows:
            i +=1
            for item in row:
                buttons[item].row = i
        j = 0
        for col in cols:
            j +=1
            for item in col:
                buttons[item].col = j
            
#Istance of Detection class
det = Detection(data,but_w,but_h)
#Its functions
rows, rows_all,r_val_hist = det.find_classes("row")
cols, cols_all,c_val_hist = det.find_classes("col")
cols_ordered = det.order_unique_coord(cols_all,c_val_hist,"cols")
rows_ordered = det.order_unique_coord(rows_all,r_val_hist,"rows")
print(rows_ordered, cols_ordered)

buttons = det.create_button(data) #Create an instance of buttons (calls Button class ->)
panel = Panel(buttons,rows_ordered,cols_ordered)  #Create an instance of panel (gives Buttons rows and columns)