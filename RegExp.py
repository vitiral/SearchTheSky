
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

from cloudtb import logtools# , dbe
from cloudtb.extra.PyQt import treeview
from logging import DEBUG, INFO, ERROR
log = logtools.get_logger(level = DEBUG)

from cloudtb.extra.pyqt import StdWidget
from cloudtb import textools
from cloudtb.extra import researched_richtext, richtext
        
from ui.RegExp_ui import (ui_RegExp, ui_RexpFiles_Folder, ui_RexpFilesTab, 
    ui_RexpTextTab)

class RegExp(ui_RegExp):
    def __init__(self, parent = None, add_sub_tab = None, sub_tabs = None,
                 parent_layout = None, main = None):
        super(RegExp, self).__init__(parent)
        self._tabs_created = False
        
        self.main = main
        self.parent = parent
        self.parent_layout = parent_layout
        self.add_sub_tab = add_sub_tab
        self.sub_tabs = sub_tabs
        
        if add_sub_tab:
            self.setupTabs()
        else:
            self.setupWidget()
        self.startTimer(200)
    
    def setupAdditional(self):
        self.parent_layout.addWidget(self.Replace_groups)
        
    def save_settings(self, application_settings):
        app_set = application_settings
        assert(not StdWidget.save_settings(self, app_set))
        assert(not self.Folder.save_settings(app_set))
        assert(not self.Replace_groups.save_settings(app_set))
        if self._tabs_created:
            assert(not self.Tab_files.save_settings(app_set))
            assert(not self.Tab_text.save_settings(app_set))
        
    def load_settings(self, application_settings):
        app_set = application_settings
        assert(not StdWidget.load_settings(self, app_set))
        assert(not self.Folder.load_settings(app_set))
        assert(not self.Replace_groups.load_settings(app_set))
        if self._tabs_created:
            assert(not self.Tab_files.load_settings(app_set))
            assert(not self.Tab_text.load_settings(app_set))
        
        self.regexp_edited()
        self.Tab_text.set_update()
    
    def setupTabs(self):
        if self._tabs_created:
            log(INFO, "Tabs attempted to be created a second time")
            return
        self.Tab_files = RexpFilesTab(self.Folder, 
                                      None, # self.get_regexp_folder
                                      self.get_regexp)
        self.Tab_text = RexpTextTab(self.get_regexp, self.get_replace)
        self._tabs_created = True
        self.setupAdditional()
    
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
        self.Ledit_regexp.textEdited.connect(self.regexp_edited)
        self.But_replace.pressed.connect(self.toggle_popgroups)
        # I couldn't find out how to connect to this damn thing, so I made
        # a custom one
        self.Replace_groups_model.dataWasChanged.connect(
            self.Tab_text.set_update)

    def toggle_popgroups(self):
        if self.Replace_groups.isHidden():
            self.Replace_groups.show()
        else:
            self.Replace_groups.hide()
    
        
    def regexp_edited(self):
        regexp = self.get_regexp()
        try:
            re.compile(regexp)
        except Exception as E:
            print "Redited Error:", E 
        else:
            self.Replace_groups_model.set_groups(textools.
                get_regex_groups(regexp))
        self.Tab_text.set_update()
    
    def pre_close(self, *args):
        self.Replace_groups.close()
        
class RexpFiles_Folder(ui_RexpFiles_Folder):
    pass

class RexpFilesTab(ui_RexpFilesTab):
    def __init__(self, Folder, get_regexp_folder, get_regexp_file, 
                 parent = None):
        super(RexpFilesTab, self).__init__(Folder, parent = parent)
        self.get_regexp_folder = get_regexp_folder
        self.get_regexp_file = get_regexp_file
        self._node = None
        self.connect_signals()

    def connect_signals(self):
        self.Folder.But_find.pressed.connect(self.search)    
        
#        QtCore.QObject.connect(self.Tree_model, 
#            QtCore.SIGNAL("itemDoubleClicked(QTreeWidgetItem *,int)"), 
#            self.tree_item_dclicked)
        self.Tree_folder.doubleClicked.connect(self.tree_item_dclicked)
        
        self.Radio_match.toggled.connect(self.update_text)

    def update_text(self):
        node = self._node
        if node == None:
            self.setText('')
            return
            
        if self.Radio_match.isChecked():
            html_list = (researched_richtext.
                re_search_format_html(node.researched,
                    show_replace = False))
        else:
            html_list = (researched_richtext.
                re_search_format_html(node.researched,
                    show_replace = True))
        
        str_html = richtext.get_str_formated_html(html_list)
        self.TextBrowser.setHtml(str_html)

    def tree_item_dclicked(self, *args):
        print 'dclicked'    
        
        index = self.Tree_folder.currentIndex()
        node = index.internalPointer()
        
        self._node = node
        
        print node.name(), ', Repl:', node.do_replace, 
        if node.isdir:
            print ' , isdir'
        else:
            print ' , Re:', node.researched
            # need to load file, regexp, etc
            if node.researched == None:
                with open(node.full_path) as f:
                    text = f.read()
                node.researched = textools.re_search(self.get_regexp_file(),
                    text)
            self.update_text()
        
    def search(self):
        folder = self.Folder.get_folder()
        print 'Searching', folder
        paths = researched_richtext.get_match_paths(folder, 
                                text_regexp = self.get_regexp_file()
#                                file_regexp = self.get_regexp_folder(), 
                                                    )
        self.Tree_model.clear_rows()
        if not paths:
            print 'No File Match Found'
            return
        self.Tree_model.update_files(paths)

