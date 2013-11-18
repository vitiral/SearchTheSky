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
import sys, os

from PyQt4 import QtGui, QtCore, uic
#import popups

def format_line():
    pass

class CheckboxListModel(QtCore.QAbstractListModel):
    def __init__(self, items, checked = None, parent = None):
        QtCore.QAbstractListModel.__init__(self, parent = parent)
        self.items = items
        if checked == None:
            checked = [0] * len(items)
        self.checked = checked
    
    def rowCount(self, parent):
        return len(self.items)
    
    def flags(self, index):
        BASE = (# QtCore.Qt.ItemIsEditable | 
            QtCore.Qt.ItemIsEnabled | 
            QtCore.Qt.ItemIsSelectable|
            QtCore.Qt.ItemIsUserCheckable)
        return BASE

    def data(self, index, role):
        row, column = index.row(), index.column()
        if role == QtCore.Qt.ToolTipRole:
            # give tool tip for what line it is on.
            pass
        
        if role == QtCore.Qt.CheckStateRole:
            value = self.checked[row]
            if value:
                return QtCore.QVariant(QtCore.Qt.Checked)
            else:
                return QtCore.QVariant(QtCore.Qt.Unchecked)
        
        if role == QtCore.Qt.DisplayRole:
            value = self.items[row]
            return format_line(value.regpart)

    def setData(self, index, value, role = QtCore.Qt.EditRole):
        row, column = index.row(), index.column()
        if role == QtCore.Qt.EditRole:
            pass
        
        if role == QtCore.Qt.CheckStateRole:
            self.checked[row] = value.toBool()
            return True
        return False

def dev1():
    pass

if __name__ == '__main__':
    dev1()
    
