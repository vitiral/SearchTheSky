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
    
