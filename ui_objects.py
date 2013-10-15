
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
log = logtools.setup_logger(level = DEBUG)

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

# settings are stored in a dictionary named std_settings, they are 
#  {'Get Setting Exec ({n})', 'Set Setting Exec({n})') : 
#         ('GetInput', 'SetInput')}
#  Where {0} should be formatted with the value given by the settings dict
#  A default setting == None indicates that something special has to be
#  done
#   Everything put into settings MUST BE PICKLEABLE
#   Also keep in mind that everything has to be it's representation, as
#   Readable by a python interpreter. So SetInput should not be "hello world"
#   but rather '"hello world"' or repr("hello world")

class StdWidget(QtGui.QWidget):
    def __init__(self, parent=None):
        super(StdWidget, self).__init__(parent)

    def save_settings(self):
        '''returns the name and current settings dict to be saved
        by the application
        
        This function is to-be extended by the parent class. It returns
        a dict of settings that have been gotten and a dict of
        settings that still need to be gotten.
        
        All upper level functions should return the same thing -- the highest
        level function does error checking by ensuring that bool(need_settings)
            == False
        '''
        return_settings = {}
        need_settings = {}
        # save settings that can be proccessed.
        for key, value in self.std_settings.iteritems():
            getexec, setexec = key
            getval, setval = value
            if getval == None:
                need_settings[getexec] = getval
            else:
                return_settings[getexec] = eval(getexec.format('self'))
        return return_settings, need_settings
        
    def load_settings(self, application_settings):
        '''Load settings given the previous settings from the 
        application settings
        
        Returns the settings that still need to be loaded. All
        implementations of this function should do the same (for error
            checking at top level)
        '''
        try:
            settings = application_settings[self._NAME_]
        except KeyError:
            settings = self.std_settings
        std_settings = self.std_settings
        # remove unrecognized settings
        for key in tuple(settings.keys()):
            if key not in std_settings:
                del settings[key]
            
        # add settings not specified
        for key in std_settings.iterkeys():
            if key not in settings:
                settings[key] = std_settings[key]
        
        need_settings = {}
        # process settings that can be processed+?expect(.*?)(t+?expect(.*?)(t
        for key, item in settings.iteritems():
            getexec, setexec = key
            getval, setval = item

            if setval == None:
                need_settings[setexec] = setval
            else:
                try:
                    exec(setexec.format(n=setval))
                except SyntaxError as E:
                    error = ("Syntax Error in loading: ", 
                        setexec.format(n=setval))
                    log(ERROR, error)
                    raise E
            
        # return settings that still need to be loaded in -- 
        #  to be used in parent
        return need_settings
    
    
    
#==============================================================================
# Regular Expressions
#==============================================================================

class ui_Regexp(StdWidget):
    std_settings = {
        ('str(self.Ledit_regexp.text())' , 'self.Ledit_regexp.setText({n})'):(
             '', repr(r'''([a-zA-Z']+\s)+?expect(.*?)(the )*Spanish '''
                        r'''Inquisition(!|.)''')),
        
        ('str(self.Ledit_replace.text())', 
             'self.Ledit_replace.setText({n})') : (
             '', repr(''' What is this, the Spanish Inquisition? ''')),
        
        ('str(self.Tab_text.getText())',
            'self.Tab_text.setText({n})') : ('', 
        repr('''talking about expecting the Spanish Inquisition in the '''
        '''text below:\n''' 
        '''Chapman: I didn't expect a kind of Spanish Inquisition.\n''' 
        '''(JARRING CHORD - the cardinals burst in) \n'''
        '''Ximinez: NOBODY expects the Spanish Inquisition! Our chief '''
        '''weapon is surprise...surprise and fear...fear and surprise.... '''
        '''Our two weapons are fear and surprise...and ruthless '''
        '''efficiency.... Our *three* weapons are fear, surprise, and '''
        '''ruthless efficiency...and an almost fanatical devotion to the '''
        '''Pope.... Our *four*...no... *Amongst* our weapons.... Amongst '''
        '''our weaponry... are such elements as fear, surprise.... I'll '''
        '''come in again. (Exit and exeunt)\n''')), 
        
        ('str(self.Folder.Ledit_folder.text())', 
            'self.Folder.Ledit_folder.setText({n})') : (repr(''), repr('')),        
        
        ('self.Folder.CBox_recurse.isChecked()', 
            'self.Folder.CBox_recurse.setChecked({n})' ): (repr(''), True),
        
        ('self.Folder.Ledit_recurse.text()',
            'self.Folder.Ledit_recurse.setText({n})') : (repr(''), repr('')),
        
        ('self.Tab_text.Radio_match.isChecked()',
            'self.Tab_text.Radio_match.setChecked({n})') : (repr(''), True),
        
        ('self.Tab_files.Radio_match.isChecked()',
            'self.Tab_files.Radio_match.setChecked({n})') : (repr(''), True),       
    }
    
    def __init__(self, parent=None, add_sub_tab = None):
        super(ui_Regexp, self).__init__(parent)
        self._tabs_created = False
        self.add_sub_tab = add_sub_tab
        self.setupUi()
    
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
        self._vbox = vbox
        
        # Folder is left floating to be in either the main Widget
        # or a sub tab
        self.Folder = ui_RexpFiles_Folder()
    
    def setupWidget(self):
        self._vbox.addWidget(self.Folder)
    
    def setupTabs(self):
        self.Tab_files = ui_RexpFilesTab(self.Folder)
        self.Tab_text = ui_RexpTextTab()
        self._tabs_created = True

