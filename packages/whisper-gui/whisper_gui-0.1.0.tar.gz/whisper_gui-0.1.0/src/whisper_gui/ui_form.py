# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'form.ui'
##
## Created by: Qt User Interface Compiler version 6.8.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QAction, QBrush, QColor, QConicalGradient,
    QCursor, QFont, QFontDatabase, QGradient,
    QIcon, QImage, QKeySequence, QLinearGradient,
    QPainter, QPalette, QPixmap, QRadialGradient,
    QTransform)
from PySide6.QtWidgets import (QApplication, QComboBox, QFormLayout, QGridLayout,
    QHBoxLayout, QLabel, QLineEdit, QMainWindow,
    QMenu, QMenuBar, QPlainTextEdit, QPushButton,
    QScrollArea, QSizePolicy, QSpacerItem, QStatusBar,
    QTabWidget, QToolButton, QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(800, 600)
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(MainWindow.sizePolicy().hasHeightForWidth())
        MainWindow.setSizePolicy(sizePolicy)
        self.actionOpen = QAction(MainWindow)
        self.actionOpen.setObjectName(u"actionOpen")
        self.actionSave = QAction(MainWindow)
        self.actionSave.setObjectName(u"actionSave")
        self.actionQuit = QAction(MainWindow)
        self.actionQuit.setObjectName(u"actionQuit")
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        sizePolicy.setHeightForWidth(self.centralwidget.sizePolicy().hasHeightForWidth())
        self.centralwidget.setSizePolicy(sizePolicy)
        self.gridLayout_4 = QGridLayout(self.centralwidget)
        self.gridLayout_4.setObjectName(u"gridLayout_4")
        self.horizontalLayout_5 = QHBoxLayout()
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.widget = QWidget(self.centralwidget)
        self.widget.setObjectName(u"widget")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Preferred)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.widget.sizePolicy().hasHeightForWidth())
        self.widget.setSizePolicy(sizePolicy1)
        self.formLayout = QFormLayout(self.widget)
        self.formLayout.setObjectName(u"formLayout")
        self.label = QLabel(self.widget)
        self.label.setObjectName(u"label")

        self.formLayout.setWidget(0, QFormLayout.LabelRole, self.label)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.txtVideo = QLineEdit(self.widget)
        self.txtVideo.setObjectName(u"txtVideo")

        self.horizontalLayout.addWidget(self.txtVideo)

        self.cmdOpenVideo = QToolButton(self.widget)
        self.cmdOpenVideo.setObjectName(u"cmdOpenVideo")

        self.horizontalLayout.addWidget(self.cmdOpenVideo)


        self.formLayout.setLayout(0, QFormLayout.FieldRole, self.horizontalLayout)

        self.label_2 = QLabel(self.widget)
        self.label_2.setObjectName(u"label_2")

        self.formLayout.setWidget(1, QFormLayout.LabelRole, self.label_2)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.txtAudio = QLineEdit(self.widget)
        self.txtAudio.setObjectName(u"txtAudio")

        self.horizontalLayout_2.addWidget(self.txtAudio)

        self.cmdOpenAudio = QToolButton(self.widget)
        self.cmdOpenAudio.setObjectName(u"cmdOpenAudio")

        self.horizontalLayout_2.addWidget(self.cmdOpenAudio)


        self.formLayout.setLayout(1, QFormLayout.FieldRole, self.horizontalLayout_2)

        self.label_OutDir = QLabel(self.widget)
        self.label_OutDir.setObjectName(u"label_OutDir")

        self.formLayout.setWidget(2, QFormLayout.LabelRole, self.label_OutDir)

        self.horizontalLayout_OutDir = QHBoxLayout()
        self.horizontalLayout_OutDir.setObjectName(u"horizontalLayout_OutDir")
        self.txtOutputDir = QLineEdit(self.widget)
        self.txtOutputDir.setObjectName(u"txtOutputDir")

        self.horizontalLayout_OutDir.addWidget(self.txtOutputDir)

        self.cmdOpenOutputDir = QToolButton(self.widget)
        self.cmdOpenOutputDir.setObjectName(u"cmdOpenOutputDir")

        self.horizontalLayout_OutDir.addWidget(self.cmdOpenOutputDir)


        self.formLayout.setLayout(2, QFormLayout.FieldRole, self.horizontalLayout_OutDir)

        self.label_Model = QLabel(self.widget)
        self.label_Model.setObjectName(u"label_Model")

        self.formLayout.setWidget(3, QFormLayout.LabelRole, self.label_Model)

        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.cmbModel = QComboBox(self.widget)
        self.cmbModel.addItem("")
        self.cmbModel.addItem("")
        self.cmbModel.addItem("")
        self.cmbModel.addItem("")
        self.cmbModel.setObjectName(u"cmbModel")

        self.horizontalLayout_3.addWidget(self.cmbModel)


        self.formLayout.setLayout(3, QFormLayout.FieldRole, self.horizontalLayout_3)

        self.horizontalLayout_4 = QHBoxLayout()
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.cmbLanguage = QComboBox(self.widget)
        self.cmbLanguage.addItem("")
        self.cmbLanguage.addItem("")
        self.cmbLanguage.setObjectName(u"cmbLanguage")

        self.horizontalLayout_4.addWidget(self.cmbLanguage)


        self.formLayout.setLayout(4, QFormLayout.FieldRole, self.horizontalLayout_4)

        self.label_3 = QLabel(self.widget)
        self.label_3.setObjectName(u"label_3")

        self.formLayout.setWidget(4, QFormLayout.LabelRole, self.label_3)

        self.cmdConvertAudio = QPushButton(self.widget)
        self.cmdConvertAudio.setObjectName(u"cmdConvertAudio")

        self.formLayout.setWidget(6, QFormLayout.FieldRole, self.cmdConvertAudio)

        self.cmdTranscribe = QPushButton(self.widget)
        self.cmdTranscribe.setObjectName(u"cmdTranscribe")

        self.formLayout.setWidget(7, QFormLayout.FieldRole, self.cmdTranscribe)

        self.cmdTerminate = QPushButton(self.widget)
        self.cmdTerminate.setObjectName(u"cmdTerminate")
        self.cmdTerminate.setEnabled(False)

        self.formLayout.setWidget(8, QFormLayout.FieldRole, self.cmdTerminate)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.formLayout.setItem(9, QFormLayout.FieldRole, self.verticalSpacer)


        self.horizontalLayout_5.addWidget(self.widget)

        self.widget_2 = QWidget(self.centralwidget)
        self.widget_2.setObjectName(u"widget_2")
        self.gridLayout_3 = QGridLayout(self.widget_2)
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.gridLayout_3.setContentsMargins(0, 0, 0, 0)
        self.tabWidget = QTabWidget(self.widget_2)
        self.tabWidget.setObjectName(u"tabWidget")
        self.tabOutput = QWidget()
        self.tabOutput.setObjectName(u"tabOutput")
        self.gridLayout_2 = QGridLayout(self.tabOutput)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.gridLayout_2.setContentsMargins(0, 0, 0, 0)
        self.scrollArea = QScrollArea(self.tabOutput)
        self.scrollArea.setObjectName(u"scrollArea")
        self.scrollArea.setWidgetResizable(True)
        self.scrollAreaWidgetContents = QWidget()
        self.scrollAreaWidgetContents.setObjectName(u"scrollAreaWidgetContents")
        self.scrollAreaWidgetContents.setGeometry(QRect(0, 0, 502, 480))
        self.gridLayout = QGridLayout(self.scrollAreaWidgetContents)
        self.gridLayout.setObjectName(u"gridLayout")
        self.txtOutput = QPlainTextEdit(self.scrollAreaWidgetContents)
        self.txtOutput.setObjectName(u"txtOutput")

        self.gridLayout.addWidget(self.txtOutput, 0, 0, 1, 1)

        self.scrollArea.setWidget(self.scrollAreaWidgetContents)

        self.gridLayout_2.addWidget(self.scrollArea, 0, 0, 1, 1)

        self.tabWidget.addTab(self.tabOutput, "")
        self.tabTxt = QWidget()
        self.tabTxt.setObjectName(u"tabTxt")
        self.gridLayout_2txt = QGridLayout(self.tabTxt)
        self.gridLayout_2txt.setObjectName(u"gridLayout_2txt")
        self.gridLayout_2txt.setContentsMargins(0, 0, 0, 0)
        self.scrollAreatxt = QScrollArea(self.tabTxt)
        self.scrollAreatxt.setObjectName(u"scrollAreatxt")
        self.scrollAreatxt.setWidgetResizable(True)
        self.scrollAreaWidgetContentstxt = QWidget()
        self.scrollAreaWidgetContentstxt.setObjectName(u"scrollAreaWidgetContentstxt")
        self.scrollAreaWidgetContentstxt.setGeometry(QRect(0, 0, 502, 480))
        self.gridLayouttxt = QGridLayout(self.scrollAreaWidgetContentstxt)
        self.gridLayouttxt.setObjectName(u"gridLayouttxt")
        self.txtText = QPlainTextEdit(self.scrollAreaWidgetContentstxt)
        self.txtText.setObjectName(u"txtText")

        self.gridLayouttxt.addWidget(self.txtText, 0, 0, 1, 1)

        self.scrollAreatxt.setWidget(self.scrollAreaWidgetContentstxt)

        self.gridLayout_2txt.addWidget(self.scrollAreatxt, 0, 0, 1, 1)

        self.tabWidget.addTab(self.tabTxt, "")

        self.gridLayout_3.addWidget(self.tabWidget, 0, 0, 1, 1)


        self.horizontalLayout_5.addWidget(self.widget_2)


        self.gridLayout_4.addLayout(self.horizontalLayout_5, 0, 0, 1, 1)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 800, 36))
        self.menuFile = QMenu(self.menubar)
        self.menuFile.setObjectName(u"menuFile")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.menubar.addAction(self.menuFile.menuAction())
        self.menuFile.addAction(self.actionOpen)
        self.menuFile.addAction(self.actionSave)
        self.menuFile.addAction(self.actionQuit)

        self.retranslateUi(MainWindow)
        self.actionOpen.triggered.connect(MainWindow.slotOpen)
        self.cmdOpenAudio.clicked.connect(MainWindow.slotOpenAudio)
        self.cmdOpenVideo.clicked.connect(MainWindow.slotOpenVideo)
        self.cmdConvertAudio.clicked.connect(MainWindow.slotConvertAudio)
        self.cmdTranscribe.clicked.connect(MainWindow.slotTranscribe)
        self.cmdOpenOutputDir.clicked.connect(MainWindow.slotOpenOutputDir)
        self.cmdTerminate.clicked.connect(MainWindow.slotTerminate)
        self.actionQuit.triggered.connect(MainWindow.close)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"Whisper GUI", None))
        self.actionOpen.setText(QCoreApplication.translate("MainWindow", u"Open", None))
