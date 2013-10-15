
#    Special Thanks to the tutorial found at
#    <http://zetcode.com/tutorials/pyqt4/>


'''
Further work requires me to figure out how I am going to handle saving settings.
What I would like is for every object that I need to save settings for just
be a "view" of a dictionary (or something) that I can just pickle. Is this
possible / easy?

'''


import pdb
import sys
import re

from PyQt4 import QtGui, QtCore
import bs4

from cloudtb import logtools, dbe
from logging import DEBUG, INFO, ERROR
log = logtools.get_logger(level = DEBUG)

from cloudtb.extra.pyqt import StdWidget

#==============================================================================
# Standard Object Bases
#==============================================================================

from ui.regexp_ui import (ui_RegExp, ui_RexpFiles_Folder, ui_RexpFilesTab, 
    ui_RexpTextTab)

class RexpFiles_Folder(ui_RexpFiles_Folder):
    _NAME_ = 'REG_EXP_FOLDER'
    pass

class RexpFilesTab(ui_RexpFilesTab):
    _NAME_ = 'REG_EXP_PART_FILES'
    pass

class RexpTextTab(ui_RexpTextTab):
    _NAME_ = 'REG_EXP_PART_TEXT'
    def __init__(self, get_regexp, get_replace, parent = None):
        super(RexpTextTab, self).__init__(parent)
        self.get_regexp = get_regexp
        self.get_replace = get_replace
        
        self._disable_signals = False
        self._update = True
        
        self.connect_signals()
    
    def connect_signals(self):
        self.Radio_match.toggled.connect(self.set_update)
        
        QtCore.QObject.connect(self.TextEdit, 
            QtCore.SIGNAL("cursorPositionChanged()"), self.cursor_changed)
        
        QtCore.QObject.connect(self.TextEdit, 
            QtCore.SIGNAL("textChanged()"), self.set_update)
    
    def cursor_changed(self):
        if not self._disable_signals:
            pass
        
    def set_update(self):
        if not self._disable_signals:
            self._update = True
            
    def check_update(self):
        '''Does the match / replacement and updates the view in real time'''
        from cloudtb import textools
        from cloudtb.extra import researched_richtext, richtext
        
        if self._update:
            self._disable_signals = True
            self.clear_error()
            
            rsearch_rtext = researched_richtext
            self._update = False
            # print 'Updating', time.time()
            qtpos = self.get_text_cursor_pos() # visible pos
            # print 'Got pos', qtpos
            raw_html = self.getHtml()
            # we need to get the "True Position", i.e. the position without
            # our formats added in. I think this is the best way to do it
            deformated = richtext.deformat_html(raw_html,
                (richtext.KEEPIF['black-bold'], 
                 richtext.KEEPIF['red-underlined-bold']))
            deformated_str = richtext.get_str_formated_true(deformated)
            assert(len(deformated_str) <= len(self.getText()))
            true_pos = richtext.get_position(deformated, 
                                visible_position = qtpos)[0]
            # TODO: Bug where if you type immediately after a formatted part
            # it just deletes your text. High Priority. This is my first
            # attempt at fixing
            
                # oK, I can solve the code formating problem simply
