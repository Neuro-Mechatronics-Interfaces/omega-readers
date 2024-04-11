# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'dialog_connect.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *


class Ui_DialogConnect(object):
    def setupUi(self, DialogConnect):
        if not DialogConnect.objectName():
            DialogConnect.setObjectName(u"DialogConnect")
        DialogConnect.resize(720, 227)
        self.centralwidget = QWidget(DialogConnect)
        self.centralwidget.setObjectName(u"centralwidget")
        self.horizontalLayout = QHBoxLayout(self.centralwidget)
        self.horizontalLayout.setSpacing(6)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(9, 9, 9, 9)
        self.gb_available_dongles = QGroupBox(self.centralwidget)
        self.gb_available_dongles.setObjectName(u"gb_available_dongles")
        self.verticalLayout_2 = QVBoxLayout(self.gb_available_dongles)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.list_av_dongles = QListWidget(self.gb_available_dongles)
        self.list_av_dongles.setObjectName(u"list_av_dongles")

        self.verticalLayout_2.addWidget(self.list_av_dongles)


        self.horizontalLayout.addWidget(self.gb_available_dongles)

        self.gb_available_devs = QGroupBox(self.centralwidget)
        self.gb_available_devs.setObjectName(u"gb_available_devs")
        self.verticalLayout_4 = QVBoxLayout(self.gb_available_devs)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.list_av_devs = QListWidget(self.gb_available_devs)
        self.list_av_devs.setObjectName(u"list_av_devs")

        self.verticalLayout_4.addWidget(self.list_av_devs)


        self.horizontalLayout.addWidget(self.gb_available_devs)

        self.gb_group = QGroupBox(self.centralwidget)
        self.gb_group.setObjectName(u"gb_group")
        self.verticalLayout_3 = QVBoxLayout(self.gb_group)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.list_group = QListWidget(self.gb_group)
        self.list_group.setObjectName(u"list_group")

        self.verticalLayout_3.addWidget(self.list_group)


        self.horizontalLayout.addWidget(self.gb_group)

        self.frame_control_connect = QFrame(self.centralwidget)
        self.frame_control_connect.setObjectName(u"frame_control_connect")
        self.frame_control_connect.setMaximumSize(QSize(100, 16777215))
        self.frame_control_connect.setFrameShape(QFrame.StyledPanel)
        self.frame_control_connect.setFrameShadow(QFrame.Raised)
        self.verticalLayout = QVBoxLayout(self.frame_control_connect)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.btn_connect = QPushButton(self.frame_control_connect)
        self.btn_connect.setObjectName(u"btn_connect")

        self.verticalLayout.addWidget(self.btn_connect)

        self.btn_pair = QPushButton(self.frame_control_connect)
        self.btn_pair.setObjectName(u"btn_pair")

        self.verticalLayout.addWidget(self.btn_pair)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout.addItem(self.verticalSpacer)

        self.btn_search_again = QPushButton(self.frame_control_connect)
        self.btn_search_again.setObjectName(u"btn_search_again")

        self.verticalLayout.addWidget(self.btn_search_again)


        self.horizontalLayout.addWidget(self.frame_control_connect)

        DialogConnect.setCentralWidget(self.centralwidget)

        self.retranslateUi(DialogConnect)

        QMetaObject.connectSlotsByName(DialogConnect)
    # setupUi

    def retranslateUi(self, DialogConnect):
        DialogConnect.setWindowTitle(QCoreApplication.translate("DialogConnect", u"Dialog Connect", None))
        self.gb_available_dongles.setTitle(QCoreApplication.translate("DialogConnect", u"Available Dongles", None))
        self.gb_available_devs.setTitle(QCoreApplication.translate("DialogConnect", u"Available Devices", None))
        self.gb_group.setTitle(QCoreApplication.translate("DialogConnect", u"Group", None))
        self.btn_connect.setText(QCoreApplication.translate("DialogConnect", u"Connect", None))
        self.btn_pair.setText(QCoreApplication.translate("DialogConnect", u"Pair", None))
        self.btn_search_again.setText(QCoreApplication.translate("DialogConnect", u"Search Again", None))
    # retranslateUi

