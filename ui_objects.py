
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

from PyQt4 import QtGui, QtCore

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

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
class StdWidget(QtGui.QWidget):
    def __init__(self, parent=None):
        super(StdWidget, self).__init__(parent)

    def save_settings(self, settings):
        return settings[self._NAME_]
    
    def load_settings(self, settings):
        std_settings = self.std_settings
        # remove unrecognized settings
        for n in tuple(settings.keys()):
            if n not in std_settings:
                del settings[n]
            
        # add settings not specified
        for n in std_settings.iterkeys():
            if n not in settings:
                settings[n] = std_settings[n]
        
        # return settings -- to be used in parent
        return settings
    
#==============================================================================
# Regular Expressions
#==============================================================================
class ui_Regexp(StdWidget):
    
    std_settings = {
        'Ledit_regexp.setText': (r'''([a-zA-Z']+\s)+?expect(.*?)(the )*Spanish '''
                        r'''Inquisition(!|.)'''),

        'Ledit_replace.setText': (''' What is this, the Spanish '''
                '''Inquisition? '''),
                
        'Tab_text.TextEdit.setText': (
        '''talking about expecting the Spanish Inquisition in the '''
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
        '''come in again. (Exit and exeunt)\n'''), 
        
        'Folder.Ledit_folder.setText' : None,        # None signifies that something special needs to happen
        'Folder.CBox_recurse.setChecked': True,
        'Folder.Ledit_recurse.setText': '',
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
        Browser_file = QtGui.QTextBrowser()
        
        grip = QtGui.QSizeGrip(Browser_file)
        self.Browser_file = Browser_file
        
        vbox_b_right.addWidget(Browser_file)
        
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
        vbox.addWidget(TextEdit)
        self.TextEdit = TextEdit
        
        self.setLayout(vbox)


#==============================================================================
# Top Level Classes
#==============================================================================
class SearchTheSky(QtGui.QMainWindow):
    def __init__(self, parent=None):
        super(SearchTheSky, self).__init__(parent)
        self.tabs = TabCentralWidget()
        self.setCentralWidget(self.tabs)
        self.resize(450, 400)
        self.show()
        
class TabCentralWidget(QtGui.QWidget):
    def __init__(self, parent=None):
        super(TabCentralWidget, self).__init__(parent)
        self.setupTabWidgets()
        
        self.createTabRegexp()
        self.tab_regexp.activateTabs(self.tabs_lower)
        
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

class RegExp(ui_Regexp):
    _NAME_ = 'REG_EXP'
    def __init__(self, parent = None, add_sub_tab = None):
        ui_Regexp.__init__(self, parent)
        self.parent = parent
        self.add_sub_tab = add_sub_tab
        
        if add_sub_tab:
            self.setupTabs()
        else:
            self.setupWidget()
    
    def load_settings(self, settings):
        settings = ui_Regexp.load_settings(settings)
#        ['Folder.CBox_recurse.setChecked', , 'Folder.Ledit_recurse.setText', 'Tab_text.TextEdit.setText', 'Ledit_regexp.setText', 'Ledit_replace.setText']
    
        for key, item in settings.iteritems():
            if item != None:
                to_exec = 'self.{0}({1})'.format(key, item)
                exec(to_exec)
            elif key == 'Folder.Ledit_folder.setText':
                Folder.Ledit_folder.setText(self.parent.get_home_directory())
            
    def save_settings(self, settings):
        settings = ui_Regexp.load_settings(settings)
    
    def activateTabs(self, tabs_lower):
        '''This gets called when the tab gets activated'''
        if not self._tabs_created:
            self.setupTabs()
            
        self.add_sub_tab(self.Tab_files, "Files")
        self.add_sub_tab(self.Tab_text, "Text")
    

def main():
    app = QtGui.QApplication(sys.argv)
    ex = SearchTheSky()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()

    
