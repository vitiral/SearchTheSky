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
# -*- coding: utf-8 -*-
"""
Created on Mon Nov 18 10:48:57 2013

@author: user
"""

import sys, os
from PyQt4 import QtGui
import shelve

from ui.SearchTheSky_ui import SearchTheSky_ui
import RegExp

from cloudtb import system

SETTINGS_FILE = '.SearchTheSky'
SETTINGS_PATH = os.path.join(system.get_user_directory(), SETTINGS_FILE)

class SearchTheSky(QtGui.QMainWindow, SearchTheSky_ui):
    def __init__(self, debug = False, parent=None):
        super(SearchTheSky, self).__init__(parent)
        self._debug = debug
        self.setupUi()
        self.setupAdditional()
        self.load_settings()
    
    def setupAdditional(self):
        self.Tabs = RegExp.TabCentralWidget(main = self)
        self.setCentralWidget(self.Tabs)
        self.Menu = RegExp.Menu(self.reset_settings, self)
        self.setMenuBar(self.Menu)
        
    def reset_settings(self):
        return self.load_settings({})
        
    def load_settings(self, set_settings = None):
        try:
            if set_settings != None:
                settings = set_settings
            else:
                settings = shelve.open(SETTINGS_PATH)
            SearchTheSky_ui.load_settings(self, settings)
            self.Tabs.load_settings(settings)
#            print "Problem loading settings. Using default. Error:"
#            print errors.get_prev_exception_str()
#            settings = dict()
#            self.Tabs.load_settings(settings)
        finally:
            if type(settings) != dict:
                settings.close()
    
    def save_settings(self):
        sfile = None
        try:
            sfile = shelve.open(SETTINGS_PATH)
            sfile.clear()
            SearchTheSky_ui.save_settings(self, sfile)
            assert(not self.Tabs.save_settings(sfile))
        finally:
            if sfile != None:
                sfile.close()
        
    def closeEvent(self, *args):
        print 'Closing'
        self.save_settings()
        # prevents any kind of dbe type shenanigans to stop us
        def fake_except_hook(*args, **kwargs):
            print 'Exiting Application'
        sys.excepthook = fake_except_hook
        self.close()

def main(debug = False):
    from PyQt4.QtCore import pyqtRemoveInputHook
    pyqtRemoveInputHook
    app = QtGui.QApplication(sys.argv)
    ex = SearchTheSky(debug = debug)
    sys.exit(app.exec_())
    print QtGui.QTextEdit

if __name__ == '__main__':
    main(debug = True)
