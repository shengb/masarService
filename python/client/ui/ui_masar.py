# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui_masar.ui'
#
# Created: Thu Mar  1 14:54:56 2012
#      by: PyQt4 UI code generator 4.8.6
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_masar(object):
    def setupUi(self, masar):
        masar.setObjectName(_fromUtf8("masar"))
        masar.resize(1207, 919)
        masar.setWindowTitle(QtGui.QApplication.translate("masar", "MASAR Viewer", None, QtGui.QApplication.UnicodeUTF8))
        self.mainwidget = QtGui.QWidget(masar)
        self.mainwidget.setObjectName(_fromUtf8("mainwidget"))
        self.verticalLayout_2 = QtGui.QVBoxLayout(self.mainwidget)
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.splitter = QtGui.QSplitter(self.mainwidget)
        self.splitter.setOrientation(QtCore.Qt.Horizontal)
        self.splitter.setObjectName(_fromUtf8("splitter"))
        self.configEventSplitter = QtGui.QSplitter(self.splitter)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.configEventSplitter.sizePolicy().hasHeightForWidth())
        self.configEventSplitter.setSizePolicy(sizePolicy)
        self.configEventSplitter.setOrientation(QtCore.Qt.Vertical)
        self.configEventSplitter.setObjectName(_fromUtf8("configEventSplitter"))
        self.layoutWidget = QtGui.QWidget(self.configEventSplitter)
        self.layoutWidget.setObjectName(_fromUtf8("layoutWidget"))
        self.configVerticalLayout = QtGui.QVBoxLayout(self.layoutWidget)
        self.configVerticalLayout.setMargin(0)
        self.configVerticalLayout.setObjectName(_fromUtf8("configVerticalLayout"))
        self.configGridLayout = QtGui.QGridLayout()
        self.configGridLayout.setObjectName(_fromUtf8("configGridLayout"))
        self.systemLabel = QtGui.QLabel(self.layoutWidget)
        self.systemLabel.setText(QtGui.QApplication.translate("masar", "System", None, QtGui.QApplication.UnicodeUTF8))
        self.systemLabel.setObjectName(_fromUtf8("systemLabel"))
        self.configGridLayout.addWidget(self.systemLabel, 0, 0, 1, 1)
        self.systemCombox = QtGui.QComboBox(self.layoutWidget)
        self.systemCombox.setObjectName(_fromUtf8("systemCombox"))
        self.configGridLayout.addWidget(self.systemCombox, 0, 1, 1, 1)
        self.configFilterLabel = QtGui.QLabel(self.layoutWidget)
        self.configFilterLabel.setText(QtGui.QApplication.translate("masar", "Config Filter", None, QtGui.QApplication.UnicodeUTF8))
        self.configFilterLabel.setObjectName(_fromUtf8("configFilterLabel"))
        self.configGridLayout.addWidget(self.configFilterLabel, 1, 0, 1, 1)
        self.configFilterLineEdit = QtGui.QLineEdit(self.layoutWidget)
        self.configFilterLineEdit.setText(QtGui.QApplication.translate("masar", "*", None, QtGui.QApplication.UnicodeUTF8))
        self.configFilterLineEdit.setObjectName(_fromUtf8("configFilterLineEdit"))
        self.configGridLayout.addWidget(self.configFilterLineEdit, 1, 1, 1, 1)
        self.fetchConfigButton = QtGui.QPushButton(self.layoutWidget)
        self.fetchConfigButton.setText(QtGui.QApplication.translate("masar", "Fetch Config(s)", None, QtGui.QApplication.UnicodeUTF8))
        self.fetchConfigButton.setObjectName(_fromUtf8("fetchConfigButton"))
        self.configGridLayout.addWidget(self.fetchConfigButton, 2, 0, 1, 1)
        self.configTableWidget = QtGui.QTableWidget(self.layoutWidget)
        self.configTableWidget.setSelectionMode(QtGui.QAbstractItemView.ExtendedSelection)
        self.configTableWidget.setSelectionBehavior(QtGui.QAbstractItemView.SelectRows)
        self.configTableWidget.setObjectName(_fromUtf8("configTableWidget"))
        self.configTableWidget.setColumnCount(0)
        self.configTableWidget.setRowCount(0)
        self.configGridLayout.addWidget(self.configTableWidget, 3, 0, 1, 2)
        self.configVerticalLayout.addLayout(self.configGridLayout)
        self.layoutWidget1 = QtGui.QWidget(self.configEventSplitter)
        self.layoutWidget1.setObjectName(_fromUtf8("layoutWidget1"))
        self.eventVerticalLayout = QtGui.QVBoxLayout(self.layoutWidget1)
        self.eventVerticalLayout.setMargin(0)
        self.eventVerticalLayout.setObjectName(_fromUtf8("eventVerticalLayout"))
        self.eventGridLayout = QtGui.QGridLayout()
        self.eventGridLayout.setObjectName(_fromUtf8("eventGridLayout"))
        self.timeRangeCheckBox = QtGui.QCheckBox(self.layoutWidget1)
        self.timeRangeCheckBox.setText(QtGui.QApplication.translate("masar", "Use time range:", None, QtGui.QApplication.UnicodeUTF8))
        self.timeRangeCheckBox.setObjectName(_fromUtf8("timeRangeCheckBox"))
        self.eventGridLayout.addWidget(self.timeRangeCheckBox, 2, 0, 1, 3)
        self.eventStartLabel = QtGui.QLabel(self.layoutWidget1)
        self.eventStartLabel.setText(QtGui.QApplication.translate("masar", "From:", None, QtGui.QApplication.UnicodeUTF8))
        self.eventStartLabel.setObjectName(_fromUtf8("eventStartLabel"))
        self.eventGridLayout.addWidget(self.eventStartLabel, 3, 0, 1, 1)
        self.eventStartDateTime = QtGui.QDateTimeEdit(self.layoutWidget1)
        self.eventStartDateTime.setEnabled(False)
        self.eventStartDateTime.setAlignment(QtCore.Qt.AlignCenter)
        self.eventStartDateTime.setReadOnly(False)
        self.eventStartDateTime.setDisplayFormat(QtGui.QApplication.translate("masar", "yyyy-MM-dd hh:mm:ss", None, QtGui.QApplication.UnicodeUTF8))
        self.eventStartDateTime.setCalendarPopup(True)
        self.eventStartDateTime.setObjectName(_fromUtf8("eventStartDateTime"))
        self.eventGridLayout.addWidget(self.eventStartDateTime, 3, 2, 1, 2)
        self.eventEndLabel = QtGui.QLabel(self.layoutWidget1)
        self.eventEndLabel.setText(QtGui.QApplication.translate("masar", "To:", None, QtGui.QApplication.UnicodeUTF8))
        self.eventEndLabel.setObjectName(_fromUtf8("eventEndLabel"))
        self.eventGridLayout.addWidget(self.eventEndLabel, 4, 0, 1, 1)
        self.fetchEventButton = QtGui.QPushButton(self.layoutWidget1)
        self.fetchEventButton.setText(QtGui.QApplication.translate("masar", "Fetch Event(s)", None, QtGui.QApplication.UnicodeUTF8))
        self.fetchEventButton.setObjectName(_fromUtf8("fetchEventButton"))
        self.eventGridLayout.addWidget(self.fetchEventButton, 5, 0, 1, 3)
        self.eventEndDateTime = QtGui.QDateTimeEdit(self.layoutWidget1)
        self.eventEndDateTime.setEnabled(False)
        self.eventEndDateTime.setAlignment(QtCore.Qt.AlignCenter)
        self.eventEndDateTime.setReadOnly(False)
        self.eventEndDateTime.setDateTime(QtCore.QDateTime(QtCore.QDate(2000, 3, 1), QtCore.QTime(0, 0, 0)))
        self.eventEndDateTime.setDisplayFormat(QtGui.QApplication.translate("masar", "yyyy-MM-dd hh:mm:ss", None, QtGui.QApplication.UnicodeUTF8))
        self.eventEndDateTime.setCalendarPopup(True)
        self.eventEndDateTime.setObjectName(_fromUtf8("eventEndDateTime"))
        self.eventGridLayout.addWidget(self.eventEndDateTime, 4, 2, 1, 2)
        self.eventFilterLineEdit = QtGui.QLineEdit(self.layoutWidget1)
        self.eventFilterLineEdit.setText(QtGui.QApplication.translate("masar", "*", None, QtGui.QApplication.UnicodeUTF8))
        self.eventFilterLineEdit.setObjectName(_fromUtf8("eventFilterLineEdit"))
        self.eventGridLayout.addWidget(self.eventFilterLineEdit, 0, 3, 1, 1)
        self.authorTextEdit = QtGui.QLineEdit(self.layoutWidget1)
        self.authorTextEdit.setText(QtGui.QApplication.translate("masar", "*", None, QtGui.QApplication.UnicodeUTF8))
        self.authorTextEdit.setObjectName(_fromUtf8("authorTextEdit"))
        self.eventGridLayout.addWidget(self.authorTextEdit, 1, 3, 1, 1)
        self.eventFilterLabel = QtGui.QLabel(self.layoutWidget1)
        self.eventFilterLabel.setText(QtGui.QApplication.translate("masar", "Event Desc", None, QtGui.QApplication.UnicodeUTF8))
        self.eventFilterLabel.setObjectName(_fromUtf8("eventFilterLabel"))
        self.eventGridLayout.addWidget(self.eventFilterLabel, 0, 0, 1, 1)
        self.ByWho = QtGui.QLabel(self.layoutWidget1)
        self.ByWho.setText(QtGui.QApplication.translate("masar", "Author", None, QtGui.QApplication.UnicodeUTF8))
        self.ByWho.setObjectName(_fromUtf8("ByWho"))
        self.eventGridLayout.addWidget(self.ByWho, 1, 0, 1, 1)
        self.eventVerticalLayout.addLayout(self.eventGridLayout)
        self.eventTableWidget = QtGui.QTableWidget(self.layoutWidget1)
        self.eventTableWidget.setSelectionMode(QtGui.QAbstractItemView.ExtendedSelection)
        self.eventTableWidget.setSelectionBehavior(QtGui.QAbstractItemView.SelectRows)
        self.eventTableWidget.setObjectName(_fromUtf8("eventTableWidget"))
        self.eventTableWidget.setColumnCount(0)
        self.eventTableWidget.setRowCount(0)
        self.eventVerticalLayout.addWidget(self.eventTableWidget)
        self.snapshotHorizontalLayout = QtGui.QHBoxLayout()
        self.snapshotHorizontalLayout.setObjectName(_fromUtf8("snapshotHorizontalLayout"))
        self.fetchSnapshotButton = QtGui.QPushButton(self.layoutWidget1)
        self.fetchSnapshotButton.setText(QtGui.QApplication.translate("masar", "Fetch Snapshot", None, QtGui.QApplication.UnicodeUTF8))
        self.fetchSnapshotButton.setObjectName(_fromUtf8("fetchSnapshotButton"))
        self.snapshotHorizontalLayout.addWidget(self.fetchSnapshotButton)
        self.eventVerticalLayout.addLayout(self.snapshotHorizontalLayout)
        self.layoutWidget2 = QtGui.QWidget(self.splitter)
        self.layoutWidget2.setObjectName(_fromUtf8("layoutWidget2"))
        self.verticalLayout = QtGui.QVBoxLayout(self.layoutWidget2)
        self.verticalLayout.setMargin(0)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.snapshotTabWidget = QtGui.QTabWidget(self.layoutWidget2)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(3)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.snapshotTabWidget.sizePolicy().hasHeightForWidth())
        self.snapshotTabWidget.setSizePolicy(sizePolicy)
        self.snapshotTabWidget.setMinimumSize(QtCore.QSize(768, 0))
        self.snapshotTabWidget.setObjectName(_fromUtf8("snapshotTabWidget"))
        self.commentTab = QtGui.QWidget()
        self.commentTab.setObjectName(_fromUtf8("commentTab"))
        self.commentTabWindowLayout = QtGui.QVBoxLayout(self.commentTab)
        self.commentTabWindowLayout.setObjectName(_fromUtf8("commentTabWindowLayout"))
        self.commentInputLabel = QtGui.QLabel(self.commentTab)
        self.commentInputLabel.setText(QtGui.QApplication.translate("masar", "Enter comment:", None, QtGui.QApplication.UnicodeUTF8))
        self.commentInputLabel.setObjectName(_fromUtf8("commentInputLabel"))
        self.commentTabWindowLayout.addWidget(self.commentInputLabel)
        self.commentInputTextEdit = QtGui.QPlainTextEdit(self.commentTab)
        self.commentInputTextEdit.setObjectName(_fromUtf8("commentInputTextEdit"))
        self.commentTabWindowLayout.addWidget(self.commentInputTextEdit)
        self.currentCommentLabel = QtGui.QLabel(self.commentTab)
        self.currentCommentLabel.setText(QtGui.QApplication.translate("masar", "Enter comment:", None, QtGui.QApplication.UnicodeUTF8))
        self.currentCommentLabel.setObjectName(_fromUtf8("currentCommentLabel"))
        self.commentTabWindowLayout.addWidget(self.currentCommentLabel)
        self.currentCommentText = QtGui.QPlainTextEdit(self.commentTab)
        palette = QtGui.QPalette()
        brush = QtGui.QBrush(QtGui.QColor(231, 231, 231))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(231, 231, 231))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Base, brush)
        self.currentCommentText.setPalette(palette)
        self.currentCommentText.setAutoFillBackground(True)
        self.currentCommentText.setReadOnly(True)
        self.currentCommentText.setPlainText(QtGui.QApplication.translate("masar", "This is a fake snapshot comment message.", None, QtGui.QApplication.UnicodeUTF8))
        self.currentCommentText.setBackgroundVisible(False)
        self.currentCommentText.setObjectName(_fromUtf8("currentCommentText"))
        self.commentTabWindowLayout.addWidget(self.currentCommentText)
        self.snapshotTabWidget.addTab(self.commentTab, _fromUtf8(""))
        self.verticalLayout.addWidget(self.snapshotTabWidget)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.machinePreviewButton = QtGui.QPushButton(self.layoutWidget2)
        self.machinePreviewButton.setText(QtGui.QApplication.translate("masar", "Preview", None, QtGui.QApplication.UnicodeUTF8))
        self.machinePreviewButton.setObjectName(_fromUtf8("machinePreviewButton"))
        self.horizontalLayout.addWidget(self.machinePreviewButton)
        self.saveCurrentPreviewButton = QtGui.QPushButton(self.layoutWidget2)
        self.saveCurrentPreviewButton.setText(QtGui.QApplication.translate("masar", "Save Current Preview", None, QtGui.QApplication.UnicodeUTF8))
        self.saveCurrentPreviewButton.setObjectName(_fromUtf8("saveCurrentPreviewButton"))
        self.horizontalLayout.addWidget(self.saveCurrentPreviewButton)
        self.label = QtGui.QLabel(self.layoutWidget2)
        self.label.setText(_fromUtf8(""))
        self.label.setObjectName(_fromUtf8("label"))
        self.horizontalLayout.addWidget(self.label)
        self.getLiveMachineButton = QtGui.QPushButton(self.layoutWidget2)
        self.getLiveMachineButton.setText(QtGui.QApplication.translate("masar", "Compare Live Machine", None, QtGui.QApplication.UnicodeUTF8))
        self.getLiveMachineButton.setObjectName(_fromUtf8("getLiveMachineButton"))
        self.horizontalLayout.addWidget(self.getLiveMachineButton)
        self.label_2 = QtGui.QLabel(self.layoutWidget2)
        self.label_2.setText(_fromUtf8(""))
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.horizontalLayout.addWidget(self.label_2)
        self.restoreMachineButton = QtGui.QPushButton(self.layoutWidget2)
        self.restoreMachineButton.setText(QtGui.QApplication.translate("masar", "Restore Machine", None, QtGui.QApplication.UnicodeUTF8))
        self.restoreMachineButton.setObjectName(_fromUtf8("restoreMachineButton"))
        self.horizontalLayout.addWidget(self.restoreMachineButton)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.verticalLayout_2.addWidget(self.splitter)
        masar.setCentralWidget(self.mainwidget)
        self.menubar = QtGui.QMenuBar(masar)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1207, 22))
        self.menubar.setObjectName(_fromUtf8("menubar"))
        masar.setMenuBar(self.menubar)
        self.statusbar = QtGui.QStatusBar(masar)
        self.statusbar.setObjectName(_fromUtf8("statusbar"))
        masar.setStatusBar(self.statusbar)

        self.retranslateUi(masar)
        self.systemCombox.setCurrentIndex(-1)
        self.snapshotTabWidget.setCurrentIndex(0)
        QtCore.QObject.connect(self.systemCombox, QtCore.SIGNAL(_fromUtf8("currentIndexChanged(QString)")), masar.systemComboxChanged)
        QtCore.QObject.connect(self.configFilterLineEdit, QtCore.SIGNAL(_fromUtf8("textChanged(QString)")), masar.configFilterChanged)
        QtCore.QObject.connect(self.fetchConfigButton, QtCore.SIGNAL(_fromUtf8("clicked()")), masar.fetchConfigAction)
        QtCore.QObject.connect(self.saveCurrentPreviewButton, QtCore.SIGNAL(_fromUtf8("clicked()")), masar.saveMachinePreviewAction)
        QtCore.QObject.connect(self.eventFilterLineEdit, QtCore.SIGNAL(_fromUtf8("textChanged(QString)")), masar.eventFilterChanged)
        QtCore.QObject.connect(self.authorTextEdit, QtCore.SIGNAL(_fromUtf8("textChanged(QString)")), masar.authorTextChanged)
        QtCore.QObject.connect(self.timeRangeCheckBox, QtCore.SIGNAL(_fromUtf8("stateChanged(int)")), masar.useTimeRange)
        QtCore.QObject.connect(self.fetchEventButton, QtCore.SIGNAL(_fromUtf8("clicked(void)")), masar.fetchEventAction)
        QtCore.QObject.connect(self.fetchSnapshotButton, QtCore.SIGNAL(_fromUtf8("clicked(void)")), masar.retrieveSnapshot)
        QtCore.QObject.connect(self.restoreMachineButton, QtCore.SIGNAL(_fromUtf8("clicked(void)")), masar.restoreSnapshotAction)
        QtCore.QObject.connect(self.machinePreviewButton, QtCore.SIGNAL(_fromUtf8("clicked()")), masar.getMachinePreviewAction)
        QtCore.QObject.connect(self.getLiveMachineButton, QtCore.SIGNAL(_fromUtf8("clicked()")), masar.getLiveMachineAction)
        QtCore.QMetaObject.connectSlotsByName(masar)

    def retranslateUi(self, masar):
        self.configTableWidget.setSortingEnabled(True)
        self.eventTableWidget.setSortingEnabled(True)
        self.snapshotTabWidget.setTabText(self.snapshotTabWidget.indexOf(self.commentTab), QtGui.QApplication.translate("masar", "Comment", None, QtGui.QApplication.UnicodeUTF8))
