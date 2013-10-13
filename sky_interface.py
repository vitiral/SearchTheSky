
'''
Features:
    - Highlights matches as light green
    - colorizes and numbers matches like kiki
    - Automatically updates text view as you write the re (greys out if no match)
    - Replacements turn the re into a light red background and then add a bold, red ->
        which points to the replacement in light yellow.
    - Helper tab which helps construct the regular expressions 
    - Uses file-system's indexing to get help on where to look first.
    
'''

from __future__ import division

import pdb
import sys, os
import time

from PyQt4 import QtGui, QtCore
from PyQt4.QtCore import pyqtRemoveInputHook

import sky_ui

from cloudtb import textools
from cloudtb.extra import researched_richtext as rsearch_rtext
from cloudtb import dbe

class SearchTheSky(QtGui.QMainWindow):
    def __init__(self, parent=None):
        super(SearchTheSky, self).__init__()
#        QtGui.QWidget.__init__(self, parent)
        self.setup()
    
    def setup(self):
        self.user_interface = UserInterface(self)
        self.startTimer(100)
    
    def timerEvent(self, ev):
        self.user_interface.TextBoxes.check_update()

class UserInterface(object):
    def __init__(self, main):
        self.main = main
        self.setup()
    
    def setup(self):
        self.setup_ui()
        self.Menus = Menus(self)
        self.CheckBoxes = CheckBoxes(self)
        self.Buttons = Buttons(self)
        self.LineEdits = LineEdits(self)
        self.TextBoxes = TextBoxes(self)
        self.setup_signals()
        
    def setup_ui(self):
        self.ui = sky_ui.Ui_SearchTheSky_window()
        self.ui.setupUi(self.main)
        ui = self.ui
        cu = ui.textEdit_input.textCursor()
        QtGui.QTextCursor()
        QtGui.QTextCursor.SelectionType()
    
        self.main.setWindowTitle("Search The Sky")
        self.ui.tabWidget_lower.setCurrentIndex(1)
    
    def setup_signals(self):
        self.ui.lineEdit_input.textEdited.connect(
            self.LineEdits.input_changed)
        self.ui.lineEdit_replace.textEdited.connect(
            self.LineEdits.replace_changed)
        QtCore.QObject.connect(self.ui.textEdit_input, 
            QtCore.SIGNAL("selectionChanged()"), 
            self.TextBoxes.input_selectionChanged)
        self.ui.textEdit_input.connect(self.ui.textEdit_input, 
            QtCore.SIGNAL("textChanged()"), self.TextBoxes.set_update)
    
class Menus(object):
    def __init__(self, user):
        self.u = user
        self.ui = user.ui
        self.connect_menus()
    
    def connect_menus(self):
        ## SPECIAL ## 
#        self.u.connect(self.ui.menu_quick_search, QtCore.SIGNAL("triggered()"),
#                     self.quick_search)
        pass

def connect_button(button, function):
        QtCore.QObject.connect(button, 
               QtCore.SIGNAL("clicked()"),
               function)

class CheckBoxes(object):
    def __init__(self, user):
        self.u = user
        self.ui = user.ui
    
    def get_text_match(self):
        return self.ui.radioButton_text_match.isEnabled()
    
    def get_text_replace(self):
        return self.ui.radioButton_text_replace.isEnabled()
    
    def get_files_match(self):
        return self.ui.radioButton_files_match.isEnabled()
    
    def get_files_replace(self):
        return self.ui.radioButton_files_replace.isEnabled()
    
class Buttons(object):
    def __init__(self, user):
        self.u = user
        self.ui = user.ui
        self.connect_buttons()
    
    def connect_buttons(self):
        pass

class LineEdits(object):
    def __init__(self, user):
        self.u = user
        self.ui = user.ui
        
    def input_changed(self):
        self.u.TextBoxes.update = True
    
    def replace_changed(self):
        self.u.TextBoxes.update = True
    
    def get_input_text(self):
        return str(self.ui.lineEdit_input.text())
    
    def get_replace_text(self):
        return str(self.ui.lineEdit_replace.text())