# getpos needs to return the index of the last HtmlPart and the
# relative index where pos is.
# Then I just find where the strings differ next(n[0] for n in enumerate(text) if n[1] != text2[n[0]])
# and finally how much (len(text) - len(text2))
# then I go through the parts and replace the true text with the visible text
#            if len(self._true_text) < (deformated_str): # data was added
#                index_dif = next(n[0] for n in enumerate(deformated_str) 
#                    if n[1] != self._prev_visible[n[0]])
#                pos_tup, obj_tup = richtext.get_position(deformated, 
#                                visible_position = index_dif,
#                                return_list_index = True)
#                true_text = richtext.get_true_text(deformated, )
#                true_pos = poses[0]; del poses
#                hlist_index, rel_pos = obj_tuple; del obj_tuple
            
            
            regexp = self.get_regexp()
            error = None
            # These slow it down alot and are not really useful. Just
            # display an error
            if regexp == '.':
                error = "'.' -- Matches everything, not displayed"
            elif regexp == '\w':
                error = "'\w' -- Matches all characters, not displayed"
            elif regexp == '':
                error = ("'' -- Results not displayed, matches between every"
                            " character.")
            else:
                try:
                    researched = textools.re_search(
                        regexp, deformated_str)
                    if len(researched) == 1 and type(researched[0]) == str:
                        error = "No Match Found" 
                except re.sre_compile.error as E:
                    error = str(E)
            if error:
                print error
                self.set_error(error)
                # believe it or not, setText will add formating!           
                # have to explicitly set html
                plain_text_html = richtext.get_str_plain_html(deformated_str)
                self.setHtml(plain_text_html)
                self._disable_signals = False                
                return                

            # Set the html to the correct values
            if self.Radio_match.isChecked():
                print 'doing match'
                html_list = rsearch_rtext.re_search_format_html(researched)
            else:
                print 'doing replace'
                replaced = textools.re_search_replace(researched, 
                    self.get_replace(), preview = True)
                html_list = rsearch_rtext.re_search_format_html(replaced)
            
            raw_html = richtext.get_str_formated_html(
                html_list)
            self.setHtml(raw_html)
            
            visible_pos = richtext.get_position(html_list,
                    text_position = true_pos)[1]
            print 'new visible pos', visible_pos
            self.set_text_cursor_pos(visible_pos)
            
            self._disable_signals = False

#==============================================================================
# Top Level Classes
#==============================================================================
class SearchTheSky(QtGui.QMainWindow):
    def __init__(self, parent=None):
        super(SearchTheSky, self).__init__(parent)
        self.Tabs = TabCentralWidget()
        self.setCentralWidget(self.Tabs)
        self.resize(450, 400)
        self.show()
        
        self.load_settings()
    
    def load_settings(self):
        settings = {}
        self.Tabs.load_settings(settings)
        
class TabCentralWidget(QtGui.QWidget):
    def __init__(self, parent=None):
        super(TabCentralWidget, self).__init__(parent)
        self.setupTabWidgets()
        
        self.createTabRegExp()
        self.tab_regexp.activateTabs(self.tabs_lower)
    
    def load_settings(self, settings):
        assert(not self.tab_regexp.load_settings(settings))
        
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
    
    def createTabRegExp(self):
        assert(self.tab_regexp == None)
        self.tab_regexp = RegExp(add_sub_tab = self.tabs_lower.addTab)
        self.tabs_upper.addTab(self.tab_regexp, "Reg Exp")
        self.tab_regexp.setEnabled(True)

import time

class RegExp(ui_RegExp):
    _NAME_ = 'REG_EXP'
    def __init__(self, parent = None, add_sub_tab = None):
        super(RegExp, self).__init__(parent)
        self._tabs_created = False
        
        self.parent = parent
        self.add_sub_tab = add_sub_tab
        
        if add_sub_tab:
            self.setupTabs()
        else:
            self.setupWidget()
        self.startTimer(200)
    
    def save_settings(self):
        StdWidget.save_settings(self)
        if self._tabs_created:
            self.Tab_files.save_settings()
            self.Tab_text.save_settings()
        
    def load_settings(self, application_settings):
        app_set = application_settings
        StdWidget.load_settings(self, app_set)
        if self._tabs_created:
            self.Tab_files.load_settings(app_set)
            self.Tab_text.load_settings(app_set)
    
    def setupTabs(self):
        if self._tabs_created:
            log(INFO, "Tabs attempted to be created a second time")
            return
        self.Tab_files = RexpFilesTab(self.Folder)
        self.Tab_text = RexpTextTab(self.get_regexp, self.get_replace)
        self._tabs_created = True
    
    def timerEvent(self, ev):
        self.Tab_text.check_update()
    
    def activateTabs(self, tabs_lower):
        '''This gets called when the tab gets activated'''
        if not self._tabs_created:
            self.setupTabs()
            
        self.add_sub_tab(self.Tab_text, "Text")
        self.add_sub_tab(self.Tab_files, "Files")
        
        self.setup_signals()
    
    def setup_signals(self):
        self.Ledit_regexp.textEdited.connect(self.Tab_text.set_update)
        self.Ledit_replace.textEdited.connect(self.Tab_text.set_update)
            
def main():
    app = QtGui.QApplication(sys.argv)
    ex = SearchTheSky()
    sys.exit(app.exec_())
    print QtGui.QTextEdit

if __name__ == '__main__':
    main()

    
