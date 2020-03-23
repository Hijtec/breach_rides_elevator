"""TODO:A postprocessing module for button recognition.

#Input:         Raw detections of buttons(array), button width and height(floats)
#Output:        Proposed corrected array of elevator panel(numpy.array)
#Assumptions:   TODO:All numbered buttons were detected(array/list of lists), localized(float) and labeled(int)
                Buttons detection data is ordered from bottom to top (y_min -> y_max)

This script utilises data given from a recognition module and feeds it
for postprocessing in order to correct and enhance the data for further
use. These include:
    assesing columns and rows
    creating callable objects
    finding correct button panel template
    TODO: correct number sequence

  Typical usage example:

  det = Detection(detection_data,button_width,button_height)
  TODO: correctseq()
"""
from math import floor as rounddown

import numpy as np

#TESTDATA
dtype = [('x', float),( 'y', float),( 'n', int)]
data = np.array([(0.625,0.11,1),
                (0.12,0.35,2),(0.39,0.36,3),(0.61,0.38,4),(0.89,0.32,5),
                (0.14,0.53,6),(0.40,0.52,7),(0.62,0.56,8),(0.90,0.58,9),
                (0.11,0.72,10),(0.35,0.71,11),(0.58,0.74,12),(0.82,0.71,13),
                (0.10,0.93,14),(0.37,0.88,15)],
                dtype=dtype)
data_OCR = np.array([(0.625,0.11,1),
                (0.12,0.35,2),(0.39,0.36,3),(0.61,0.38,4),(0.89,0.32,5),
                (0.14,0.53,8),(0.40,0.52,7),(0.62,0.56,8),(0.90,0.58,8),
                (0.11,0.72,1),(0.35,0.71,11),(0.58,0.74,12),(0.82,0.71,13),
                (0.10,0.93,14),(0.37,0.88,15)],
                dtype=dtype)
but_w = 0.2
but_h = 0.18

class Detection:
    """A wrapper class for data input.

    Attributes:
        detected:                   An array of given data from recognition
        buttons:                    List of Button classes based on given data
        panel:                      Panel object
        template:                   Template object
        but:                        List of detected button parameters
        adj_cooef: TODO: A cooeficient for moving the comparison value for imperfect/real positions

    Methods:
        create_buttons:             Creates a list of Button objects
        create_panel:               Creates a slave Panel object
        create_template:            Creates a slave Template object
        find_classes(axis = 1/0):   Finds buttons along the same row/column
        order_unique_coord(coord, history, type = "rows"/"cols"): 
                                    Rearanges rows and columns based on their average position in space
    """

    def __init__(self,detected,but_w,but_h):
        """Initializes the class and calls its methods."""
        self.detected = detected
        self.buttons = None
        self.panel = None
        self.but = (but_w,but_h)
        self.adj_cooef = 1

        self.create_buttons() 
        self.create_panel()
        self.create_template()

    def create_buttons(self):
        """Creates a list of button objects."""
        button_list = []
        for i in self.detected:
            x_raw, y_raw, n_raw = i[0], i[1], i[2]
            button_list.append(Button(x_raw,y_raw,n_raw))
        self.buttons = button_list
    
    def create_panel(self):
        """Creates a panel object with all of its necessities."""
        rows, rows_all, r_val_hist = self.find_classes("row")
        cols, cols_all, c_val_hist = self.find_classes("col")

        if len(rows) > 1/but_h: raise ValueError("There can't be more rows than can physically fit into statespace")
        if len(cols) > 1/but_w: raise ValueError("There can't be more cols than can physically fit into statespace")

        rows_ordered = self.order_unique_coord(rows_all, r_val_hist, "row")
        cols_ordered = self.order_unique_coord(cols_all, c_val_hist, "col")

        self.panel = Panel(self.buttons, rows_ordered, cols_ordered)

    def create_template(self):
        """Creates a template object."""
        self.template = Template(self.panel)

    def find_classes(self,axis):
        """Finds rows/columns in data.

        Args:
            axis:                   String ("row"/"col") that depends upon if we want to find rows or cols

        Returns:
            sames_unique:           Numpy sorted array of unique classes
            sames:                  Numpy array of found classes
            comp_val_history:       List of average values of y_raw (for rows)/ x_raw(for cols) 
                                    for each member, used to differenciate classes
        """
        if axis == "row": 
            axis = 1
        elif axis == "col": 
            axis = 0
        else: 
            raise NameError("argument must be row or col")

        i = -1
        sames = []
        comp_val_history = []

        for _ in self.detected:
            same_class = []
            j = -1

            i +=1
            compare_val = self.detected[i][axis]

            for d in self.detected:
                j +=1
                val = d[axis]
                if abs(val-compare_val) < self.but[axis]/2:
                    same_class.append(j)
                    compare_val = compare_val + (val-compare_val)/self.adj_cooef

            sames.append(same_class)
            comp_val_history.append(rounddown(compare_val*10)) #Important to sorting the columns based on y_axis

        sames = np.array(sames)
        sames_unique = np.unique(sames)

        return sames_unique, sames, comp_val_history

    def order_unique_coord(self,coord,comp_hist,type):
        """Rearanges rows/cols based on their position and eliminates duplicities.

        Args:
            coord:      List of lists of all detected rows/columns
            comp_hist:  List of average values of y_raw (for rows)/ x_raw(for cols)
                        for each member, used to differenciate classes
            type:       str("row"/"col") based on finding order of rows/columns

        Returns:
            out:        Returns the ordered list of rows/cols
    
        Raises:
            TypeError:  When arg type is not either "col" or "row"
        """
        rearranged, out = [], []
        indexing = np.argsort(comp_hist)

        for j in indexing:
            rearranged.append(coord[j])
        _, idx = np.unique(rearranged, return_index=True)

        for j in np.sort(idx):
            out.append(rearranged[j])

        if type == "col":
            self.cols = out
        elif type == "row":
            self.rows = out
        else:
            raise TypeError("Type must be a (row) or (col)")
        
        return out

