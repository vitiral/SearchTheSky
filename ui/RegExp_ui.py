
from cloudtb import logtools
from logging import DEBUG, INFO, ERROR
log = logtools.get_logger(level = DEBUG)

from PyQt4 import QtGui
from cloudtb.extra.pyqt import StdWidget
from cloudtb.extra import richtext

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
# Regular Expressions ui classes
#==============================================================================
EMPTY_STR = repr('')
class ui_RegExp(StdWidget):
    _NAME_ = 'REG_EXP'
    
    def __init__(self, parent=None, add_sub_tab = None):
        super(ui_RegExp, self).__init__(parent)
        self.setupUi()
        self.std_settings = {
        ('self.settings_ledit_regexp_text', 'self.Ledit_regexp.setText'):(
             [], [r'''([a-zA-Z']+\s)+?expect(.*?)(the )*Spanish '''
                        r'''Inquisition(!|.)''']),
        
        ('self.settings_ledit_replace_text', 
             'self.Ledit_replace.setText') : (
             [], [''' What is this, the Spanish Inquisition? ''']),
        
        }
    
    def settings_ledit_regexp_text(self):
        return str(self.Ledit_regexp.text())
    
    def settings_ledit_replace_text(self):
        return str(self.Ledit_replace.text())
        
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
    
    def get_regexp(self):
        return str(self.Ledit_regexp.text())
    
    def get_replace(self):
        return str(self.Ledit_replace.text())
    
class ui_RexpFiles_Folder(StdWidget):
    _NAME_ = 'REG_EXP_FOLDER'
    
    def __init__(self, parent=None):
        super(ui_RexpFiles_Folder, self).__init__(parent)
        self.setupUi()
        self.std_settings = {
        ('self.settings_ledit_folder_text', 
         'self.Ledit_folder.setText') : ([], ['']),        
        
        ('self.CBox_recurse.isChecked', 
            'self.CBox_recurse.setChecked' ): ([], [True]),
        
        ('self.settings_ledit_recurse_text',
             'self.Ledit_recurse.setText') : ([], ['']),
        }
        self.setup_signals()
    
    def settings_ledit_folder_text(self):
        return str(self.Ledit_folder.text())
    
    def settings_ledit_recurse_text(self):
        return str(self.Ledit_recurse.text())
    
    def setup_signals(self):
        self.But_folder.pressed.connect(self.select_folder)
    
    def select_folder(self):
        folder = QtGui.QFileDialog.getExistingDirectory(self,
          "Select Directory", self.get_folder())
        if not folder.isEmpty():
            self.Ledit_folder.setText(folder)
            
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
    
    def get_folder(self):
        return str(self.Ledit_folder.text())
        
class ui_RexpFilesTab(StdWidget):
    _NAME_ = 'REG_EXP_PART_FILES'
    def __init__(self, Folder, parent=None, create_child_tab = None):
        super(ui_RexpFilesTab, self).__init__(parent)
        self.Folder = Folder
        self.setupUi()
        self.std_settings = {
        ('self.Radio_match.isChecked',
            'self.Radio_match.setChecked' ): ([], [True]),
        }
        self.setup_signals()
    
    def setup_signals(self):
        self.Folder.But_find.pressed.connect(self.search)
    
    def search(self):
        folder = self.Folder.get_folder()
        print 'Searching', folder
    
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
        self.root_node = treeview.Node("Rootdir")
        self.Tree_model = treeview.TableViewModel(self.root_node)
        Tree_folder.setModel(self.Tree_model)         
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
    
class ui_RexpTextTab(StdWidget):
    _NAME_ = 'REG_EXP_PART_TEXT'

    def __init__(self, parent=None):
        super(ui_RexpTextTab, self).__init__(parent)
        self.std_settings = {
        ('self.getDeformated', 'self.setText') : ([],[
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
        '''come in again. (Exit and exeunt)\n''']), 
        
        ('self.Radio_match.isChecked',
            'self.Radio_match.setChecked') : ([], [True]),
        }
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

        Label_error = QtGui.QLabel()
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setItalic(True)
        font.setWeight(75)
        Label_error.setFont(font)
        Label_error.setWordWrap(True)
        vbox.addWidget(Label_error)        
        Label_error.hide()
        self.Label_error = Label_error
        
        TextEdit = QtGui.QTextEdit()
        TextEdit.setAcceptRichText(False)
        TextEdit.setAutoFormatting(QtGui.QTextEdit.AutoNone)
        
        vbox.addWidget(TextEdit)
        self.TextEdit = TextEdit
        
        self.setLayout(vbox)
    
    def set_error(self, error):
        self.Label_error.setText(str(error))
        self.Label_error.show()
    
    def clear_error(self):
        self.Label_error.hide()
    
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
    
    def getDeformated(self):
        raw_html = self.getHtml()
        deformated = richtext.deformat_html(raw_html,
                (richtext.KEEPIF['black-bold'], 
                 richtext.KEEPIF['red-underlined-bold']))
        deformated_str = richtext.get_str_formated_true(deformated)
        return deformated_str
    
    # seting text functions
    def setHtml(self, html):
        self.TextEdit.setHtml(html)
    def setText(self, text):
        plain_text_html = richtext.get_str_plain_html(text)
        self.setHtml(plain_text_html)
        
from cloudtb.extra.PyQt import treeview

def _init_node_list(node_list):
    '''Initializes the node list so that their do_replace variables are all
    set to True (default).
    do_replace == True  -- all regexp replaced
    do_replace == None  -- some regexp replaced
    do_replace == False -- No regexp replaced
    '''    
    for node in node_list:
        if node.isdir:
            _init_node_list(node._children)
        else:
            node.do_replace = True
    
#self.connect(lb,QtCore.SIGNAL("itemDoubleClicked (QListWidgetItem *)")
#    ,self.someMethod) 

class FileTreeModel(treeview.TableViewModel):
    def update_files(self, fullpath_list):
        '''deletes the current files and updates to the files on the
        fullpath_list'''
        self.clear_rows()
        rows = treeview.get_filelist_nodes(fullpath_list)
        
        self.insertRows(0, rows)

        