class TextBoxes(object):
    UPDATE_PERIOD = 0.6
    ''''
    'selectedText'
    'selectedText', 'select', 'selectedTableCells', 'selectedText', 'selection', 'selectionEnd',
    'selectionStart', 'setBlockCharFormat', 'setBlockFormat', 'setCharFormat', 
    'setKeepPositionOnInsert', 'setPosition','''
    def __init__(self, user):
        self.u = user
        self.ui = user.ui
        
        self.text_input = self.ui.textEdit_input
        self.text_files = self.ui.textBrowser_files
        self.input_original = '''Monty Python skit talking about expecting the Spanish Inquisition in the text below: 
Chapman: I didn't expect a kind of Spanish Inquisition. 
(JARRING CHORD - the cardinals burst in) 
Ximinez: NOBODY expects the Spanish Inquisition! Our chief weapon is surprise...surprise and fear...fear and surprise.... Our two weapons are fear and surprise...and ruthless efficiency.... Our *three* weapons are fear, surprise, and ruthless efficiency...and an almost fanatical devotion to the Pope.... Our *four*...no... *Amongst* our weapons.... Amongst our weaponry...are such elements as fear, surprise.... I'll come in again. (Exit and exeunt) 
'''
        self.html_list = None
        self.last_update = 0
        self.update = True  # flag used to determine if update is necessary
        self.check_update()
    
    def check_update(self):
        '''Does the match / replacement and updates the view in real time'''
        if None: #self.update:
            self.update = False
            print 'Updating', time.time()
            if time.time() - self.last_update > self.UPDATE_PERIOD:
                cpos = self.get_text_cursor_pos()   # html position
                checkbox_match = self.u.CheckBoxes.get_text_match()
                researched = textools.re_search(self.u.LineEdits.get_input_text(),
                                                self.input_original)
                if checkbox_match:
                    html_list = rsearch_rtext.re_search_format_html(researched)
                else:
                    html_list = rsearch_rtext.re_search_format_html(
                        textools.re_search_replace(researched, 
                        self.u.LineEdits.get_replace_text, 
                        preview = True))
                self.set_html_input(rsearch_rtext.
                    str_html_formatted(html_list))
                if self.html_list:
                    # note self.html_list is previous list
                    cpos = rsearch_rtext.get_position(self.html_list,
                            html_position = cpos)
                    self.set_text_cursor_pos(rsearch_rtext.get_position(
                        text_position = cpos))
                self.html_list = html_list
        self.last_update = time.time()
        
    
    # text cursor functions
    def get_text_cursor(self):
        return self.text_input.textCursor()
    def set_text_cursor_pos(self, value):
        return self.text_input.textCursor.setPosition(value)
    def get_text_cursor_pos(self):
        return self.get_text_cursor().position()
    def get_text_selection(self):
        cursor = self.get_text_cursor()
        return cursor.selectionStart(), cursor.selectionEnd()
    
    # Reading text functions
    def get_text_input(self):
        return str(self.ui.textEdit_input.toPlainText())
    
    # seting text functions
    def set_html_input(self, html):
        self.ui.textEdit_input.setHtml(html)
    def set_plain_input(self, text):
        self.ui.textEdit_input.setText(text)
    
    # signals
    def set_update(self):
        print 'cursor at', self.get_text_cursor_pos()
        self.update = True
    def input_selectionChanged(self):
        print 'cursor at', self.get_text_cursor_pos()
    def input_textChanged(self):
        print 'edited', time.time()
        self.update = True
    
    def event(self, *args, **kwargs):
        pdb.set_trace()

if __name__ == "__main__":
    pyqtRemoveInputHook()
    print 'Starting...'
    app = QtGui.QApplication(sys.argv)
    myapp = SearchTheSky()
    myapp.show()
    sys.exit(app.exec_())
