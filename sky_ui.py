# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'sky_ui.ui'
#
# Created: Mon Oct 14 19:54:19 2013
#      by: PyQt4 UI code generator 4.9.1
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_SearchTheSky_window(object):
    def setupUi(self, SearchTheSky_window):
        SearchTheSky_window.setObjectName(_fromUtf8("SearchTheSky_window"))
        SearchTheSky_window.resize(452, 390)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(SearchTheSky_window.sizePolicy().hasHeightForWidth())
        SearchTheSky_window.setSizePolicy(sizePolicy)
        SearchTheSky_window.setAnimated(True)
        self.centralwidget = QtGui.QWidget(SearchTheSky_window)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.tabWidget_lower = QtGui.QTabWidget(self.centralwidget)
        self.tabWidget_lower.setEnabled(True)
        self.tabWidget_lower.setGeometry(QtCore.QRect(0, 83, 441, 271))
        self.tabWidget_lower.setObjectName(_fromUtf8("tabWidget_lower"))
        self.tab_files = QtGui.QWidget()
        self.tab_files.setObjectName(_fromUtf8("tab_files"))
        self.groupBox_2 = QtGui.QGroupBox(self.tab_files)
        self.groupBox_2.setGeometry(QtCore.QRect(0, 0, 421, 41))
        self.groupBox_2.setObjectName(_fromUtf8("groupBox_2"))
        self.pushButton_find = QtGui.QPushButton(self.groupBox_2)
        self.pushButton_find.setGeometry(QtCore.QRect(330, 12, 79, 25))
        self.pushButton_find.setObjectName(_fromUtf8("pushButton_find"))
        self.toolButton_folder = QtGui.QToolButton(self.groupBox_2)
        self.toolButton_folder.setGeometry(QtCore.QRect(10, 15, 41, 21))
        self.toolButton_folder.setToolButtonStyle(QtCore.Qt.ToolButtonIconOnly)
        self.toolButton_folder.setObjectName(_fromUtf8("toolButton_folder"))
        self.lineEdit_folder = QtGui.QLineEdit(self.groupBox_2)
        self.lineEdit_folder.setGeometry(QtCore.QRect(50, 14, 271, 21))
        self.lineEdit_folder.setObjectName(_fromUtf8("lineEdit_folder"))
        self.treeView_files = QtGui.QTreeView(self.tab_files)
        self.treeView_files.setGeometry(QtCore.QRect(10, 51, 141, 191))
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.treeView_files.sizePolicy().hasHeightForWidth())
        self.treeView_files.setSizePolicy(sizePolicy)
        self.treeView_files.setObjectName(_fromUtf8("treeView_files"))
        self.textBrowser_files = QtGui.QTextBrowser(self.tab_files)
        self.textBrowser_files.setGeometry(QtCore.QRect(160, 73, 271, 171))
        self.textBrowser_files.setObjectName(_fromUtf8("textBrowser_files"))
        self.groupBox_4 = QtGui.QGroupBox(self.tab_files)
        self.groupBox_4.setGeometry(QtCore.QRect(270, 40, 161, 31))
        self.groupBox_4.setObjectName(_fromUtf8("groupBox_4"))
        self.radioButton_files_match = QtGui.QRadioButton(self.groupBox_4)
        self.radioButton_files_match.setGeometry(QtCore.QRect(10, 10, 98, 20))
        self.radioButton_files_match.setChecked(True)
        self.radioButton_files_match.setObjectName(_fromUtf8("radioButton_files_match"))
        self.radioButton_files_replace = QtGui.QRadioButton(self.groupBox_4)
        self.radioButton_files_replace.setGeometry(QtCore.QRect(80, 10, 98, 20))
        self.radioButton_files_replace.setObjectName(_fromUtf8("radioButton_files_replace"))
        self.pushButton_replace_all = QtGui.QPushButton(self.tab_files)
        self.pushButton_replace_all.setGeometry(QtCore.QRect(168, 44, 81, 25))
        self.pushButton_replace_all.setObjectName(_fromUtf8("pushButton_replace_all"))
        self.tabWidget_lower.addTab(self.tab_files, _fromUtf8(""))
        self.tab_text = QtGui.QWidget()
        self.tab_text.setObjectName(_fromUtf8("tab_text"))
        self.textEdit_input = QtGui.QTextEdit(self.tab_text)
        self.textEdit_input.setGeometry(QtCore.QRect(0, 30, 431, 211))
        self.textEdit_input.setAutoFormatting(QtGui.QTextEdit.AutoNone)
        self.textEdit_input.setAcceptRichText(False)
        self.textEdit_input.setObjectName(_fromUtf8("textEdit_input"))
        self.groupBox = QtGui.QGroupBox(self.tab_text)
        self.groupBox.setGeometry(QtCore.QRect(0, 0, 161, 31))
        self.groupBox.setObjectName(_fromUtf8("groupBox"))
        self.radioButton_text_match = QtGui.QRadioButton(self.groupBox)
        self.radioButton_text_match.setGeometry(QtCore.QRect(10, 10, 98, 20))
        self.radioButton_text_match.setChecked(True)
        self.radioButton_text_match.setObjectName(_fromUtf8("radioButton_text_match"))
        self.radioButton_text_replace = QtGui.QRadioButton(self.groupBox)
        self.radioButton_text_replace.setGeometry(QtCore.QRect(80, 10, 98, 20))
        self.radioButton_text_replace.setChecked(False)
        self.radioButton_text_replace.setObjectName(_fromUtf8("radioButton_text_replace"))
        self.pushButton = QtGui.QPushButton(self.tab_text)
        self.pushButton.setGeometry(QtCore.QRect(360, 3, 61, 25))
        self.pushButton.setObjectName(_fromUtf8("pushButton"))
        self.label = QtGui.QLabel(self.tab_text)
        self.label.setGeometry(QtCore.QRect(210, 10, 121, 16))
        font = QtGui.QFont()
        font.setPointSize(15)
        font.setBold(True)
        font.setItalic(True)
        font.setWeight(75)
        self.label.setFont(font)
        self.label.setObjectName(_fromUtf8("label"))
        self.tabWidget_lower.addTab(self.tab_text, _fromUtf8(""))
        self.tab_help = QtGui.QWidget()
        self.tab_help.setObjectName(_fromUtf8("tab_help"))
        self.comboBox_help = QtGui.QComboBox(self.tab_help)
        self.comboBox_help.setGeometry(QtCore.QRect(10, 10, 411, 22))
        self.comboBox_help.setObjectName(_fromUtf8("comboBox_help"))
        self.textBrowser_help = QtGui.QTextBrowser(self.tab_help)
        self.textBrowser_help.setGeometry(QtCore.QRect(10, 40, 421, 201))
        self.textBrowser_help.setTextInteractionFlags(QtCore.Qt.LinksAccessibleByKeyboard|QtCore.Qt.LinksAccessibleByMouse|QtCore.Qt.TextBrowserInteraction|QtCore.Qt.TextSelectableByKeyboard|QtCore.Qt.TextSelectableByMouse)
        self.textBrowser_help.setObjectName(_fromUtf8("textBrowser_help"))
        self.tabWidget_lower.addTab(self.tab_help, _fromUtf8(""))
        self.tabWidget_upper = QtGui.QTabWidget(self.centralwidget)
        self.tabWidget_upper.setGeometry(QtCore.QRect(0, 0, 441, 81))
        self.tabWidget_upper.setObjectName(_fromUtf8("tabWidget_upper"))
        self.tab = QtGui.QWidget()
        self.tab.setObjectName(_fromUtf8("tab"))
        self.lineEdit_input = QtGui.QLineEdit(self.tab)
        self.lineEdit_input.setGeometry(QtCore.QRect(120, 0, 301, 21))
        self.lineEdit_input.setObjectName(_fromUtf8("lineEdit_input"))
        self.lineEdit_replace = QtGui.QLineEdit(self.tab)
        self.lineEdit_replace.setGeometry(QtCore.QRect(120, 30, 301, 21))
        self.lineEdit_replace.setObjectName(_fromUtf8("lineEdit_replace"))
        self.label_main_top = QtGui.QLabel(self.tab)
        self.label_main_top.setGeometry(QtCore.QRect(10, 2, 101, 16))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label_main_top.setFont(font)
        self.label_main_top.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_main_top.setObjectName(_fromUtf8("label_main_top"))
        self.label__main_bottom = QtGui.QLabel(self.tab)
        self.label__main_bottom.setGeometry(QtCore.QRect(10, 32, 101, 16))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label__main_bottom.setFont(font)
        self.label__main_bottom.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label__main_bottom.setObjectName(_fromUtf8("label__main_bottom"))
        self.tabWidget_upper.addTab(self.tab, _fromUtf8(""))
        SearchTheSky_window.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(SearchTheSky_window)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 452, 20))
        self.menubar.setObjectName(_fromUtf8("menubar"))
        self.menuOptions = QtGui.QMenu(self.menubar)
        self.menuOptions.setObjectName(_fromUtf8("menuOptions"))
        self.menuMode = QtGui.QMenu(self.menuOptions)
        self.menuMode.setObjectName(_fromUtf8("menuMode"))
        SearchTheSky_window.setMenuBar(self.menubar)
        self.statusbar = QtGui.QStatusBar(SearchTheSky_window)
        self.statusbar.setObjectName(_fromUtf8("statusbar"))
        SearchTheSky_window.setStatusBar(self.statusbar)
        self.menu_quick_search = QtGui.QAction(SearchTheSky_window)
        self.menu_quick_search.setCheckable(False)
        self.menu_quick_search.setChecked(False)
        self.menu_quick_search.setEnabled(False)
        self.menu_quick_search.setObjectName(_fromUtf8("menu_quick_search"))
        self.actionRegexp_P_ython_erl = QtGui.QAction(SearchTheSky_window)
        self.actionRegexp_P_ython_erl.setObjectName(_fromUtf8("actionRegexp_P_ython_erl"))
        self.actionPy_refactor = QtGui.QAction(SearchTheSky_window)
        self.actionPy_refactor.setEnabled(False)
        self.actionPy_refactor.setObjectName(_fromUtf8("actionPy_refactor"))
        self.menuMode.addAction(self.actionRegexp_P_ython_erl)
        self.menuMode.addAction(self.actionPy_refactor)
        self.menuOptions.addAction(self.menu_quick_search)
        self.menuOptions.addAction(self.menuMode.menuAction())
        self.menubar.addAction(self.menuOptions.menuAction())

        self.retranslateUi(SearchTheSky_window)
        self.tabWidget_lower.setCurrentIndex(1)
        self.tabWidget_upper.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(SearchTheSky_window)

    def retranslateUi(self, SearchTheSky_window):
        SearchTheSky_window.setWindowTitle(QtGui.QApplication.translate("SearchTheSky_window", "Search The Sky", None, QtGui.QApplication.UnicodeUTF8))
        self.groupBox_2.setTitle(QtGui.QApplication.translate("SearchTheSky_window", "Folder", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButton_find.setText(QtGui.QApplication.translate("SearchTheSky_window", "Find", None, QtGui.QApplication.UnicodeUTF8))
        self.toolButton_folder.setText(QtGui.QApplication.translate("SearchTheSky_window", "...", None, QtGui.QApplication.UnicodeUTF8))
        self.groupBox_4.setTitle(QtGui.QApplication.translate("SearchTheSky_window", "Display", None, QtGui.QApplication.UnicodeUTF8))
        self.radioButton_files_match.setText(QtGui.QApplication.translate("SearchTheSky_window", "Match", None, QtGui.QApplication.UnicodeUTF8))
        self.radioButton_files_replace.setText(QtGui.QApplication.translate("SearchTheSky_window", "Replace", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButton_replace_all.setText(QtGui.QApplication.translate("SearchTheSky_window", "Replace All", None, QtGui.QApplication.UnicodeUTF8))
        self.tabWidget_lower.setTabText(self.tabWidget_lower.indexOf(self.tab_files), QtGui.QApplication.translate("SearchTheSky_window", "Files", None, QtGui.QApplication.UnicodeUTF8))
        self.textEdit_input.setHtml(QtGui.QApplication.translate("SearchTheSky_window", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Sans Serif\'; font-size:9pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-weight:600; text-decoration: underline; vertical-align:sub;\">0:</span><span style=\" font-weight:600; color:#b30000;\">(</span><span style=\" font-weight:600; color:#000000;\">talking </span><span style=\" font-weight:600; color:#b3008d;\">(</span><span style=\" font-weight:600; color:#000000;\">about </span><span style=\" font-weight:600; color:#b3008d;\">)</span><span style=\" font-weight:600; color:#b3008d; vertical-align:sub;\">1</span><span style=\" font-weight:600; color:#000000;\">expect</span><span style=\" font-weight:600; color:#4b00b3;\">(</span><span style=\" font-weight:600; color:#000000;\">ing </span><span style=\" font-weight:600; color:#4b00b3;\">)</span><span style=\" font-weight:600; color:#4b00b3; vertical-align:sub;\">2</span><span style=\" font-weight:600; color:#0041b3;\">(</span><span style=\" font-weight:600; color:#000000;\">the </span><span style=\" font-weight:600; color:#0041b3;\">)</span><span style=\" font-weight:600; color:#0041b3; vertical-align:sub;\">3</span><span style=\" font-weight:600; color:#000000;\">Spanish Inquisition</span><span style=\" font-weight:600; color:#00b398;\">(</span><span style=\" font-weight:600; color:#000000;\"> </span><span style=\" font-weight:600; color:#00b398;\">)</span><span style=\" font-weight:600; color:#00b398; vertical-align:sub;\">4</span><span style=\" font-weight:600; color:#b30000;\">)</span><span style=\" font-weight:600; color:#b30000; vertical-align:sub;\">0</span>in the text below: </p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">    Chapman: <span style=\" font-weight:600; text-decoration: underline; vertical-align:sub;\">1:</span><span style=\" font-weight:600; color:#b30000;\">(</span><span style=\" font-weight:600; color:#000000;\">I </span><span style=\" font-weight:600; color:#b3008d;\">(</span><span style=\" font-weight:600; color:#000000;\">didn\'t </span><span style=\" font-weight:600; color:#b3008d;\">)</span><span style=\" font-weight:600; color:#b3008d; vertical-align:sub;\">1</span><span style=\" font-weight:600; color:#000000;\">expect</span><span style=\" font-weight:600; color:#4b00b3;\">(</span><span style=\" font-weight:600; color:#000000;\"> a kind of </span><span style=\" font-weight:600; color:#4b00b3;\">)</span><span style=\" font-weight:600; color:#4b00b3; vertical-align:sub;\">2</span><span style=\" font-weight:600; color:#000000;\">Spanish Inquisition</span><span style=\" font-weight:600; color:#00b398;\">(</span><span style=\" font-weight:600; color:#000000;\">.</span><span style=\" font-weight:600; color:#00b398;\">)</span><span style=\" font-weight:600; color:#00b398; vertical-align:sub;\">4</span><span style=\" font-weight:600; color:#b30000;\">)</span><span style=\" font-weight:600; color:#b30000; vertical-align:sub;\">0</span> </p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">    (JARRING CHORD - the cardinals burst in) </p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">    Ximinez: <span style=\" font-weight:600; text-decoration: underline; vertical-align:sub;\">2:</span><span style=\" font-weight:600; color:#b30000;\">(</span><span style=\" font-weight:600; color:#b3008d;\">(</span><span style=\" font-weight:600; color:#000000;\">NOBODY </span><span style=\" font-weight:600; color:#b3008d;\">)</span><span style=\" font-weight:600; color:#b3008d; vertical-align:sub;\">1</span><span style=\" font-weight:600; color:#000000;\">expect</span><span style=\" font-weight:600; color:#4b00b3;\">(</span><span style=\" font-weight:600; color:#000000;\">s </span><span style=\" font-weight:600; color:#4b00b3;\">)</span><span style=\" font-weight:600; color:#4b00b3; vertical-align:sub;\">2</span><span style=\" font-weight:600; color:#0041b3;\">(</span><span style=\" font-weight:600; color:#000000;\">the </span><span style=\" font-weight:600; color:#0041b3;\">)</span><span style=\" font-weight:600; color:#0041b3; vertical-align:sub;\">3</span><span style=\" font-weight:600; color:#000000;\">Spanish Inquisition</span><span style=\" font-weight:600; color:#00b398;\">(</span><span style=\" font-weight:600; color:#000000;\">!</span><span style=\" font-weight:600; color:#00b398;\">)</span><span style=\" font-weight:600; color:#00b398; vertical-align:sub;\">4</span><span style=\" font-weight:600; color:#b30000;\">)</span><span style=\" font-weight:600; color:#b30000; vertical-align:sub;\">0</span> Our chief weapon is surprise...surprise and fear...fear and surprise.... Our two weapons are fear and surprise...and ruthless efficiency.... Our *three* weapons are fear, surprise, and ruthless efficiency...and an almost fanatical devotion to the Pope.... Our *four*...no... *Amongst* our weapons.... Amongst our weaponry...are such elements as fear, surprise.... I\'ll come in again. (Exit and exeunt) </p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">    </p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.groupBox.setTitle(QtGui.QApplication.translate("SearchTheSky_window", "Display", None, QtGui.QApplication.UnicodeUTF8))
        self.radioButton_text_match.setText(QtGui.QApplication.translate("SearchTheSky_window", "Match", None, QtGui.QApplication.UnicodeUTF8))
        self.radioButton_text_replace.setText(QtGui.QApplication.translate("SearchTheSky_window", "Replace", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButton.setToolTip(QtGui.QApplication.translate("SearchTheSky_window", "Copy results to clipboard", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButton.setText(QtGui.QApplication.translate("SearchTheSky_window", "Copy", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("SearchTheSky_window", "TextLabel", None, QtGui.QApplication.UnicodeUTF8))
        self.tabWidget_lower.setTabText(self.tabWidget_lower.indexOf(self.tab_text), QtGui.QApplication.translate("SearchTheSky_window", "Text", None, QtGui.QApplication.UnicodeUTF8))
        self.textBrowser_help.setDocumentTitle(QtGui.QApplication.translate("SearchTheSky_window", "Help", None, QtGui.QApplication.UnicodeUTF8))
        self.tabWidget_lower.setTabText(self.tabWidget_lower.indexOf(self.tab_help), QtGui.QApplication.translate("SearchTheSky_window", "Help", None, QtGui.QApplication.UnicodeUTF8))
        self.lineEdit_input.setText(QtGui.QApplication.translate("SearchTheSky_window", "([a-zA-Z\']+\\s)+?expect(.*?)(the )*Spanish Inquisition(!|.)", None, QtGui.QApplication.UnicodeUTF8))
        self.lineEdit_replace.setText(QtGui.QApplication.translate("SearchTheSky_window", "What is this, the Spanish Inquisition?", None, QtGui.QApplication.UnicodeUTF8))
        self.label_main_top.setText(QtGui.QApplication.translate("SearchTheSky_window", "Reg Exp", None, QtGui.QApplication.UnicodeUTF8))
        self.label__main_bottom.setText(QtGui.QApplication.translate("SearchTheSky_window", "Replace", None, QtGui.QApplication.UnicodeUTF8))
        self.tabWidget_upper.setTabText(self.tabWidget_upper.indexOf(self.tab), QtGui.QApplication.translate("SearchTheSky_window", "Search", None, QtGui.QApplication.UnicodeUTF8))
        self.menuOptions.setTitle(QtGui.QApplication.translate("SearchTheSky_window", "Options", None, QtGui.QApplication.UnicodeUTF8))
        self.menuMode.setTitle(QtGui.QApplication.translate("SearchTheSky_window", "Mode", None, QtGui.QApplication.UnicodeUTF8))
        self.menu_quick_search.setText(QtGui.QApplication.translate("SearchTheSky_window", "Quick Search", None, QtGui.QApplication.UnicodeUTF8))
        self.actionRegexp_P_ython_erl.setText(QtGui.QApplication.translate("SearchTheSky_window", "regexp P(erl|ython)", None, QtGui.QApplication.UnicodeUTF8))
        self.actionPy_refactor.setText(QtGui.QApplication.translate("SearchTheSky_window", "py refactor", None, QtGui.QApplication.UnicodeUTF8))
        self.actionPy_refactor.setToolTip(QtGui.QApplication.translate("SearchTheSky_window", "To Be Implemented!", None, QtGui.QApplication.UnicodeUTF8))

