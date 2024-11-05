# -*- coding: utf-8 -*-

#
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_TabAnalysis(object):
    def setupUi(self, TabAnalysis):
        TabAnalysis.setObjectName("TabAnalysis")
        TabAnalysis.resize(1331, 739)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(TabAnalysis.sizePolicy().hasHeightForWidth())
        TabAnalysis.setSizePolicy(sizePolicy)
        TabAnalysis.setFocusPolicy(QtCore.Qt.ClickFocus)
        TabAnalysis.setAcceptDrops(True)
        TabAnalysis.setProperty("lineWidth", 1)
        TabAnalysis.setProperty("midLineWidth", 0)
        self.verticalLayout_7 = QtWidgets.QVBoxLayout(TabAnalysis)
        self.verticalLayout_7.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_7.setSpacing(0)
        self.verticalLayout_7.setObjectName("verticalLayout_7")
        self.scrollArea = QtWidgets.QScrollArea(TabAnalysis)
        self.scrollArea.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.scrollArea.setLineWidth(0)
        self.scrollArea.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAsNeeded)
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setObjectName("scrollArea")
        self.scrollAreaWidgetContents = QtWidgets.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 1331, 739))
        self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")
        self.verticalLayout_5 = QtWidgets.QVBoxLayout(self.scrollAreaWidgetContents)
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.splitter_2 = QtWidgets.QSplitter(self.scrollAreaWidgetContents)
        self.splitter_2.setStyleSheet(
            "QSplitter::handle:vertical {\n"
            "margin: 4px 0px;\n"
            "    background-color: qlineargradient(x1:0, y1:0, x2:1, y2:0, \n"
            "stop:0 rgba(255, 255, 255, 0), \n"
            "stop:0.5 rgba(100, 100, 100, 100), \n"
            "stop:1 rgba(255, 255, 255, 0));\n"
            "image: url(:/icons/icons/splitter_handle_horizontal.svg);\n"
            "}"
        )
        self.splitter_2.setOrientation(QtCore.Qt.Vertical)
        self.splitter_2.setHandleWidth(6)
        self.splitter_2.setObjectName("splitter_2")
        self.splitter = QtWidgets.QSplitter(self.splitter_2)
        self.splitter.setStyleSheet(
            "QSplitter::handle:horizontal {\n"
            "margin: 4px 0px;\n"
            "    background-color: qlineargradient(x1:0, y1:0, x2:0, y2:1, \n"
            "stop:0 rgba(255, 255, 255, 0), \n"
            "stop:0.5 rgba(100, 100, 100, 100), \n"
            "stop:1 rgba(255, 255, 255, 0));\n"
            "image: url(:/icons/icons/splitter_handle_vertical.svg);\n"
            "}"
        )
        self.splitter.setOrientation(QtCore.Qt.Horizontal)
        self.splitter.setHandleWidth(6)
        self.splitter.setObjectName("splitter")
        self.layoutWidget = QtWidgets.QWidget(self.splitter)
        self.layoutWidget.setObjectName("layoutWidget")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.layoutWidget)
        self.verticalLayout_2.setContentsMargins(11, 11, 11, 11)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.tabWidget = QtWidgets.QTabWidget(self.layoutWidget)
        self.tabWidget.setStyleSheet("QTabWidget::pane { border: 0; }")
        self.tabWidget.setObjectName("tabWidget")
        self.tab_protocols = QtWidgets.QWidget()
        self.tab_protocols.setObjectName("tab_protocols")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.tab_protocols)
        self.verticalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_3.setSpacing(7)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.treeViewProtocols = ProtocolTreeView(self.tab_protocols)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.treeViewProtocols.sizePolicy().hasHeightForWidth()
        )
        self.treeViewProtocols.setSizePolicy(sizePolicy)
        self.treeViewProtocols.setAcceptDrops(True)
        self.treeViewProtocols.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.treeViewProtocols.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAsNeeded)
        self.treeViewProtocols.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAsNeeded)
        self.treeViewProtocols.setDragEnabled(True)
        self.treeViewProtocols.setDragDropOverwriteMode(False)
        self.treeViewProtocols.setDragDropMode(QtWidgets.QAbstractItemView.DragDrop)
        self.treeViewProtocols.setDefaultDropAction(QtCore.Qt.IgnoreAction)
        self.treeViewProtocols.setSelectionMode(
            QtWidgets.QAbstractItemView.SingleSelection
        )
        self.treeViewProtocols.setSelectionBehavior(
            QtWidgets.QAbstractItemView.SelectRows
        )
        self.treeViewProtocols.setTextElideMode(QtCore.Qt.ElideRight)
        self.treeViewProtocols.setAnimated(True)
        self.treeViewProtocols.setObjectName("treeViewProtocols")
        self.treeViewProtocols.header().setVisible(False)
        self.treeViewProtocols.header().setCascadingSectionResizes(False)
        self.treeViewProtocols.header().setStretchLastSection(True)
        self.verticalLayout_3.addWidget(self.treeViewProtocols)
        self.tabWidget.addTab(self.tab_protocols, "")
        self.tab_participants = QtWidgets.QWidget()
        self.tab_participants.setObjectName("tab_participants")
        self.verticalLayout_11 = QtWidgets.QVBoxLayout(self.tab_participants)
        self.verticalLayout_11.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_11.setObjectName("verticalLayout_11")
        self.listViewParticipants = QtWidgets.QListView(self.tab_participants)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Expanding
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.listViewParticipants.sizePolicy().hasHeightForWidth()
        )
        self.listViewParticipants.setSizePolicy(sizePolicy)
        self.listViewParticipants.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.listViewParticipants.setTextElideMode(QtCore.Qt.ElideRight)
        self.listViewParticipants.setObjectName("listViewParticipants")
        self.verticalLayout_11.addWidget(self.listViewParticipants)
        self.tabWidget.addTab(self.tab_participants, "")
        self.verticalLayout_2.addWidget(self.tabWidget)
        self.gridLayout_3 = QtWidgets.QGridLayout()
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.label_5 = QtWidgets.QLabel(self.layoutWidget)
        self.label_5.setObjectName("label_5")
        self.gridLayout_3.addWidget(self.label_5, 1, 0, 1, 1)
        self.label_4 = QtWidgets.QLabel(self.layoutWidget)
        self.label_4.setObjectName("label_4")
        self.gridLayout_3.addWidget(self.label_4, 0, 0, 1, 1)
        self.lEncodingErrors = QtWidgets.QLabel(self.layoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.lEncodingErrors.sizePolicy().hasHeightForWidth()
        )
        self.lEncodingErrors.setSizePolicy(sizePolicy)
        self.lEncodingErrors.setObjectName("lEncodingErrors")
        self.gridLayout_3.addWidget(self.lEncodingErrors, 2, 0, 1, 1)
        self.cbDecoding = QtWidgets.QComboBox(self.layoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.cbDecoding.sizePolicy().hasHeightForWidth())
        self.cbDecoding.setSizePolicy(sizePolicy)
        self.cbDecoding.setSizeAdjustPolicy(QtWidgets.QComboBox.AdjustToContents)
        self.cbDecoding.setObjectName("cbDecoding")
        self.cbDecoding.addItem("")
        self.cbDecoding.addItem("")
        self.cbDecoding.addItem("")
        self.cbDecoding.addItem("")
        self.cbDecoding.addItem("")
        self.gridLayout_3.addWidget(self.cbDecoding, 1, 1, 1, 1)
        self.chkBoxShowOnlyDiffs = QtWidgets.QCheckBox(self.layoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.chkBoxShowOnlyDiffs.sizePolicy().hasHeightForWidth()
        )
        self.chkBoxShowOnlyDiffs.setSizePolicy(sizePolicy)
        self.chkBoxShowOnlyDiffs.setObjectName("chkBoxShowOnlyDiffs")
        self.gridLayout_3.addWidget(self.chkBoxShowOnlyDiffs, 4, 0, 1, 2)
        self.cbProtoView = QtWidgets.QComboBox(self.layoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.cbProtoView.sizePolicy().hasHeightForWidth())
        self.cbProtoView.setSizePolicy(sizePolicy)
        self.cbProtoView.setObjectName("cbProtoView")
        self.cbProtoView.addItem("")
        self.cbProtoView.addItem("")
        self.cbProtoView.addItem("")
        self.gridLayout_3.addWidget(self.cbProtoView, 0, 1, 1, 1)
        self.lDecodingErrorsValue = QtWidgets.QLabel(self.layoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.lDecodingErrorsValue.sizePolicy().hasHeightForWidth()
        )
        self.lDecodingErrorsValue.setSizePolicy(sizePolicy)
        self.lDecodingErrorsValue.setObjectName("lDecodingErrorsValue")
        self.gridLayout_3.addWidget(self.lDecodingErrorsValue, 2, 1, 1, 1)
        self.chkBoxOnlyShowLabelsInProtocol = QtWidgets.QCheckBox(self.layoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.chkBoxOnlyShowLabelsInProtocol.sizePolicy().hasHeightForWidth()
        )
        self.chkBoxOnlyShowLabelsInProtocol.setSizePolicy(sizePolicy)
        self.chkBoxOnlyShowLabelsInProtocol.setObjectName(
            "chkBoxOnlyShowLabelsInProtocol"
        )
        self.gridLayout_3.addWidget(self.chkBoxOnlyShowLabelsInProtocol, 5, 0, 1, 2)
        self.cbShowDiffs = QtWidgets.QCheckBox(self.layoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.cbShowDiffs.sizePolicy().hasHeightForWidth())
        self.cbShowDiffs.setSizePolicy(sizePolicy)
        self.cbShowDiffs.setObjectName("cbShowDiffs")
        self.gridLayout_3.addWidget(self.cbShowDiffs, 3, 0, 1, 2)
        self.stackedWidgetLogicAnalysis = QtWidgets.QStackedWidget(self.layoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Maximum
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.stackedWidgetLogicAnalysis.sizePolicy().hasHeightForWidth()
        )
        self.stackedWidgetLogicAnalysis.setSizePolicy(sizePolicy)
        self.stackedWidgetLogicAnalysis.setObjectName("stackedWidgetLogicAnalysis")
        self.pageButtonAnalyzer = QtWidgets.QWidget()
        self.pageButtonAnalyzer.setObjectName("pageButtonAnalyzer")
        self.verticalLayout_8 = QtWidgets.QVBoxLayout(self.pageButtonAnalyzer)
        self.verticalLayout_8.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_8.setSpacing(0)
        self.verticalLayout_8.setObjectName("verticalLayout_8")
        self.btnAnalyze = QtWidgets.QToolButton(self.pageButtonAnalyzer)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.btnAnalyze.sizePolicy().hasHeightForWidth())
        self.btnAnalyze.setSizePolicy(sizePolicy)
        self.btnAnalyze.setPopupMode(QtWidgets.QToolButton.MenuButtonPopup)
        self.btnAnalyze.setToolButtonStyle(QtCore.Qt.ToolButtonTextOnly)
        self.btnAnalyze.setObjectName("btnAnalyze")
        self.verticalLayout_8.addWidget(self.btnAnalyze)
        self.stackedWidgetLogicAnalysis.addWidget(self.pageButtonAnalyzer)
        self.pageProgressBar = QtWidgets.QWidget()
        self.pageProgressBar.setObjectName("pageProgressBar")
        self.verticalLayout_9 = QtWidgets.QVBoxLayout(self.pageProgressBar)
        self.verticalLayout_9.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_9.setSpacing(0)
        self.verticalLayout_9.setObjectName("verticalLayout_9")
        self.progressBarLogicAnalyzer = QtWidgets.QProgressBar(self.pageProgressBar)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.progressBarLogicAnalyzer.sizePolicy().hasHeightForWidth()
        )
        self.progressBarLogicAnalyzer.setSizePolicy(sizePolicy)
        self.progressBarLogicAnalyzer.setProperty("value", 24)
        self.progressBarLogicAnalyzer.setObjectName("progressBarLogicAnalyzer")
        self.verticalLayout_9.addWidget(self.progressBarLogicAnalyzer)
        self.stackedWidgetLogicAnalysis.addWidget(self.pageProgressBar)
        self.gridLayout_3.addWidget(self.stackedWidgetLogicAnalysis, 6, 0, 1, 2)
        self.verticalLayout_2.addLayout(self.gridLayout_3)
        self.layoutWidget1 = QtWidgets.QWidget(self.splitter)
        self.layoutWidget1.setObjectName("layoutWidget1")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.layoutWidget1)
        self.verticalLayout.setContentsMargins(11, 11, 11, 11)
        self.verticalLayout.setObjectName("verticalLayout")
        self.gridLayout_2 = QtWidgets.QGridLayout()
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.btnSaveProto = QtWidgets.QToolButton(self.layoutWidget1)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Preferred
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.btnSaveProto.sizePolicy().hasHeightForWidth())
        self.btnSaveProto.setSizePolicy(sizePolicy)
        self.btnSaveProto.setBaseSize(QtCore.QSize(0, 0))
        self.btnSaveProto.setText("")
        icon = QtGui.QIcon.fromTheme("document-save")
        self.btnSaveProto.setIcon(icon)
        self.btnSaveProto.setToolButtonStyle(QtCore.Qt.ToolButtonIconOnly)
        self.btnSaveProto.setObjectName("btnSaveProto")
        self.gridLayout_2.addWidget(self.btnSaveProto, 0, 16, 1, 1)
        self.lSlash = QtWidgets.QLabel(self.layoutWidget1)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lSlash.sizePolicy().hasHeightForWidth())
        self.lSlash.setSizePolicy(sizePolicy)
        self.lSlash.setAlignment(QtCore.Qt.AlignCenter)
        self.lSlash.setObjectName("lSlash")
        self.gridLayout_2.addWidget(self.lSlash, 0, 7, 1, 1)
        self.lblShownRows = QtWidgets.QLabel(self.layoutWidget1)
        self.lblShownRows.setObjectName("lblShownRows")
        self.gridLayout_2.addWidget(self.lblShownRows, 0, 4, 1, 1)
        self.lTime = QtWidgets.QLabel(self.layoutWidget1)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lTime.sizePolicy().hasHeightForWidth())
        self.lTime.setSizePolicy(sizePolicy)
        self.lTime.setTextFormat(QtCore.Qt.PlainText)
        self.lTime.setAlignment(
            QtCore.Qt.AlignLeading | QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter
        )
        self.lTime.setObjectName("lTime")
        self.gridLayout_2.addWidget(self.lTime, 0, 15, 1, 1)
        self.lSearchCurrent = QtWidgets.QLabel(self.layoutWidget1)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.lSearchCurrent.sizePolicy().hasHeightForWidth()
        )
        self.lSearchCurrent.setSizePolicy(sizePolicy)
        self.lSearchCurrent.setStyleSheet(
            "QLabel\n" "{\n" "    qproperty-alignment: AlignCenter;\n" "}"
        )
        self.lSearchCurrent.setObjectName("lSearchCurrent")
        self.gridLayout_2.addWidget(self.lSearchCurrent, 0, 6, 1, 1)
        self.lblRSSI = QtWidgets.QLabel(self.layoutWidget1)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lblRSSI.sizePolicy().hasHeightForWidth())
        self.lblRSSI.setSizePolicy(sizePolicy)
        self.lblRSSI.setObjectName("lblRSSI")
        self.gridLayout_2.addWidget(self.lblRSSI, 0, 12, 1, 1)
        self.btnNextSearch = QtWidgets.QToolButton(self.layoutWidget1)
        self.btnNextSearch.setEnabled(False)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.btnNextSearch.sizePolicy().hasHeightForWidth()
        )
        self.btnNextSearch.setSizePolicy(sizePolicy)
        icon = QtGui.QIcon.fromTheme("go-next")
        self.btnNextSearch.setIcon(icon)
        self.btnNextSearch.setObjectName("btnNextSearch")
        self.gridLayout_2.addWidget(self.btnNextSearch, 0, 9, 1, 1)
        self.btnPrevSearch = QtWidgets.QToolButton(self.layoutWidget1)
        self.btnPrevSearch.setEnabled(False)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.btnPrevSearch.sizePolicy().hasHeightForWidth()
        )
        self.btnPrevSearch.setSizePolicy(sizePolicy)
        icon = QtGui.QIcon.fromTheme("go-previous")
        self.btnPrevSearch.setIcon(icon)
        self.btnPrevSearch.setObjectName("btnPrevSearch")
        self.gridLayout_2.addWidget(self.btnPrevSearch, 0, 5, 1, 1)
        self.lSearchTotal = QtWidgets.QLabel(self.layoutWidget1)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lSearchTotal.sizePolicy().hasHeightForWidth())
        self.lSearchTotal.setSizePolicy(sizePolicy)
        self.lSearchTotal.setStyleSheet(
            "QLabel\n" "{\n" "    qproperty-alignment: AlignCenter;\n" "}"
        )
        self.lSearchTotal.setObjectName("lSearchTotal")
        self.gridLayout_2.addWidget(self.lSearchTotal, 0, 8, 1, 1)
        self.label_3 = QtWidgets.QLabel(self.layoutWidget1)
        self.label_3.setAlignment(
            QtCore.Qt.AlignRight | QtCore.Qt.AlignTrailing | QtCore.Qt.AlignVCenter
        )
        self.label_3.setObjectName("label_3")
        self.gridLayout_2.addWidget(self.label_3, 0, 14, 1, 1)
        self.line_2 = QtWidgets.QFrame(self.layoutWidget1)
        self.line_2.setFrameShape(QtWidgets.QFrame.VLine)
        self.line_2.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_2.setObjectName("line_2")
        self.gridLayout_2.addWidget(self.line_2, 0, 13, 1, 1)
        self.btnSearchSelectFilter = QtWidgets.QToolButton(self.layoutWidget1)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.btnSearchSelectFilter.sizePolicy().hasHeightForWidth()
        )
        self.btnSearchSelectFilter.setSizePolicy(sizePolicy)
        icon = QtGui.QIcon.fromTheme("edit-find")
        self.btnSearchSelectFilter.setIcon(icon)
        self.btnSearchSelectFilter.setPopupMode(QtWidgets.QToolButton.MenuButtonPopup)
        self.btnSearchSelectFilter.setToolButtonStyle(
            QtCore.Qt.ToolButtonTextBesideIcon
        )
        self.btnSearchSelectFilter.setAutoRaise(False)
        self.btnSearchSelectFilter.setArrowType(QtCore.Qt.NoArrow)
        self.btnSearchSelectFilter.setObjectName("btnSearchSelectFilter")
        self.gridLayout_2.addWidget(self.btnSearchSelectFilter, 0, 2, 1, 1)
        spacerItem = QtWidgets.QSpacerItem(
            60, 0, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum
        )
        self.gridLayout_2.addItem(spacerItem, 0, 10, 1, 1)
        self.line = QtWidgets.QFrame(self.layoutWidget1)
        self.line.setFrameShape(QtWidgets.QFrame.VLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.gridLayout_2.addWidget(self.line, 0, 11, 1, 1)
        self.btnLoadProto = QtWidgets.QToolButton(self.layoutWidget1)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Preferred
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.btnLoadProto.sizePolicy().hasHeightForWidth())
        self.btnLoadProto.setSizePolicy(sizePolicy)
        icon = QtGui.QIcon.fromTheme("document-open")
        self.btnLoadProto.setIcon(icon)
        self.btnLoadProto.setObjectName("btnLoadProto")
        self.gridLayout_2.addWidget(self.btnLoadProto, 0, 17, 1, 1)
        self.lblClearAlignment = QtWidgets.QLabel(self.layoutWidget1)
        self.lblClearAlignment.setObjectName("lblClearAlignment")
        self.gridLayout_2.addWidget(self.lblClearAlignment, 0, 3, 1, 1)
        self.lineEditSearch = QtWidgets.QLineEdit(self.layoutWidget1)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.lineEditSearch.sizePolicy().hasHeightForWidth()
        )
        self.lineEditSearch.setSizePolicy(sizePolicy)
        self.lineEditSearch.setAcceptDrops(False)
        self.lineEditSearch.setClearButtonEnabled(True)
        self.lineEditSearch.setObjectName("lineEditSearch")
        self.gridLayout_2.addWidget(self.lineEditSearch, 0, 1, 1, 1)
        self.verticalLayout.addLayout(self.gridLayout_2)
        self.tblViewProtocol = ProtocolTableView(self.layoutWidget1)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.tblViewProtocol.sizePolicy().hasHeightForWidth()
        )
        self.tblViewProtocol.setSizePolicy(sizePolicy)
        self.tblViewProtocol.setAcceptDrops(True)
        self.tblViewProtocol.setAutoFillBackground(True)
        self.tblViewProtocol.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.tblViewProtocol.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.tblViewProtocol.setLineWidth(1)
        self.tblViewProtocol.setAutoScroll(True)
        self.tblViewProtocol.setDragDropMode(QtWidgets.QAbstractItemView.DropOnly)
        self.tblViewProtocol.setAlternatingRowColors(True)
        self.tblViewProtocol.setSelectionMode(
            QtWidgets.QAbstractItemView.ExtendedSelection
        )
        self.tblViewProtocol.setTextElideMode(QtCore.Qt.ElideNone)
        self.tblViewProtocol.setVerticalScrollMode(
            QtWidgets.QAbstractItemView.ScrollPerPixel
        )
        self.tblViewProtocol.setHorizontalScrollMode(
            QtWidgets.QAbstractItemView.ScrollPerPixel
        )
        self.tblViewProtocol.setShowGrid(False)
        self.tblViewProtocol.setGridStyle(QtCore.Qt.NoPen)
        self.tblViewProtocol.setSortingEnabled(False)
        self.tblViewProtocol.setWordWrap(False)
        self.tblViewProtocol.setCornerButtonEnabled(False)
        self.tblViewProtocol.setObjectName("tblViewProtocol")
        self.tblViewProtocol.horizontalHeader().setDefaultSectionSize(57)
        self.verticalLayout.addWidget(self.tblViewProtocol)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.lBits = QtWidgets.QLabel(self.layoutWidget1)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lBits.sizePolicy().hasHeightForWidth())
        self.lBits.setSizePolicy(sizePolicy)
        self.lBits.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.lBits.setObjectName("lBits")
        self.horizontalLayout_3.addWidget(self.lBits)
        self.lBitsSelection = QtWidgets.QLineEdit(self.layoutWidget1)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.lBitsSelection.sizePolicy().hasHeightForWidth()
        )
        self.lBitsSelection.setSizePolicy(sizePolicy)
        self.lBitsSelection.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.lBitsSelection.setAcceptDrops(False)
        self.lBitsSelection.setStyleSheet("background-color: rgba(255, 255, 255, 0);")
        self.lBitsSelection.setFrame(False)
        self.lBitsSelection.setReadOnly(True)
        self.lBitsSelection.setObjectName("lBitsSelection")
        self.horizontalLayout_3.addWidget(self.lBitsSelection)
        self.lHex = QtWidgets.QLabel(self.layoutWidget1)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lHex.sizePolicy().hasHeightForWidth())
        self.lHex.setSizePolicy(sizePolicy)
        self.lHex.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.lHex.setObjectName("lHex")
        self.horizontalLayout_3.addWidget(self.lHex)
        self.lHexSelection = QtWidgets.QLineEdit(self.layoutWidget1)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.lHexSelection.sizePolicy().hasHeightForWidth()
        )
        self.lHexSelection.setSizePolicy(sizePolicy)
        self.lHexSelection.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.lHexSelection.setAcceptDrops(False)
        self.lHexSelection.setStyleSheet("background-color: rgba(255, 255, 255, 0);")
        self.lHexSelection.setFrame(False)
        self.lHexSelection.setReadOnly(True)
        self.lHexSelection.setObjectName("lHexSelection")
        self.horizontalLayout_3.addWidget(self.lHexSelection)
        self.lDecimal = QtWidgets.QLabel(self.layoutWidget1)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lDecimal.sizePolicy().hasHeightForWidth())
        self.lDecimal.setSizePolicy(sizePolicy)
        self.lDecimal.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.lDecimal.setObjectName("lDecimal")
        self.horizontalLayout_3.addWidget(self.lDecimal)
        self.lDecimalSelection = QtWidgets.QLineEdit(self.layoutWidget1)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.lDecimalSelection.sizePolicy().hasHeightForWidth()
        )
        self.lDecimalSelection.setSizePolicy(sizePolicy)
        self.lDecimalSelection.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.lDecimalSelection.setAcceptDrops(False)
        self.lDecimalSelection.setStyleSheet(
            "background-color: rgba(255, 255, 255, 0);"
        )
        self.lDecimalSelection.setFrame(False)
        self.lDecimalSelection.setReadOnly(True)
        self.lDecimalSelection.setObjectName("lDecimalSelection")
        self.horizontalLayout_3.addWidget(self.lDecimalSelection)
        self.lNumSelectedColumns = QtWidgets.QLabel(self.layoutWidget1)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.lNumSelectedColumns.sizePolicy().hasHeightForWidth()
        )
        self.lNumSelectedColumns.setSizePolicy(sizePolicy)
        self.lNumSelectedColumns.setAlignment(
            QtCore.Qt.AlignRight | QtCore.Qt.AlignTrailing | QtCore.Qt.AlignVCenter
        )
        self.lNumSelectedColumns.setObjectName("lNumSelectedColumns")
        self.horizontalLayout_3.addWidget(self.lNumSelectedColumns)
        self.lColumnsSelectedText = QtWidgets.QLabel(self.layoutWidget1)
        self.lColumnsSelectedText.setObjectName("lColumnsSelectedText")
        self.horizontalLayout_3.addWidget(self.lColumnsSelectedText)
        self.verticalLayout.addLayout(self.horizontalLayout_3)
        self.layoutWidget2 = QtWidgets.QWidget(self.splitter_2)
        self.layoutWidget2.setObjectName("layoutWidget2")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout(self.layoutWidget2)
        self.verticalLayout_4.setContentsMargins(11, 11, 11, 11)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.label = QtWidgets.QLabel(self.layoutWidget2)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label.sizePolicy().hasHeightForWidth())
        self.label.setSizePolicy(sizePolicy)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)
        self.lblLabelValues = QtWidgets.QLabel(self.layoutWidget2)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.lblLabelValues.sizePolicy().hasHeightForWidth()
        )
        self.lblLabelValues.setSizePolicy(sizePolicy)
        self.lblLabelValues.setAlignment(QtCore.Qt.AlignCenter)
        self.lblLabelValues.setObjectName("lblLabelValues")
        self.gridLayout.addWidget(self.lblLabelValues, 0, 1, 1, 1)
        self.btnAddMessagetype = QtWidgets.QToolButton(self.layoutWidget2)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.btnAddMessagetype.sizePolicy().hasHeightForWidth()
        )
        self.btnAddMessagetype.setSizePolicy(sizePolicy)
        icon = QtGui.QIcon.fromTheme("list-add")
        self.btnAddMessagetype.setIcon(icon)
        self.btnAddMessagetype.setToolButtonStyle(QtCore.Qt.ToolButtonTextBesideIcon)
        self.btnAddMessagetype.setObjectName("btnAddMessagetype")
        self.gridLayout.addWidget(self.btnAddMessagetype, 3, 0, 1, 1)
        self.tblLabelValues = LabelValueTableView(self.layoutWidget2)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.tblLabelValues.sizePolicy().hasHeightForWidth()
        )
        self.tblLabelValues.setSizePolicy(sizePolicy)
        self.tblLabelValues.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.tblLabelValues.setAlternatingRowColors(True)
        self.tblLabelValues.setShowGrid(False)
        self.tblLabelValues.setObjectName("tblLabelValues")
        self.tblLabelValues.horizontalHeader().setVisible(True)
        self.tblLabelValues.horizontalHeader().setCascadingSectionResizes(False)
        self.tblLabelValues.horizontalHeader().setDefaultSectionSize(150)
        self.tblLabelValues.horizontalHeader().setStretchLastSection(True)
        self.tblLabelValues.verticalHeader().setVisible(False)
        self.gridLayout.addWidget(self.tblLabelValues, 1, 1, 3, 1)
        self.tblViewMessageTypes = MessageTypeTableView(self.layoutWidget2)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.tblViewMessageTypes.sizePolicy().hasHeightForWidth()
        )
        self.tblViewMessageTypes.setSizePolicy(sizePolicy)
        self.tblViewMessageTypes.setAcceptDrops(False)
        self.tblViewMessageTypes.setToolTip("")
        self.tblViewMessageTypes.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.tblViewMessageTypes.setAlternatingRowColors(True)
        self.tblViewMessageTypes.setShowGrid(False)
        self.tblViewMessageTypes.setObjectName("tblViewMessageTypes")
        self.tblViewMessageTypes.verticalHeader().setVisible(False)
        self.gridLayout.addWidget(self.tblViewMessageTypes, 1, 0, 2, 1)
        self.verticalLayout_4.addLayout(self.gridLayout)
        self.verticalLayout_5.addWidget(self.splitter_2)
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)
        self.verticalLayout_7.addWidget(self.scrollArea)

        self.retranslateUi(TabAnalysis)
        self.tabWidget.setCurrentIndex(0)
        self.stackedWidgetLogicAnalysis.setCurrentIndex(0)

    def retranslateUi(self, TabAnalysis):
        _translate = QtCore.QCoreApplication.translate
        TabAnalysis.setWindowTitle(_translate("TabAnalysis", "Frame"))
        self.tabWidget.setTabText(
            self.tabWidget.indexOf(self.tab_protocols),
            _translate("TabAnalysis", "Protocols"),
        )
        self.tabWidget.setTabText(
            self.tabWidget.indexOf(self.tab_participants),
            _translate("TabAnalysis", "Participants"),
        )
        self.label_5.setText(_translate("TabAnalysis", "Decoding:"))
        self.label_4.setText(_translate("TabAnalysis", "View data as:"))
        self.lEncodingErrors.setText(_translate("TabAnalysis", "Decoding errors:"))
        self.cbDecoding.setItemText(0, _translate("TabAnalysis", "NRZ"))
        self.cbDecoding.setItemText(1, _translate("TabAnalysis", "Manchester"))
        self.cbDecoding.setItemText(2, _translate("TabAnalysis", "Manchester II"))
        self.cbDecoding.setItemText(
            3, _translate("TabAnalysis", "Differential Manchester")
        )
        self.cbDecoding.setItemText(4, _translate("TabAnalysis", "..."))
        self.chkBoxShowOnlyDiffs.setText(
            _translate("TabAnalysis", "Show only diffs in protocol")
        )
        self.cbProtoView.setToolTip(
            _translate(
                "TabAnalysis",
                "<html><head/><body><p>Set the desired view here.</p></body></html>",
            )
        )
        self.cbProtoView.setItemText(0, _translate("TabAnalysis", "Bits"))
        self.cbProtoView.setItemText(1, _translate("TabAnalysis", "Hex"))
        self.cbProtoView.setItemText(2, _translate("TabAnalysis", "ASCII"))
        self.lDecodingErrorsValue.setText(_translate("TabAnalysis", "0 (0.00%)"))
        self.chkBoxOnlyShowLabelsInProtocol.setText(
            _translate("TabAnalysis", "Show only labels in protocol")
        )
        self.cbShowDiffs.setText(_translate("TabAnalysis", "Mark diffs in protocol"))
        self.btnAnalyze.setToolTip(
            _translate(
                "TabAnalysis",
                "<html><head/><body><p>Run some automatic analysis on the protocol e.g. assign labels automatically. You can configure which checks to run with the arrow on the right of this button.</p></body></html>",
            )
        )
        self.btnAnalyze.setText(_translate("TabAnalysis", "Analyze Protocol"))
        self.btnSaveProto.setToolTip(
            _translate("TabAnalysis", "Save current protocol.")
        )
        self.lSlash.setText(_translate("TabAnalysis", "/"))
        self.lblShownRows.setText(_translate("TabAnalysis", "shown: 42/108"))
        self.lTime.setToolTip(
            _translate(
                "TabAnalysis",
                '<html><head/><body><p>The <span style=" font-weight:600;">Message</span><span style=" font-weight:600;">Start</span> is the point in time when a protocol message begins. Additionally the relative time (+ ...) from the previous message is shown.</p></body></html>',
            )
        )
        self.lTime.setText(_translate("TabAnalysis", "0 (+0)"))
        self.lSearchCurrent.setText(_translate("TabAnalysis", "-"))
        self.lblRSSI.setToolTip(
            _translate(
                "TabAnalysis",
                "<html><head/><body><p>This is the average signal power of the current message. The nearer this value is to zero, the stronger the signal is.</p></body></html>",
            )
        )
        self.lblRSSI.setText(_translate("TabAnalysis", "-∞ dBm"))
        self.btnNextSearch.setText(_translate("TabAnalysis", ">"))
        self.btnPrevSearch.setText(_translate("TabAnalysis", "<"))
        self.lSearchTotal.setText(_translate("TabAnalysis", "-"))
        self.label_3.setToolTip(
            _translate(
                "TabAnalysis",
                '<html><head/><body><p>The <span style=" font-weight:600;">Message Start</span> is the point in time when a protocol message begins. Additionally the relative time (+ ...) from the previous message is shown.</p></body></html>',
            )
        )
        self.label_3.setText(_translate("TabAnalysis", "Timestamp:"))
        self.btnSearchSelectFilter.setText(_translate("TabAnalysis", "Search"))
        self.btnLoadProto.setToolTip(_translate("TabAnalysis", "Load a protocol."))
        self.btnLoadProto.setText(_translate("TabAnalysis", "..."))
        self.lblClearAlignment.setText(
            _translate(
                "TabAnalysis",
                '<html><head/><body><p><a href="reset_alignment"><span style=" text-decoration: underline; color:#0000ff;">Reset alignment</span></a></p></body></html>',
            )
        )
        self.lineEditSearch.setPlaceholderText(
            _translate("TabAnalysis", "Enter pattern here")
        )
        self.lBits.setText(_translate("TabAnalysis", "Bit:"))
        self.lHex.setText(_translate("TabAnalysis", "Hex:"))
        self.lDecimal.setText(_translate("TabAnalysis", "Decimal:"))
        self.lNumSelectedColumns.setText(_translate("TabAnalysis", "0"))
        self.lColumnsSelectedText.setText(
            _translate("TabAnalysis", "column(s) selected")
        )
        self.label.setText(_translate("TabAnalysis", "Message types"))
        self.lblLabelValues.setText(_translate("TabAnalysis", "Labels for message"))
        self.btnAddMessagetype.setToolTip(
            _translate("TabAnalysis", "Add a new message type")
        )
        self.btnAddMessagetype.setText(
            _translate("TabAnalysis", "Add new message type")
        )


from urh.ui.views.LabelValueTableView import LabelValueTableView
from urh.ui.views.MessageTypeTableView import MessageTypeTableView
from urh.ui.views.ProtocolTableView import ProtocolTableView
from urh.ui.views.ProtocolTreeView import ProtocolTreeView
from . import urh_rc