class RexpTextTab(ui_RexpTextTab):
    def __init__(self, get_regexp, get_replace, parent = None):
        super(RexpTextTab, self).__init__(parent)
        self.get_regexp = get_regexp
        self.get_replace = get_replace
        
        self._disable_signals = False
        self._cached_deformated = None
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
            if self._cached_deformated == None:
                self._cached_deformated = richtext.deformat_html(raw_html,
                    (richtext.KEEPIF['black-bold'], 
                     richtext.KEEPIF['red-underlined-bold']))
            deformated = self._cached_deformated
                
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
        
    def set_update(self, *args, **kwargs):
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
#            assert(len(deformated_str) <= len(self.getText()))
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
                self.setText(deformated_str)
                self._disable_signals = False                
                return                

            # Set the html to the correct values
            if self.Radio_match.isChecked():
                print 'doing match'
                html_list = rsearch_rtext.re_search_format_html(researched)
            else:
                print 'doing replace'
                rlist = self.get_replace()
                replaced = textools.re_search_replace(researched, 
                    rlist, preview = True)
                print textools.format_re_search(replaced)
                html_list = rsearch_rtext.re_search_format_html(replaced)
            
            raw_html = richtext.get_str_formated_html(
                html_list)
            self.setHtml(raw_html)
            
            visible_pos = richtext.get_position(html_list,
                    true_position = true_pos)[1]
            print 'new visible pos', visible_pos
            self.set_text_cursor_pos(visible_pos)
            
            self._cached_deformated = None
            self._disable_signals = False

#==============================================================================
# Top Level Classes
#==============================================================================
import shelve
import os
from cloudtb import system, errors

SETTINGS_FILE = '.SearchTheSky'
SETTINGS_PATH = os.path.join(system.get_user_directory(), SETTINGS_FILE)

class Menu(QtGui.QMenuBar):
    def __init__(self, reset_settings, parent = None):
        super(Menu, self).__init__(parent)
#        pdb.set_trace()
        self.reset_settings = reset_settings
        
        self.setupUi()
        self.connect_signals()
    
    def connect_signals(self):
        self.connect(self.ResetSettings, QtCore.SIGNAL("triggered()"),
                     self.reload_settings)
    
    def reload_settings(self):
        print "Reloading Settings"
        self.reset_settings()
        
    def setupUi(self):
        self.Options_menu = QtGui.QMenu(self)
        self.Options_menu.setTitle("Options")
#        self.Options.setCheckable(False)
#        self.Options.setChecked(False)
        self.ResetSettings = QtGui.QAction(self)
        self.ResetSettings.setText("Reset Settings")
        
        self.Options_menu.addAction(self.ResetSettings)
        self.addAction(self.Options_menu.menuAction())


class TabCentralWidget(StdWidget):
    _NAME_ = 'TAB_CENTRAL'
    def __init__(self, parent=None, main = None):
        super(TabCentralWidget, self).__init__(parent)
        self.main = main
        self.setupTabWidgets()
        
        self.createTabRegExp()
        self.tab_regexp.activateTabs(self.tabs_lower)
        self.std_settings = {('self.tabs_lower.currentIndex', 
                         'self.tabs_lower.setCurrentIndex'): ([], [0])
                        } 
    
    def load_settings(self, settings):
        StdWidget.load_settings(self, settings)
        assert(not self.tab_regexp.load_settings(settings))
        
    def save_settings(self, settings):
        StdWidget.save_settings(self, settings)
        assert(not self.tab_regexp.save_settings(settings))
    
    def pre_close(self):
        self.tab_regexp.pre_close()
    
    def setupTabWidgets(self):
        # Set all possible upper tabs to None
        self.tab_regexp = None
        
        vbox = QtGui.QVBoxLayout()
        
        tabs_upper = QtGui.QTabWidget()
        tabs_upper.setFixedHeight(90)
        vbox.addWidget(tabs_upper)
        
        splitter_lower = QtGui.QSplitter()
        spolicy = QtGui.QSizePolicy()
        spolicy.setVerticalPolicy(QtGui.QSizePolicy.Expanding)
        spolicy.setHorizontalPolicy(QtGui.QSizePolicy.Expanding)
        splitter_lower.setSizePolicy(spolicy)
        
        tabs_lower =  QtGui.QTabWidget()
        splitter_lower.addWidget(tabs_lower)
        vbox.addWidget(splitter_lower)
        
        self.setLayout(vbox)
        self.splitter_lower = splitter_lower
        self.vbox = vbox
        self.tabs_upper = tabs_upper
        self.tabs_lower = tabs_lower
        
        # TODO: how to hide / remove tabs
        # clear seems to work -- and it forces me to integrate
        # saving settings early on.
    
    def createTabRegExp(self):
        assert(self.tab_regexp == None)
        self.tab_regexp = RegExp(add_sub_tab = self.tabs_lower.addTab,
                                 sub_tabs = self.tabs_lower,
                                 parent_layout = self.splitter_lower,
                                 main = self.main)
        self.tabs_upper.addTab(self.tab_regexp, "Reg Exp")
        self.tab_regexp.setEnabled(True)

from ui.SearchTheSky_ui import SearchTheSky_ui
class SearchTheSky(QtGui.QMainWindow, SearchTheSky_ui):
    def __init__(self, debug = False, parent=None):
        super(SearchTheSky, self).__init__(parent)
        self._debug = debug
        self.setupUi()
        self.setupAdditional()
        self.load_settings()
    
    def setupAdditional(self):
        self.Tabs = TabCentralWidget(main = self)
        self.setCentralWidget(self.Tabs)
        self.Menu = Menu(self.reset_settings, self)
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

    
