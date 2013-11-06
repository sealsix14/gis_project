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
        self.map = None
        self.data = None
        self.record = None
        self.initUI()

    def initUI(self):

        #self.setToolTip('This is a <b>QWidget</b> widget')
    #Quit Button handler and positioning code below
        quit_btn = QtGui.QPushButton('Quit', self)
        quit_btn.clicked.connect(QtCore.QCoreApplication.instance().quit)
        #quit_btn.setToolTip('This is a <b>QPushButton</b> widget')
        quit_btn.resize(quit_btn.sizeHint())
        quit_btn.move(450, 450)

    #Load file button
        load_btn = QtGui.QPushButton('Load File', self)
        load_btn.resize(load_btn.sizeHint())
        load_btn.move(20,450)
        load_btn.clicked.connect(self.loadFile)

        self.setGeometry(200,200,250,150)
        #self.setWindowTitle('Tooltips')
        self.setWindowTitle('GIS')
        self.show()

    def loadFile(self, sender):
        gis_file = QtGui.QFileDialog()
        fname = gis_file.getOpenFileName(self,'Open File', '.')
        self.data = Dataset()
        self.data.load(fname)
        self.map = DataMap(self.data.data_list)

    def showInputDialog(self):

        text, ok = QtGui.QInputDialog.getText(self, 'Input Dialog',
            'Enter your name:')

        if ok:
            vin = str(text)
            x,y,t = vin.split(" ")
            self.record = Record()
            self.record.x = x
            self.record.y = y
            self.record.t = t

    def IDW_Query(self, record, exp=1, n=1):
        '''
        We will set a record with the inputted data from the GUI.
        We then calculate the neighbors and use this list of neighbors
        in the IDW calculations.
        '''
        neighbors = self.map.get_n_neighbors(record, n)
        #result = idw(r, neighbors, exp)




def main():
    """
    Pass Main GUI information here
    """
    app = QtGui.QApplication(sys.argv)
    frame = Window()
    sys.exit(app.exec_())





if __name__ == '__main__':
    main()