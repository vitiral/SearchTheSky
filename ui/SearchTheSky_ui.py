#!/usr/bin/python
# -*- coding: utf-8 -*-
#     LICENSE: The GNU Public License v3 or Greater
#
#     Search The Sky (SearchTheSky) v0.0.2
#     Copyright 2013 Garrett Berg
#     
#     This file is part of Search The Sky, a tool that provides powerful code 
#     refactoring in a single tool. This includes:
#       - Interactive regular expression building with file search and replace
#       - (future) integration with python ropetools for python refactoring
#`      - (future) integration with the Java and C tool "cscope" for
#           refactoring in those langages.
#       - (future) other changes -- proposed by you! Suggest them at 
#    
#     You are free to redistribute and/or modify Search The Sky 
#     under the terms of the GNU General Public License (GPL), version 3
#     or (at your option) any later version.
#    
#     You should have received a copy of the GNU General Public
#     License along with Search The Sky.  If you can't find it,
#     see <http://www.gnu.org/licenses/>


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