class ui_RexpFiles_Folder(QtGui.QWidget):
    def __init__(self, parent=None):
        super(ui_RexpFiles_Folder, self).__init__(parent)
        self.setupUi()
    
    def setupUi(self):
        h_box = QtGui.QHBoxLayout()

        But_folder = QtGui.QToolButton()
        But_folder.setText('  ...  ')
        h_box.addWidget(But_folder)
        self.But_folder = But_folder
        
        Ledit_folder = QtGui.QLineEdit()
        h_box.addWidget(Ledit_folder)
        self.Ledit_folder = Ledit_folder

        But_find = QtGui.QPushButton(" Find ")
        But_find.setToolTip("Search Folder for Regular Expression")
        h_box.addWidget(But_find)
        self.But_find = But_find
        
        CBox_recurse = QtGui.QCheckBox("Recursive")
        CBox_recurse.setToolTip("Look through folders recursively")
        h_box.addWidget(CBox_recurse)
        self.CBox_recurse = CBox_recurse        

        Ledit_recurse = QtGui.QLineEdit()
        Ledit_recurse.setToolTip("Depth of Recursion")
        width = 50
        Ledit_recurse.setMaximumWidth(width)
        Ledit_recurse.setMinimumWidth(width)
        h_box.addWidget(Ledit_recurse)
        self.Ledit_recurse = Ledit_recurse
        
        self.setLayout(h_box)
        
class ui_RexpFilesTab(QtGui.QWidget):
    def __init__(self, Folder, parent=None, create_child_tab = None):
        super(ui_RexpFilesTab, self).__init__(parent)
        self.Folder = Folder
        self.setupUi()
    
    def setupUi(self):
        vbox_main = QtGui.QVBoxLayout()
        
        # # # Folder Line
        vbox_main.addWidget(self.Folder)
        
        # TODO: Want to be able to have user change sizes of the left/right
        
        # # # Bottom
        hbox_bottom = QtGui.QHBoxLayout()
        
        Tree_folder = QtGui.QTreeView()
        grip = QtGui.QSizeGrip(Tree_folder)
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
        TextBrowser = QtGui.QTextBrowser()
        
        grip = QtGui.QSizeGrip(TextBrowser)
        self.TextBrowser = TextBrowser
        
        vbox_b_right.addWidget(TextBrowser)
        
        hbox_bottom.addLayout(vbox_b_right)
        
        # Finally, add hbox
        vbox_main.addLayout(hbox_bottom)
        
        self.setLayout(vbox_main)

class ui_RexpTextTab(QtGui.QWidget):
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
        TextEdit.setAcceptRichText(False)
        TextEdit.setAutoFormatting(QtGui.QTextEdit.AutoNone)
        
        vbox.addWidget(TextEdit)
        self.TextEdit = TextEdit
        
        self.setLayout(vbox)
    
    # text cursor functions
    def get_text_cursor(self):
        return self.TextEdit.textCursor()

    def set_text_cursor_pos(self, value):
        tc = self.get_text_cursor()
        tc.setPosition(value)
        self.TextEdit.setTextCursor(tc)
        
    def get_text_cursor_pos(self):
        return self.get_text_cursor().position()
        
    def get_text_selection(self):
        
        cursor = self.get_text_cursor()
        return cursor.selectionStart(), cursor.selectionEnd()
    
    # Reading text functions
    def getText(self):
        return str(self.TextEdit.toPlainText())
    def getHtml(self):
        return str(self.TextEdit.toHtml())
    
    # seting text functions
    def setHtml(self, html):
        self.TextEdit.setHtml(html)
    def setText(self, text):
        self.TextEdit.setText(text)


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
        
        self.createTabRegexp()
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
    
    def createTabRegexp(self):
        assert(self.tab_regexp == None)
        self.tab_regexp = RegExp(add_sub_tab = self.tabs_lower.addTab)
        self.tabs_upper.addTab(self.tab_regexp, "Reg Exp")
        self.tab_regexp.setEnabled(True)