#if QT_CONFIG(shortcut)
        self.actionOpen.setShortcut(QCoreApplication.translate("MainWindow", u"Ctrl+O", None))
#endif // QT_CONFIG(shortcut)
        self.actionSave.setText(QCoreApplication.translate("MainWindow", u"Save", None))
#if QT_CONFIG(shortcut)
        self.actionSave.setShortcut(QCoreApplication.translate("MainWindow", u"Ctrl+S", None))
#endif // QT_CONFIG(shortcut)
        self.actionQuit.setText(QCoreApplication.translate("MainWindow", u"Quit", None))
#if QT_CONFIG(shortcut)
        self.actionQuit.setShortcut(QCoreApplication.translate("MainWindow", u"Ctrl+Q", None))
#endif // QT_CONFIG(shortcut)
        self.label.setText(QCoreApplication.translate("MainWindow", u"Video", None))
        self.cmdOpenVideo.setText(QCoreApplication.translate("MainWindow", u"...", None))
        self.label_2.setText(QCoreApplication.translate("MainWindow", u"Audio", None))
        self.cmdOpenAudio.setText(QCoreApplication.translate("MainWindow", u"...", None))
        self.label_OutDir.setText(QCoreApplication.translate("MainWindow", u"Output Dir", None))
        self.cmdOpenOutputDir.setText(QCoreApplication.translate("MainWindow", u"...", None))
        self.label_Model.setText(QCoreApplication.translate("MainWindow", u"Model", None))
        self.cmbModel.setItemText(0, QCoreApplication.translate("MainWindow", u"tiny", None))
        self.cmbModel.setItemText(1, QCoreApplication.translate("MainWindow", u"medium", None))
        self.cmbModel.setItemText(2, QCoreApplication.translate("MainWindow", u"large", None))
        self.cmbModel.setItemText(3, QCoreApplication.translate("MainWindow", u"small", None))

        self.cmbLanguage.setItemText(0, QCoreApplication.translate("MainWindow", u"German", None))
        self.cmbLanguage.setItemText(1, QCoreApplication.translate("MainWindow", u"English", None))

        self.label_3.setText(QCoreApplication.translate("MainWindow", u"Language", None))
        self.cmdConvertAudio.setText(QCoreApplication.translate("MainWindow", u"Convert Audio", None))
        self.cmdTranscribe.setText(QCoreApplication.translate("MainWindow", u"Transcribe", None))
        self.cmdTerminate.setText(QCoreApplication.translate("MainWindow", u"Terminate", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tabOutput), QCoreApplication.translate("MainWindow", u"Output", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tabTxt), QCoreApplication.translate("MainWindow", u"Txt", None))
        self.menuFile.setTitle(QCoreApplication.translate("MainWindow", u"File", None))
    # retranslateUi

