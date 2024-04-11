# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'acquisition.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *


class Ui_Acquisition(object):
    def setupUi(self, Acquisition):
        if not Acquisition.objectName():
            Acquisition.setObjectName(u"Acquisition")
        Acquisition.resize(757, 490)
        self.horizontalLayout = QHBoxLayout(Acquisition)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.frame_sidebar = QFrame(Acquisition)
        self.frame_sidebar.setObjectName(u"frame_sidebar")
        self.frame_sidebar.setMinimumSize(QSize(300, 0))
        self.frame_sidebar.setMaximumSize(QSize(300, 16777215))
        self.frame_sidebar.setFrameShape(QFrame.StyledPanel)
        self.frame_sidebar.setFrameShadow(QFrame.Raised)
        self.verticalLayout = QVBoxLayout(self.frame_sidebar)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.scrollArea = QScrollArea(self.frame_sidebar)
        self.scrollArea.setObjectName(u"scrollArea")
        self.scrollArea.setWidgetResizable(True)
        self.scrollAreaWidgetContents = QWidget()
        self.scrollAreaWidgetContents.setObjectName(u"scrollAreaWidgetContents")
        self.scrollAreaWidgetContents.setGeometry(QRect(0, 0, 296, 486))
        self.verticalLayout_3 = QVBoxLayout(self.scrollAreaWidgetContents)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.group_time_window = QGroupBox(self.scrollAreaWidgetContents)
        self.group_time_window.setObjectName(u"group_time_window")
        self.horizontalLayout_3 = QHBoxLayout(self.group_time_window)
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.radio_10s = QRadioButton(self.group_time_window)
        self.radio_10s.setObjectName(u"radio_10s")
        self.radio_10s.setChecked(True)

        self.horizontalLayout_3.addWidget(self.radio_10s)

        self.radio_1s = QRadioButton(self.group_time_window)
        self.radio_1s.setObjectName(u"radio_1s")

        self.horizontalLayout_3.addWidget(self.radio_1s)

        self.radio_200ms = QRadioButton(self.group_time_window)
        self.radio_200ms.setObjectName(u"radio_200ms")

        self.horizontalLayout_3.addWidget(self.radio_200ms)


        self.verticalLayout_3.addWidget(self.group_time_window)

        self.group_automation = QGroupBox(self.scrollAreaWidgetContents)
        self.group_automation.setObjectName(u"group_automation")
        self.verticalLayout_2 = QVBoxLayout(self.group_automation)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.chk_auto_offset = QCheckBox(self.group_automation)
        self.chk_auto_offset.setObjectName(u"chk_auto_offset")

        self.verticalLayout_2.addWidget(self.chk_auto_offset)


        self.verticalLayout_3.addWidget(self.group_automation)

        self.group_filter = QGroupBox(self.scrollAreaWidgetContents)
        self.group_filter.setObjectName(u"group_filter")
        self.gridLayout = QGridLayout(self.group_filter)
        self.gridLayout.setObjectName(u"gridLayout")
        self.lbl_lp = QLabel(self.group_filter)
        self.lbl_lp.setObjectName(u"lbl_lp")

        self.gridLayout.addWidget(self.lbl_lp, 1, 0, 1, 1)

        self.lbl_hp = QLabel(self.group_filter)
        self.lbl_hp.setObjectName(u"lbl_hp")

        self.gridLayout.addWidget(self.lbl_hp, 0, 0, 1, 1)

        self.btn_enable_filter = QPushButton(self.group_filter)
        self.btn_enable_filter.setObjectName(u"btn_enable_filter")

        self.gridLayout.addWidget(self.btn_enable_filter, 2, 2, 1, 1)

        self.spin_hp = QSpinBox(self.group_filter)
        self.spin_hp.setObjectName(u"spin_hp")
        self.spin_hp.setAlignment(Qt.AlignCenter)
        self.spin_hp.setMaximum(250)

        self.gridLayout.addWidget(self.spin_hp, 0, 3, 1, 1)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.gridLayout.addItem(self.horizontalSpacer, 2, 0, 1, 1)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.gridLayout.addItem(self.horizontalSpacer_2, 2, 3, 1, 1)

        self.spin_lp = QSpinBox(self.group_filter)
        self.spin_lp.setObjectName(u"spin_lp")
        self.spin_lp.setAlignment(Qt.AlignCenter)
        self.spin_lp.setMaximum(250)

        self.gridLayout.addWidget(self.spin_lp, 1, 3, 1, 1)


        self.verticalLayout_3.addWidget(self.group_filter)

        self.group_processing = QGroupBox(self.scrollAreaWidgetContents)
        self.group_processing.setObjectName(u"group_processing")
        self.verticalLayout_4 = QVBoxLayout(self.group_processing)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.layout_processings = QVBoxLayout()
        self.layout_processings.setObjectName(u"layout_processings")

        self.verticalLayout_4.addLayout(self.layout_processings)


        self.verticalLayout_3.addWidget(self.group_processing)

        self.layout_controls = QVBoxLayout()
        self.layout_controls.setObjectName(u"layout_controls")

        self.verticalLayout_3.addLayout(self.layout_controls)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout_3.addItem(self.verticalSpacer)

        self.scrollArea.setWidget(self.scrollAreaWidgetContents)

        self.verticalLayout.addWidget(self.scrollArea)


        self.horizontalLayout.addWidget(self.frame_sidebar)

        self.frame_plotter = QFrame(Acquisition)
        self.frame_plotter.setObjectName(u"frame_plotter")
        self.frame_plotter.setFrameShape(QFrame.StyledPanel)
        self.frame_plotter.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_2 = QHBoxLayout(self.frame_plotter)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.layout_frame_plotter = QVBoxLayout()
        self.layout_frame_plotter.setObjectName(u"layout_frame_plotter")

        self.horizontalLayout_2.addLayout(self.layout_frame_plotter)


        self.horizontalLayout.addWidget(self.frame_plotter)


        self.retranslateUi(Acquisition)

        QMetaObject.connectSlotsByName(Acquisition)
    # setupUi

    def retranslateUi(self, Acquisition):
        Acquisition.setWindowTitle(QCoreApplication.translate("Acquisition", u"Form", None))
        self.group_time_window.setTitle(QCoreApplication.translate("Acquisition", u"Time Window", None))
        self.radio_10s.setText(QCoreApplication.translate("Acquisition", u"10 s", None))
        self.radio_1s.setText(QCoreApplication.translate("Acquisition", u"1 s", None))
        self.radio_200ms.setText(QCoreApplication.translate("Acquisition", u"200 ms", None))
        self.group_automation.setTitle(QCoreApplication.translate("Acquisition", u"Automation", None))
        self.chk_auto_offset.setText(QCoreApplication.translate("Acquisition", u"Automatic offset removal", None))
        self.group_filter.setTitle(QCoreApplication.translate("Acquisition", u"Filter", None))
        self.lbl_lp.setText(QCoreApplication.translate("Acquisition", u"Low Pass (Hz)", None))
        self.lbl_hp.setText(QCoreApplication.translate("Acquisition", u"High Pass (Hz)", None))
        self.btn_enable_filter.setText(QCoreApplication.translate("Acquisition", u"Enable", None))
        self.group_processing.setTitle(QCoreApplication.translate("Acquisition", u"RealTime Processing", None))
    # retranslateUi

