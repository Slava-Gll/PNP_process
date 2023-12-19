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
from PySide6.QtWidgets import (QAbstractScrollArea, QApplication, QFrame, QListView,
    QListWidget, QListWidgetItem, QPushButton, QSizePolicy,
    QTextEdit, QWidget)

class Ui_Form(object):
    def setupUi(self, Form):
        if not Form.objectName():
            Form.setObjectName(u"Form")
        Form.resize(548, 492)
        self.pushButton_select_file = QPushButton(Form)
        self.pushButton_select_file.setObjectName(u"pushButton_select_file")
        self.pushButton_select_file.setGeometry(QRect(10, 10, 91, 24))
        self.listWidget_files = QListWidget(Form)
        self.listWidget_files.setObjectName(u"listWidget_files")
        self.listWidget_files.setGeometry(QRect(110, 10, 256, 81))
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.listWidget_files.sizePolicy().hasHeightForWidth())
        self.listWidget_files.setSizePolicy(sizePolicy)
        self.listWidget_files.setMinimumSize(QSize(0, 1))
        self.listWidget_files.setBaseSize(QSize(0, 0))
        self.listWidget_files.setFrameShape(QFrame.StyledPanel)
        self.listWidget_files.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)
        self.listWidget_files.setResizeMode(QListView.Adjust)
        self.listWidget_files.setViewMode(QListView.ListMode)
        self.textEdit_output = QTextEdit(Form)
        self.textEdit_output.setObjectName(u"textEdit_output")
        self.textEdit_output.setGeometry(QRect(20, 130, 441, 301))
        self.pushButton_process = QPushButton(Form)
        self.pushButton_process.setObjectName(u"pushButton_process")
        self.pushButton_process.setGeometry(QRect(260, 450, 75, 24))

        self.retranslateUi(Form)

        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"\u041f\u0440\u0435\u043e\u0431\u0440\u0430\u0437\u043e\u0432\u0430\u0442\u0435\u043b\u044c PnP", None))
        self.pushButton_select_file.setText(QCoreApplication.translate("Form", u"\u0412\u044b\u0431\u0440\u0430\u0442\u044c \u0444\u0430\u0439\u043b", None))
        self.pushButton_process.setText(QCoreApplication.translate("Form", u"\u041e\u0431\u0440\u0430\u0431\u043e\u0442\u0430\u0442\u044c", None))
    # retranslateUi

