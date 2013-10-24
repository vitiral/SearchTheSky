

import pdb
from cloudtb import logtools
from logging import DEBUG, INFO, ERROR
log = logtools.get_logger(level = DEBUG)

from PyQt4 import QtGui, QtCore
import itertools

from cloudtb import iteration
from cloudtb.extra.pyqt import StdWidget
from cloudtb.extra import richtext

class SearchTheSky_ui(StdWidget):
    _NAME_ = "SearchTheSky"
    def setupUi(self):
        self.setWindowTitle("Search The Sky")
        
        self.std_settings = {
        ('self.geometry', 'self.setGeometry'):(
             [], [QtCore.QRect(10, 10, 600, 600)]),
        }
        self.statusbar = QtGui.QStatusBar(self)
        self.setStatusBar(self.statusbar)
        self.show()
    
    def get_size(self):
        return self.width(), self.height()
    
    def set_size(self, size):
        return self.resize(*size)