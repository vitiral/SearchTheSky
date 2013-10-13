# -*- coding: utf-8 -*-
"""
Created on Sat Oct 12 19:02:08 2013

@author: user
"""
import pdb
import sys

# TODO: how do you resize stuff?

from PyQt4 import QtGui, QtCore

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class ui_SearchTheSky(QtGui.QMainWindow):
    def __init__(self, parent=None):
        super(ui_SearchTheSky, self).__init__(parent)
        self.ui = ui_CentralWidget()
        self.setCentralWidget(self.ui)
        self.resize(450, 400)
        self.show()
        
class ui_CentralWidget(QtGui.QWidget):
    def __init__(self, parent=None):
        super(ui_CentralWidget, self).__init__(parent)
        self.setupTabWidgets()
        
        self.createTabRegexp()
        
        self.tab_regexp.activate(self.tabs_lower)
        
    def setupTabWidgets(self):
        # Set all possible upper tabs to None
        self.tab_regexp = None
        tabs_upper = QtGui.QTabWidget()
        tabs_lower =  QtGui.QTabWidget()
        tabs_upper.setFixedHeight(90)
        
        vbox = QtGui.QVBoxLayout()
        vbox.addWidget(tabs_upper)
        vbox.addWidget(tabs_lower)
        
        self.setLayout(vbox)
        self._layout = vbox
        self.tabs_upper = tabs_upper
        self.tabs_lower = tabs_lower
        
        # TODO: how to hide / remove tabs
        # clear seems to work -- and it forces me to integrate
        # saving settings early on.
        
    def createTabRegexp(self):
        assert(self.tab_regexp == None)
        self.tab_regexp = ui_RegexpTab()
        self.tabs_upper.addTab(self.tab_regexp, "Reg Exp")
        self.tab_regexp.setEnabled(True)


#==============================================================================
# Constructor Functions
#==============================================================================
def get_match_replace_radiobox(parent):
    Radio_match = QtGui.QRadioButton("Match", parent)
    Radio_match.setToolTip("Display Match Results")
    Radio_replace = QtGui.QRadioButton("Replace", parent)
    Radio_match.setToolTip("Display Replace Results")
    radio_box_layout = QtGui.QHBoxLayout()
    radio_box_layout.addWidget(Radio_match)
    radio_box_layout.addWidget(Radio_replace)
    return radio_box_layout, Radio_match, Radio_replace


#==============================================================================
# Standard Object Bases
#==============================================================================
class ui_StdTab(QtGui.QWidget):
    def __init__(self, parent=None):
        super(ui_StdTab, self).__init__(parent)

    def save_settings(self):
        print type(self), ': No save settings routine'
    
    def load_settings(self):
        print type(self), ': No load settings routine'
    
    
#==============================================================================
# Regular Expression Tab
#==============================================================================
class ui_RegexpTab(ui_StdTab):
    def __init__(self, parent=None):
        super(ui_RegexpTab, self).__init__(parent)
        self.setupUi()
        self._tabs_created = False
    
    def setupUi(self):
        vbox = QtGui.QVBoxLayout()
        
        hbox_top = QtGui.QHBoxLayout()
        label_regexp = QtGui.QLabel("Reg Exp")
        Ledit_regexp = QtGui.QLineEdit()
        hbox_top.addWidget(label_regexp)
        hbox_top.addWidget(Ledit_regexp)
        self.Ledit_regexp = Ledit_regexp
        vbox.addLayout(hbox_top)
        
        hbox_bot = QtGui.QHBoxLayout()
        label_replace = QtGui.QLabel("Replace")
        Ledit_replace = QtGui.QLineEdit()
        hbox_bot.addWidget(label_replace)
        hbox_bot.addWidget(Ledit_replace)
        self.Ledit_replace = Ledit_replace
        vbox.addLayout(hbox_bot)
        
        self.setLayout(vbox)
    
    def createTabs(self):
        self.Tab_files = ui_RexpFilesTab()
        self.Tab_text = ui_RexpTextTab()
        self._tabs_created = True
    
    def activate(self, tabs_lower):
        '''This gets called when the tab gets activated'''
        if not self._tabs_created:
            self.createTabs()
            
        tabs_lower = tabs_lower
        tabs_lower.addTab(self.Tab_files, "Files")
        tabs_lower.addTab(self.Tab_text, "Text")
        