class Button:
    """A storage class for button instance.

    Attributes:
        x_raw:                  X coordinate from button recognition data
        y_raw:                  Y coordinate from button recognition data
        n_raw:                  Proposed number from button recognition data
        n_miss:                 An attribute indicating whether the button is suspected to be mislabeled
        col:                    Column coordinate/position
        row:                    Row coordinate/position
    """
    def __init__(self,x_raw,y_raw,n_raw):
        """Initializes the class with position parameters."""
        self.x_raw = x_raw
        self.y_raw = y_raw
        self.n_raw = n_raw
        self.n_miss = 0
        self.n_corr = None
        self.col = None
        self.row = None
    
class Panel:
    """A class for assigning buttons coords to a detection instance.

    Attributes:
        buttons:               List of Button instances
        rows:                  List of ordered unique rows
        cols:                  List of ordered unique columns
    """
    def __init__(self,buttons,rows,cols):
        self.buttons = buttons
        self.rows = rows
        self.cols = cols
        #assign rows and cols
        i = 0
        for row in rows:
            i +=1
            for item in row:
                self.buttons[item].row = i
        j = 0
        for col in cols:
            j +=1
            for item in col:
                self.buttons[item].col = j

class Template:
    """A class for assigning a template to detection instance.

    Attributes:
        n_ranks:                    List of ranked template candidates
        priority_lr:                Boolean of left-right sequence priority
        priority_vh:                Boolean of horizontal-vertical sequence priority
        rows:                       List of ordered unique cols inherited from panel instance
        cols:                       List of ordered unique rows inherited from panel instance
        panel:                      Panel inherited instance
    
    Methods:
        find_template_candidate:    Finds ranks of all possible templates and saves them in a list
        assign_template:            Sets priority_XX based on best template candidate, prints info
        count_lr:                   Creates an iterable list through which it computes left-right ranks
        count_vh:                   Creates an iterable list through which it computes horizontal-vertical ranks
        suppress_odd_rows:          Based on average members in row suppresses first row, prints info if it did
        recalculate_cols:           Recalculates the columns based upon the suppressed rows
    """
    def __init__(self,panel):
        self.n_ranks = None
        self.priority_lr = None #True if left->right, false if right->left
        self.priority_vh = None #True if counting by rows, false if counting by columns
        self.rows = panel.rows
        self.cols = panel.cols
        self.panel = panel
        self.find_template_candidate()
        self.assign_template()
    
    def find_template_candidate(self):
        """Ranks the numbering template based upon its correct probability."""
        self.rank_h_lr = self.count_lr("left")
        self.rank_h_rl = self.count_lr("right")
        self.rank_v_lr = self.count_vh("left")
        self.rank_v_rl = self.count_vh("right")
        
        self.n_ranks = [self.rank_h_lr, self.rank_h_rl, self.rank_v_lr, self.rank_v_rl]

    def assign_template(self):
        """Assigns priority_XX to Template object.

        Raises:
            ValueError:  Unexpected input
        """
        minElement = np.argmax(np.array(self.n_ranks)) #gets the index of the best candidate

        if minElement == 0 or minElement == 2:
            self.priority_lr = True
        elif minElement == 1 or minElement == 3:
            self.priority_lr = False
        else:
            raise ValueError("Unexpected input into finding template")

        if minElement == 0 or minElement == 1:
            self.priority_vh = True
        elif minElement == 2 or minElement == 3:
            self.priority_vh = False
        else:
            raise ValueError("Unexpected input into finding template")

        print(f'The values are ordered from left to right: {self.priority_lr} \nThe values are counted by rows: {self.priority_vh}')

    def count_lr(self, order):
        """Creates an iterable list through rows and computes left-right ranks.

        Args:
            order:          str("left"/"right"), test counting from left/right

        Returns:
            n_order:        Rank of the tested sequence
    
        Raises:
            ValueError:     arg(order): Order must be either left or right
        """
        if order == "left":
            axis = 1
        elif order == "right":
            axis = -1
        else:
            raise ValueError("Order must be either left or right")

        #Making an iterable list to count with
        listed_numbers = []
        for row in self.rows:
            for i in row:
                listed_numbers.append(self.panel.buttons[i].n_raw) #get the proposed button number
        
        #Defining starting positions
        if axis == 1:
            curr, foll = 0, 0
        if axis == -1:
            curr, foll = -1, -1
        n_order = 0
        #Iterate through the list
        for _ in range(len(listed_numbers)-1):
            foll += axis

            if listed_numbers[curr] < listed_numbers[foll]:
                n_order += 1
            else:
                n_order += 0
            
            curr = foll

        return n_order #Return order of the sequence
    
    def count_vh(self, order):
        """Creates an iterable list through columns and computes horizontal-vertical ranks.

        Args:
            order:          str("left"/"right"), test counting from left/right

        Returns:
            n_order:        Rank of the tested sequence
    
        Raises:
            ValueError:     arg(order): Order must be either left or right
        """
        if order == "left":
            axis = 1
        elif order == "right":
            axis = -1
        else:
            raise ValueError("Order must be either left or right")
        #Suppression and recalculation of odd data
        rows_suppressed = self.suppress_odd_rows()
        cols_suppressed = self.recalculate_cols(rows_suppressed)
        #Making an iterable list to count with
        listed_numbers = []

        for col in cols_suppressed:
            for i in col:
                listed_numbers.append(self.panel.buttons[i].n_raw) #get the proposed button number

        #Defining starting positions
        if axis == 1:
            curr, foll = 0, 0
        if axis == -1:
            curr, foll = -1,-1
        n_order = 0
        #Iterate through the list
        for _ in range(len(listed_numbers)-1):
            foll += axis
            if listed_numbers[curr] < listed_numbers[foll]:
                n_order += 1
            else:
                n_order += 0
            curr = foll
        
        return n_order #Return order of the sequence
    
    def suppress_odd_rows(self):
        """Suppresses first row of panel for counting rank if the row is smaller than avg of all others.

        Returns:
            suppressed:     List of rows without the potentionally suppressed one
    
        """
        avg_in_row = 0

        for row in self.rows:
            avg_in_row += len(row)

        avg_in_row = avg_in_row/len(self.rows)

        if avg_in_row > len(self.rows[0]): #compare if the first row has less members
            del_index = self.rows[0][:]
            suppressed_rows = np.delete(self.rows, del_index)
            print("First row suppressed for rank count")
        else:
            suppressed_rows = self.rows

        return suppressed_rows

    def recalculate_cols(self,suppressed):
        """Recalculates columns after the potential suppression of first row.

        Args:
            suppressed:                     List of unique rows

        Returns:
            cols_ordered_suppressed:        List of ordered unique columns
        """
        cols_ordered_suppressed = []
        ncols, col = 0, []

        for i in suppressed:
            if len(i) > ncols: 
                ncols = len(i)
        
        for i in range(ncols):
            #TODO:get rid of try
            try:
                col = []
                for item in suppressed:
                    col.append(item[i])
                cols_ordered_suppressed.append(col)
            except:
                cols_ordered_suppressed.append(col)
    
        return cols_ordered_suppressed

#Istance of Detection class
det = Detection(data_OCR,but_w,but_h)
print(det.template.n_ranks,det.template.priority_lr,det.template.priority_vh, det.template.rows, det.template.cols, det.panel.buttons[5].n_raw)