# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'mainWidget.ui'
##
## Created by: Qt User Interface Compiler version 6.6.1
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QAbstractScrollArea, QApplication, QCheckBox, QFrame,
    QHBoxLayout, QListView, QListWidget, QListWidgetItem,
    QPushButton, QSizePolicy, QTabWidget, QTextEdit,
    QWidget)

class Ui_Form(object):
    def setupUi(self, Form):
        if not Form.objectName():
            Form.setObjectName(u"Form")
        Form.resize(472, 555)
        Form.setAcceptDrops(True)
        self.tabWidget = QTabWidget(Form)
        self.tabWidget.setObjectName(u"tabWidget")
        self.tabWidget.setGeometry(QRect(0, 0, 471, 551))
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tabWidget.sizePolicy().hasHeightForWidth())
        self.tabWidget.setSizePolicy(sizePolicy)
        self.tab_3 = QWidget()
        self.tab_3.setObjectName(u"tab_3")
        self.listWidget_files = QListWidget(self.tab_3)
        self.listWidget_files.setObjectName(u"listWidget_files")
        self.listWidget_files.setGeometry(QRect(120, 10, 256, 81))
        sizePolicy.setHeightForWidth(self.listWidget_files.sizePolicy().hasHeightForWidth())
        self.listWidget_files.setSizePolicy(sizePolicy)
        self.listWidget_files.setMinimumSize(QSize(0, 1))
        self.listWidget_files.setBaseSize(QSize(0, 0))
        self.listWidget_files.setFrameShape(QFrame.StyledPanel)
        self.listWidget_files.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)
        self.listWidget_files.setResizeMode(QListView.Adjust)
        self.listWidget_files.setViewMode(QListView.ListMode)
        self.pushButton_select_file = QPushButton(self.tab_3)
        self.pushButton_select_file.setObjectName(u"pushButton_select_file")
        self.pushButton_select_file.setGeometry(QRect(10, 20, 101, 24))
        self.pushButton_process = QPushButton(self.tab_3)
        self.pushButton_process.setObjectName(u"pushButton_process")
        self.pushButton_process.setGeometry(QRect(10, 50, 101, 24))
        self.checkBox_open_folder = QCheckBox(self.tab_3)
        self.checkBox_open_folder.setObjectName(u"checkBox_open_folder")
        self.checkBox_open_folder.setGeometry(QRect(270, 400, 121, 31))
        self.checkBox_open_folder.setChecked(True)
        self.textEdit_output = QTextEdit(self.tab_3)
        self.textEdit_output.setObjectName(u"textEdit_output")
        self.textEdit_output.setGeometry(QRect(120, 100, 261, 291))
        self.textEdit_output.setAcceptDrops(False)
        self.textEdit_output.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)
        self.textEdit_output.setLineWrapMode(QTextEdit.NoWrap)
        self.tabWidget.addTab(self.tab_3, "")
        self.tab_4 = QWidget()
        self.tab_4.setObjectName(u"tab_4")
        self.pushButton_generate_components = QPushButton(self.tab_4)
        self.pushButton_generate_components.setObjectName(u"pushButton_generate_components")
        self.pushButton_generate_components.setGeometry(QRect(120, 10, 171, 31))
        self.pushButton_generate_components.setLayoutDirection(Qt.LeftToRight)
        self.textEdit_output_comp = QTextEdit(self.tab_4)
        self.textEdit_output_comp.setObjectName(u"textEdit_output_comp")
        self.textEdit_output_comp.setGeometry(QRect(10, 50, 441, 231))
        self.textEdit_output_comp.setAcceptDrops(False)
        self.textEdit_output_comp.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)
        self.textEdit_output_comp.setLineWrapMode(QTextEdit.NoWrap)
        self.tabWidget.addTab(self.tab_4, "")
        self.tab_debug = QWidget()
        self.tab_debug.setObjectName(u"tab_debug")
        self.horizontalLayoutWidget = QWidget(self.tab_debug)
        self.horizontalLayoutWidget.setObjectName(u"horizontalLayoutWidget")
        self.horizontalLayoutWidget.setGeometry(QRect(9, 69, 451, 451))
        self.horizontalLayout = QHBoxLayout(self.horizontalLayoutWidget)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.textEdit_stdout = QTextEdit(self.horizontalLayoutWidget)
        self.textEdit_stdout.setObjectName(u"textEdit_stdout")

        self.horizontalLayout.addWidget(self.textEdit_stdout)

        self.textEdit_stderr = QTextEdit(self.horizontalLayoutWidget)
        self.textEdit_stderr.setObjectName(u"textEdit_stderr")

        self.horizontalLayout.addWidget(self.textEdit_stderr)

        self.tabWidget.addTab(self.tab_debug, "")
        self.pushButton_debug = QPushButton(Form)
        self.pushButton_debug.setObjectName(u"pushButton_debug")
        self.pushButton_debug.setGeometry(QRect(520, 30, 75, 24))

        self.retranslateUi(Form)

        self.tabWidget.setCurrentIndex(2)


        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"\u041f\u0440\u0435\u043e\u0431\u0440\u0430\u0437\u043e\u0432\u0430\u0442\u0435\u043b\u044c PnP", None))
        self.pushButton_select_file.setText(QCoreApplication.translate("Form", u"\u0412\u044b\u0431\u0440\u0430\u0442\u044c \u0444\u0430\u0439\u043b\u044b", None))
        self.pushButton_process.setText(QCoreApplication.translate("Form", u"\u041e\u0431\u0440\u0430\u0431\u043e\u0442\u0430\u0442\u044c", None))
        self.checkBox_open_folder.setText(QCoreApplication.translate("Form", u"\u041e\u0442\u043a\u0440\u044b\u0432\u0430\u0442\u044c \u043f\u0430\u043f\u043a\u0443", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_3), QCoreApplication.translate("Form", u"PnP", None))
        self.pushButton_generate_components.setText(QCoreApplication.translate("Form", u"\u0421\u0433\u0435\u043d\u0435\u0440\u0438\u0440\u043e\u0432\u0430\u0442\u044c \u043a\u043e\u043c\u043f\u043e\u043d\u0435\u043d\u0442\u044b", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_4), QCoreApplication.translate("Form", u"\u041a\u043e\u043c\u043f\u043e\u043d\u0435\u043d\u0442\u044b", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_debug), QCoreApplication.translate("Form", u"DEBUG", None))
        self.pushButton_debug.setText(QCoreApplication.translate("Form", u"DEBUG", None))
    # retranslateUi

