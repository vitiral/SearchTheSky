
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
import time

from PyQt4 import QtGui, QtCore
import bs4

from cloudtb import logtools, dbe
from logging import DEBUG, INFO, ERROR
log = logtools.get_logger(level = DEBUG)

from cloudtb.extra.pyqt import StdWidget
from cloudtb import textools
from cloudtb.extra import researched_richtext, richtext
        
from ui.RegExp_ui import (ui_RegExp, ui_RexpFiles_Folder, ui_RexpFilesTab, 
    ui_RexpTextTab)


class RegExp(ui_RegExp):
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
    
    def save_settings(self, application_settings):
        app_set = application_settings
        assert(not StdWidget.save_settings(self, app_set))
        if self._tabs_created:
            assert(not self.Tab_files.save_settings(app_set))
            assert(not self.Tab_text.save_settings(app_set))
        
    def load_settings(self, application_settings):
        app_set = application_settings
        assert(not StdWidget.load_settings(self, app_set))
        if self._tabs_created:
            assert(not self.Tab_files.load_settings(app_set))
            assert(not self.Tab_text.load_settings(app_set))
    
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

class RexpFiles_Folder(ui_RexpFiles_Folder):
    pass

class RexpFilesTab(ui_RexpFilesTab):
    pass

class RexpTextTab(ui_RexpTextTab):
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
            self._disable_signals = True
            self._prev_cursor = self.get_text_cursor_pos()
            # if you are at the right redge of a formatted section, 
            # move to the left. If you are at the left edge, move
            # to the right + 1
            qtpos = self.get_text_cursor_pos() # visible pos
            # print 'Got pos', qtpos
            raw_html = self.getHtml()
            deformated = richtext.deformat_html(raw_html,
                (richtext.KEEPIF['black-bold'], 
                 richtext.KEEPIF['red-underlined-bold']))
            poses, obj_poses = richtext.get_position(deformated, 
                                visible_position = qtpos, 
                                return_list_index = True)
            true_pos, vis_pos, html_pos = poses
            index, rel_vis_pos = obj_poses
            
            hpart = deformated[index]
            if index > 0:
                prev_hpart = deformated[index - 1]
            else:
                prev_hpart = hpart
            vis_text = hpart.visible_text
            true_text = hpart.true_text
            set_true = None
            set_visible = None
            no_change = False
            visible_add = 0
            if len(true_text) == 0:
                # we might be on the inside of formatting
                # Check what the text is before it.
                if qtpos != 0:
                    poses, obj_poses = richtext.get_position(deformated, 
                                visible_position = qtpos - 1, 
                                return_list_index = True)
                else:
                    no_change = True
                if deformated[obj_poses[0]].true_text or qtpos == 0:
                    print 'left side'
                    # the value before is actual text
                    no_change = True
                else:
                    print 'inside'
                    # the value before is formatting, move
                    set_true = true_pos + 1
            elif rel_vis_pos == 0:
                print 'right side'
                # We are on the right side of formatting
                if true_pos != 0:
                    set_true = true_pos - 1
                    visible_add = 1
                else:
                    set_visible = true_pos
            else:
                print 'cursor fine'
                no_change = True
            print no_change, visible_add, set_true
            if set_visible != None: # override for only at 0
                self.set_text_cursor_pos(set_visible)
            elif not no_change:
                set_visible = richtext.get_position(deformated,
                        true_position = set_true)[1] + visible_add
                if set_visible == qtpos - 1:
                    # kind of a hack through trial and error. Not totally
                    # at first I thought it should just be == qtpos...
                    set_visible += 1
                self.set_text_cursor_pos(set_visible)
            self._disable_signals = False
        
    def set_update(self):
        if not self._disable_signals:
            self._update = True
            
    def check_update(self):
        '''Does the match / replacement and updates the view in real time'''
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
                    true_position = true_pos)[1]
            print 'new visible pos', visible_pos
            self.set_text_cursor_pos(visible_pos)
            
            self._disable_signals = False

#==============================================================================
# Top Level Classes
#==============================================================================
import shelve
import os
from cloudtb import system, errors

SETTINGS_FILE = '.SearchTheSky'
SETTINGS_PATH = os.path.join(system.get_user_directory(), SETTINGS_FILE)

class SearchTheSky(QtGui.QMainWindow):
    def __init__(self, parent=None):
        super(SearchTheSky, self).__init__(parent)
        self.Tabs = TabCentralWidget()
        self.setCentralWidget(self.Tabs)
        self.resize(450, 400)
        self.show()
        
        self.load_settings()
    
    def load_settings(self):
        try:
            settings = shelve.open(SETTINGS_PATH)
            self.Tabs.load_settings(settings)
        except Exception as E:
            print "Problem loading settings. Using default. Error:"
            print errors.get_prev_exception_str()
            settings = dict()
            self.Tabs.load_settings(settings)
        finally:
            if type(settings) != dict:
                settings.close()
    
    def save_settings(self):
        settings = {}
        assert(not self.Tabs.save_settings(settings))
        
        try:
            sfile = shelve.open(SETTINGS_PATH)
        except Exception:
            print "Could not save settings Error:"
            print errors.get_prev_exception_str()
        
        try:
            sfile.update(settings)
        finally:
            sfile.close()
        
    def closeEvent(self, *args):
        print 'Closing'
        self.save_settings()
        # prevents any kind of dbe type shenanigans to stop us
        def fake_except_hook(*args, **kwargs):
            print 'Exiting Application'
        sys.excepthook = fake_except_hook
        self.close()
        
class TabCentralWidget(QtGui.QWidget):
    def __init__(self, parent=None):
        super(TabCentralWidget, self).__init__(parent)
        self.setupTabWidgets()
        
        self.createTabRegExp()
        self.tab_regexp.activateTabs(self.tabs_lower)
    
    def load_settings(self, settings):
        assert(not self.tab_regexp.load_settings(settings))
        
    def save_settings(self, settings):
        assert(not self.tab_regexp.save_settings(settings))
    
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


def main():
    from PyQt4.QtCore import pyqtRemoveInputHook
    pyqtRemoveInputHook
    app = QtGui.QApplication(sys.argv)
    ex = SearchTheSky()
    sys.exit(app.exec_())
    print QtGui.QTextEdit

if __name__ == '__main__':
    main()

    