class ui_RexpFilesTab(ui_StdTab):
    def __init__(self, parent=None):
        super(ui_RexpFilesTab, self).__init__(parent)
        self.setupUi()
    
    def setupUi(self):
        vbox_main = QtGui.QVBoxLayout()
        
        # # # Folder Line
        hbox_folder = QtGui.QHBoxLayout()

        But_folder = QtGui.QToolButton()
        But_folder.setText('  ...  ')
        hbox_folder.addWidget(But_folder)
        self.But_folder = But_folder
        
        Ledit_folder = QtGui.QLineEdit()
        hbox_folder.addWidget(Ledit_folder)
        self.Ledit_folder = Ledit_folder

        But_find = QtGui.QPushButton(" Find ")
        But_find.setToolTip("Search Folder for Regular Expression")
        hbox_folder.addWidget(But_find)
        self.But_find = But_find
        
        CBox_recurse = QtGui.QCheckBox("Recursive")
        CBox_recurse.setToolTip("Look through folders recursively")
        hbox_folder.addWidget(CBox_recurse)
        self.CBox_recurse = CBox_recurse        
        
        Ledit_recurse = QtGui.QLineEdit()
        Ledit_recurse.setToolTip("Depth of Recursion")
        width = 50
        Ledit_recurse.setMaximumWidth(width)
        Ledit_recurse.setMinimumWidth(width)
        hbox_folder.addWidget(Ledit_recurse)
        self.Ledit_recurse = Ledit_recurse
        vbox_main.addLayout(hbox_folder)
        # TODO: Want to be able to have user change sizes of the left/right
        
        # # # Bottom
        hbox_bottom = QtGui.QHBoxLayout()
        
        Tree_folder = QtGui.QTreeView()
        hbox_bottom.addWidget(Tree_folder)
        self.Tree_folder = Tree_folder
        
        # # Bottom right
        vbox_b_right = QtGui.QVBoxLayout()
        # Top
        hbox_b_right_top = QtGui.QHBoxLayout()
        But_replace = QtGui.QPushButton("  Replace  ")
        But_replace.setToolTip("Perform Replacement")
        hbox_b_right_top.addWidget(But_replace)
        self.But_replace = But_replace
        
        hbox_b_right_top.addSpacing(25)   
        hbox_b_right_top.addStretch(1)
        
        radio_box_layout, self.Radio_match, self.Radio_replace = (
            get_match_replace_radiobox(self))
        hbox_b_right_top.addLayout(radio_box_layout)
        
        vbox_b_right.addLayout(hbox_b_right_top)
        
        # Bottom
        Browser_file = QtGui.QTextBrowser()
        self.Browser_file = Browser_file
        
        vbox_b_right.addWidget(Browser_file)
        
        hbox_bottom.addLayout(vbox_b_right)
        
        # Finally, add hbox
        vbox_main.addLayout(hbox_bottom)
        
        self.setLayout(vbox_main)

class ui_RexpTextTab(ui_StdTab):
    def __init__(self, parent=None):
        super(ui_RexpTextTab, self).__init__(parent)
        self.setupUi()
    
    def setupUi(self):
        vbox = QtGui.QVBoxLayout()
        
        hbox_top = QtGui.QHBoxLayout()
        rbox_layout, self.Radio_match, self.Radio_replace = (
            get_match_replace_radiobox(self))
        hbox_top.addLayout(rbox_layout)
        hbox_top.addStretch(1)
        But_copy = QtGui.QPushButton("  Copy  ")
        But_copy.setToolTip("Copy Results to Paste Buffer")
        hbox_top.addWidget(But_copy)
        self.But_copy = But_copy
        
        vbox.addLayout(hbox_top)
        
        TextEdit = QtGui.QTextEdit()
        vbox.addWidget(TextEdit)
        self.TextEdit = TextEdit
        
        self.setLayout(vbox)
def main():
    app = QtGui.QApplication(sys.argv)
    ex = ui_SearchTheSky()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()

    
