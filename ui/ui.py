"""
ui.py is  used as the starting point for the GIS GUI application. This file will initialize the window, and all the sub structure's
that integrate into the window. It will allow the user to query locations from the db dump of data points, plot on a map from the location
data and other required information.
"""
import sys
from PyQt4 import QtGui
from PyQt4 import uic
from PyQt4 import QtCore
from data.data import Dataset, DataMap, Record


class Window(QtGui.QWidget):

    def __init__(self):
        super(Window, self).__init__()
        self.d_map = None
        self.data = None
        self.record = None
        self.i_vals = []
        self.o_vals = []
        self.initUI()

    def initUI(self):
        self.setFixedHeight(500)
        self.setFixedWidth(700)

    #IDW calculation Button
        IDW_btn = QtGui.QPushButton('Calculate IDW', self)
        IDW_btn.clicked.connect(self.calculate_idw)
        IDW_btn.resize(IDW_btn.sizeHint())
        IDW_btn.move(10,200)
        self.idw_label = QtGui.QLabel(self)
        self.idw_label.move(70,200)
        self.idw_label.setText("")

    #Generate LOOCV Button
        loocv_btn = QtGui.QPushButton('Generate Loocv File', self)
        loocv_btn.clicked.connect(self.generateLoocv)
        loocv_btn.resize(loocv_btn.sizeHint())
        loocv_btn.move(10,300)

    #Quit Button handler and positioning code below
        quit_btn = QtGui.QPushButton('Quit', self)
        quit_btn.clicked.connect(QtCore.QCoreApplication.instance().quit)
        #quit_btn.setToolTip('This is a <b>QPushButton</b> widget')
        quit_btn.resize(quit_btn.sizeHint())
        quit_btn.move(420, 450)

    #Load file button
        load_btn = QtGui.QPushButton('Load File', self)
        load_btn.resize(load_btn.sizeHint())
        load_btn.move(10,450)
        load_btn.clicked.connect(self.loadFile)

    #File loaded label, initialize to ""
        self.file_label = QtGui.QLabel(self)
        self.file_label.setText("No File Loaded")
        self.file_label.move(120,455)

    #query button
        query_btn = QtGui.QPushButton('Interpolate Value ->', self)
        query_btn.resize(query_btn.sizeHint())
        query_btn.move(10,50)
        query_btn.clicked.connect(self.interpolate)
        self.setGeometry(200,200,250,150)
        #self.setWindowTitle('Tooltips')

    #Interpolated Value Label
        self.i_label = QtGui.QLabel(self)
        self.i_label.setText("Interpolated Value: ")
        self.move(10,80)

    #Query Field Input
        self.query_x = QtGui.QLineEdit(self)
        self.query_x.setFixedWidth(50)
        self.query_x.move(260,50)
        x_label = QtGui.QLabel(self)
        x_label.setText("X Value: ")
        x_label.move(200,50)
        self.query_y = QtGui.QLineEdit(self)
        self.query_y.setFixedWidth(50)
        self.query_y.move(380,50)
        y_label = QtGui.QLabel(self)
        y_label.setText("Y Value: ")
        y_label.move(320,50)
        self.query_t = QtGui.QLineEdit(self)
        self.query_t.setFixedWidth(50)
        self.query_t.move(500,50)
        t_label = QtGui.QLabel(self)
        t_label.setText("T Value: ")
        t_label.move(440,50)
        self.query_p = QtGui.QLineEdit(self)
        self.query_p.setFixedWidth(50)
        self.query_p.move(630,50)
        p_label = QtGui.QLabel(self)
        p_label.setText("EXP Value: ")
        p_label.move(560,50)

        #Show the window finally
        self.setWindowTitle('GIS')
        self.show()

    def loadFile(self, sender):
        gis_file = QtGui.QFileDialog()
        fname = gis_file.getOpenFileName(self,'Open File', '.')
        self.data = Dataset()
        self.data.load(fname)
        self.d_map = DataMap(self.data)
        self.file_label.setText("File Loaded!")
        self.o_vals = self.d_map.o_vals

    def showInputDialog(self):

        text, ok = QtGui.QInputDialog.getText(self, 'Input Dialog', 'Enter your data via "x y t":')

        if ok:
            vin = str(text)
            x,y,t = vin.split(" ")
            self.record = Record(x,y,t,self.d_map)
            self.IDW_Query(self.record)

    def interpolate(self):
        nb, ok = QtGui.QInputDialog.getText(self, 'Input Dialog', 'How Many Neighbors do you want to use?:')
        if ok:
            n = int(nb)
        else:
            n = 3
        x = float(self.query_x.text())
        y = float(self.query_y.text())
        t = float(self.query_t.text())
        exp = float(self.query_p.text())
        record = Record(x, y, t, 0.0)
        print record
        i_val = Record.interpolate_value(record.x, record.y, record.t, self.d_map, n, exp)
        print i_val
        self.i_label.setText("Interpolated Value: %f" % i_val)

    def generateLoocv(self):
        Record.generateloocv(self.d_map)

    def IDW_Query(self, record, exp=1, n=1):
        '''
        We will set a record with the inputted data from the GUI.
        We then calculate the neighbors and use this list of neighbors
        in the IDW calculations.
        '''
        result = Record.interpolate_value(record.x, record.y, record.t, self.d_map, n, exp)
        self.query_field.setText(str(result))

    def calculate_idw(self):
        # Calculate IDW and output to an array to store the i_vals, then can use it in the error measurements
        n,ok = QtGui.QInputDialog.getText(self, 'Input Neighbors', 'How Many Neighbors?:')
        if ok:
            neighbors = n
        else:
            neighbors = 3
        exp,ok = QtGui.QInputDialog.getText(self, 'Input Exp', 'What Exponent?:')
        if ok:
            p = exp
        else:
            p = 1
        for i, record in enumerate(self.d_map.records):
            i_val = Record.interpolate_value(record.x, record.y, record.t, record.m, self.d_map, neighbors, p)
            self.i_vals[i] = i_val
        self.idw_label.setText("IDW Calculated!")


def main():
    """
    Pass Main GUI information here
    """
    app = QtGui.QApplication(sys.argv)
    frame = Window()
    sys.exit(app.exec_())





if __name__ == '__main__':
    main()