import time

class RegExp(ui_Regexp):
    _NAME_ = 'REG_EXP'
    def __init__(self, parent = None, add_sub_tab = None):
        ui_Regexp.__init__(self, parent)
        self.parent = parent
        self.add_sub_tab = add_sub_tab
        
        self._disable_signals = False
        self._upate = True
        
        if add_sub_tab:
            self.setupTabs()
        else:
            self.setupWidget()
        self.startTimer(200)
    
    def timerEvent(self, ev):
        self.check_update()
    
    def activateTabs(self, tabs_lower):
        '''This gets called when the tab gets activated'''
        if not self._tabs_created:
            self.setupTabs()
            
        self.add_sub_tab(self.Tab_text, "Text")
        self.add_sub_tab(self.Tab_files, "Files")
        
        self.setup_signals()
    
    def set_update(self):
        if not self._disable_signals:
            self._update = True
    
    def cursor_changed(self):
        if not self._disable_signals:
            pass
        
    def setup_signals(self):
        self.Ledit_regexp.textEdited.connect(self.set_update)
        self.Ledit_replace.textEdited.connect(self.set_update)
        # only need one radio match, we only have one
        self.Tab_text.Radio_match.toggled.connect(self.set_update)
        
        QtCore.QObject.connect(self.Tab_text.TextEdit, 
            QtCore.SIGNAL("cursorPositionChanged()"), self.cursor_changed)
        
        QtCore.QObject.connect(self.Tab_text.TextEdit, 
            QtCore.SIGNAL("textChanged()"), self.set_update)

    def check_update(self):
        '''Does the match / replacement and updates the view in real time'''
        from cloudtb import textools
        from cloudtb.extra import researched_richtext, richtext
        
        if self._update:
            self._disable_signals = True
            rsearch_rtext = researched_richtext
            self._update = False
            # print 'Updating', time.time()
            qtpos = self.Tab_text.get_text_cursor_pos() # visible pos
            # print 'Got pos', qtpos
            raw_html = self.Tab_text.getHtml()
            # we need to get the "True Position", i.e. the position without
            # our formats added in. I think this is the best way to do it
            deformated = richtext.deformat_html(raw_html,
                (richtext.KEEPIF['black-bold'], 
                 richtext.KEEPIF['red-underlined-bold']))
            deformated_str = richtext.get_str_formated_true(deformated)
            assert(len(deformated_str) <= len(self.Tab_text.getText()))
            ot = self.Tab_text.getText()
            nt = deformated_str
#            if len(deformated_str) < len(self.Tab_text.getText()):
#                pdb.set_trace()
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
            
            
            regexp = str(self.Ledit_regexp.text())
            error = None
            # These slow it down alot and are not really useful. Just
            # display an error
            if regexp == '.':
                error = "'.' -- Matches everything, not displayed"
            elif regexp == '\w':
                error = "'\w' -- Matches all characters, not displayed"
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
                # believe it or not, setText will add formating!           
                # have to explicitly set html
                plain_text_html = richtext.get_str_plain_html(deformated_str)
                self.Tab_text.setHtml(plain_text_html)
                self._disable_signals = False                
                return                

            # Set the html to the correct values
            if self.Tab_text.Radio_match.isChecked():
                print 'doing match'
                html_list = rsearch_rtext.re_search_format_html(researched)
            else:
                print 'doing replace'
                replaced = textools.re_search_replace(researched, 
                    str(self.Ledit_replace.text()), preview = True)
                html_list = rsearch_rtext.re_search_format_html(replaced)
            
            raw_html = richtext.get_str_formated_html(
                html_list)
            self.Tab_text.setHtml(raw_html)
            
            visible_pos = richtext.get_position(html_list,
                    text_position = true_pos)[1]
            print 'new visible pos', visible_pos
            self.Tab_text.set_text_cursor_pos(visible_pos)
            
            self._disable_signals = False
        
def main():
    app = QtGui.QApplication(sys.argv)
    ex = SearchTheSky()
    sys.exit(app.exec_())
    print QtGui.QTextEdit

if __name__ == '__main__':
    main()

    
