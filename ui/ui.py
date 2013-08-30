"""
ui.py is  used as the starting point for the GIS GUI application. This file will initialize the window, and all the sub structure's
that integrate into the window. It will allow the user to query locations from the db dump of data points, plot on a map from the location
data and other required information.
"""
import sys
from PyQt4 import QtGui
from PyQt4 import uic


class Window(QtGui.QFrame):

    height = 200
    width = 200

    def __init__(self):
        QtGui.QFrame.__init__(self)
        self.frame = uic.loadUi("/Users/brandon/PycharmProjects/gis_project/resources/gis.ui")
        self.frame.show()



def main():
    """
    Pass Main GUI information here
    """
    app = QtGui.QApplication(sys.argv)
    frame = Window()
    sys.exit(app.exec_())





if __name__ == '__main__':
    main()