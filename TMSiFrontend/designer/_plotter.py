# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'plotter.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *

from pyqtgraph import GraphicsLayoutWidget


class Ui_Plotter(object):
    def setupUi(self, Plotter):
        if not Plotter.objectName():
            Plotter.setObjectName(u"Plotter")
        Plotter.resize(757, 540)
        self.gridLayout = QGridLayout(Plotter)
        self.gridLayout.setObjectName(u"gridLayout")
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.frame_sidebar = QFrame(Plotter)
        self.frame_sidebar.setObjectName(u"frame_sidebar")
        self.frame_sidebar.setMinimumSize(QSize(300, 0))
        self.frame_sidebar.setMaximumSize(QSize(300, 16777215))
        self.frame_sidebar.setFrameShape(QFrame.StyledPanel)
        self.frame_sidebar.setFrameShadow(QFrame.Raised)
        self.verticalLayout = QVBoxLayout(self.frame_sidebar)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.lbl_sidebar_title = QLabel(self.frame_sidebar)
        self.lbl_sidebar_title.setObjectName(u"lbl_sidebar_title")
        self.lbl_sidebar_title.setMaximumSize(QSize(16777215, 0))
        font = QFont()
        font.setPointSize(12)
        self.lbl_sidebar_title.setFont(font)
        self.lbl_sidebar_title.setAlignment(Qt.AlignCenter)
        self.lbl_sidebar_title.setWordWrap(True)

        self.verticalLayout.addWidget(self.lbl_sidebar_title)

        self.btn_freeze = QPushButton(self.frame_sidebar)
        self.btn_freeze.setObjectName(u"btn_freeze")
        self.btn_freeze.setMaximumSize(QSize(10000000, 16777215))

        self.verticalLayout.addWidget(self.btn_freeze)

        self.group_channels = QGroupBox(self.frame_sidebar)
        self.group_channels.setObjectName(u"group_channels")
        self.gridLayout_2 = QGridLayout(self.group_channels)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.btn_enable_all_channels = QPushButton(self.group_channels)
        self.btn_enable_all_channels.setObjectName(u"btn_enable_all_channels")

        self.gridLayout_2.addWidget(self.btn_enable_all_channels, 0, 0, 1, 1)

        self.btn_disable_all_channels = QPushButton(self.group_channels)
        self.btn_disable_all_channels.setObjectName(u"btn_disable_all_channels")

        self.gridLayout_2.addWidget(self.btn_disable_all_channels, 0, 1, 1, 1)

        self.btn_autoscale = QPushButton(self.group_channels)
        self.btn_autoscale.setObjectName(u"btn_autoscale")

        self.gridLayout_2.addWidget(self.btn_autoscale, 1, 0, 1, 2)


        self.verticalLayout.addWidget(self.group_channels)

        self.group_amplitude = QGroupBox(self.frame_sidebar)
        self.group_amplitude.setObjectName(u"group_amplitude")
        self.gridLayout_3 = QGridLayout(self.group_amplitude)
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.btn_amplitude_increase = QPushButton(self.group_amplitude)
        self.btn_amplitude_increase.setObjectName(u"btn_amplitude_increase")

        self.gridLayout_3.addWidget(self.btn_amplitude_increase, 1, 2, 1, 1)

        self.btn_amplitude_decrease = QPushButton(self.group_amplitude)
        self.btn_amplitude_decrease.setObjectName(u"btn_amplitude_decrease")

        self.gridLayout_3.addWidget(self.btn_amplitude_decrease, 1, 0, 1, 1)

        self.spin_amplitude = QSpinBox(self.group_amplitude)
        self.spin_amplitude.setObjectName(u"spin_amplitude")
        self.spin_amplitude.setAlignment(Qt.AlignCenter)
        self.spin_amplitude.setMaximum(100000)

        self.gridLayout_3.addWidget(self.spin_amplitude, 1, 1, 1, 1)


        self.verticalLayout.addWidget(self.group_amplitude)

        self.group_plotter_zoom = QGroupBox(self.frame_sidebar)
        self.group_plotter_zoom.setObjectName(u"group_plotter_zoom")
        self.horizontalLayout_4 = QHBoxLayout(self.group_plotter_zoom)
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.btn_plotter_zoom_decrease = QPushButton(self.group_plotter_zoom)
        self.btn_plotter_zoom_decrease.setObjectName(u"btn_plotter_zoom_decrease")

        self.horizontalLayout_4.addWidget(self.btn_plotter_zoom_decrease)

        self.spin_plotter_zoom = QDoubleSpinBox(self.group_plotter_zoom)
        self.spin_plotter_zoom.setObjectName(u"spin_plotter_zoom")
        self.spin_plotter_zoom.setAlignment(Qt.AlignCenter)
        self.spin_plotter_zoom.setMinimum(1)

        self.horizontalLayout_4.addWidget(self.spin_plotter_zoom)

        self.btn_plotter_zoom_increase = QPushButton(self.group_plotter_zoom)
        self.btn_plotter_zoom_increase.setObjectName(u"btn_plotter_zoom_increase")

        self.horizontalLayout_4.addWidget(self.btn_plotter_zoom_increase)


        self.verticalLayout.addWidget(self.group_plotter_zoom)

        self.group_rotation = QGroupBox(self.frame_sidebar)
        self.group_rotation.setObjectName(u"group_rotation")
        self.horizontalLayout_5 = QHBoxLayout(self.group_rotation)
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.cb_rotation_angles = QComboBox(self.group_rotation)
        self.cb_rotation_angles.setObjectName(u"cb_rotation_angles")
        self.cb_rotation_angles.setEditable(True)

        self.horizontalLayout_5.addWidget(self.cb_rotation_angles)


        self.verticalLayout.addWidget(self.group_rotation)

        self.scrollArea = QScrollArea(self.frame_sidebar)
        self.scrollArea.setObjectName(u"scrollArea")
        self.scrollArea.setWidgetResizable(True)
        self.scrollAreaWidgetContents = QWidget()
        self.scrollAreaWidgetContents.setObjectName(u"scrollAreaWidgetContents")
        self.scrollAreaWidgetContents.setGeometry(QRect(0, 0, 296, 69))
        self.verticalLayout_3 = QVBoxLayout(self.scrollAreaWidgetContents)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.layout_channels = QVBoxLayout()
        self.layout_channels.setObjectName(u"layout_channels")

        self.verticalLayout_3.addLayout(self.layout_channels)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout_3.addItem(self.verticalSpacer)

        self.scrollArea.setWidget(self.scrollAreaWidgetContents)

        self.verticalLayout.addWidget(self.scrollArea)

        self.group_window_size = QGroupBox(self.frame_sidebar)
        self.group_window_size.setObjectName(u"group_window_size")
        self.group_window_size.setMinimumSize(QSize(0, 0))
        self.horizontalLayout = QHBoxLayout(self.group_window_size)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.btn_time_window_decrease = QPushButton(self.group_window_size)
        self.btn_time_window_decrease.setObjectName(u"btn_time_window_decrease")

        self.horizontalLayout.addWidget(self.btn_time_window_decrease)

        self.spin_time_window = QSpinBox(self.group_window_size)
        self.spin_time_window.setObjectName(u"spin_time_window")
        self.spin_time_window.setAlignment(Qt.AlignCenter)
        self.spin_time_window.setReadOnly(True)
        self.spin_time_window.setMinimum(1)
        self.spin_time_window.setMaximum(10)
        self.spin_time_window.setValue(10)

        self.horizontalLayout.addWidget(self.spin_time_window)

        self.btn_time_window_increase = QPushButton(self.group_window_size)
        self.btn_time_window_increase.setObjectName(u"btn_time_window_increase")

        self.horizontalLayout.addWidget(self.btn_time_window_increase)


        self.verticalLayout.addWidget(self.group_window_size)

        self.frame_logo = QFrame(self.frame_sidebar)
        self.frame_logo.setObjectName(u"frame_logo")
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.frame_logo.sizePolicy().hasHeightForWidth())
        self.frame_logo.setSizePolicy(sizePolicy)
        self.frame_logo.setMaximumSize(QSize(16777215, 80))
        self.frame_logo.setFrameShape(QFrame.StyledPanel)
        self.frame_logo.setFrameShadow(QFrame.Raised)
        self.gridLayout_4 = QGridLayout(self.frame_logo)
        self.gridLayout_4.setObjectName(u"gridLayout_4")
        self.gridLayout_4.setSizeConstraint(QLayout.SetFixedSize)
        self.gridLayout_4.setVerticalSpacing(0)
        self.gridLayout_4.setContentsMargins(-1, 0, -1, 0)
        self.label_logo = QLabel(self.frame_logo)
        self.label_logo.setObjectName(u"label_logo")
        sizePolicy.setHeightForWidth(self.label_logo.sizePolicy().hasHeightForWidth())
        self.label_logo.setSizePolicy(sizePolicy)
        self.label_logo.setMinimumSize(QSize(143, 62))
        self.label_logo.setMaximumSize(QSize(143, 62))
        self.label_logo.setCursor(QCursor(Qt.ArrowCursor))
        self.label_logo.setLayoutDirection(Qt.LeftToRight)
        self.label_logo.setFrameShape(QFrame.NoFrame)
        self.label_logo.setFrameShadow(QFrame.Plain)
        self.label_logo.setScaledContents(True)
        self.label_logo.setAlignment(Qt.AlignCenter)
        self.label_logo.setMargin(0)

        self.gridLayout_4.addWidget(self.label_logo, 0, 1, 1, 1)

        self.horizontalSpacer_logo1 = QSpacerItem(68, 20, QSizePolicy.Fixed, QSizePolicy.Minimum)

        self.gridLayout_4.addItem(self.horizontalSpacer_logo1, 0, 0, 1, 1)

        self.horizontalSpacer_logo2 = QSpacerItem(70, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.gridLayout_4.addItem(self.horizontalSpacer_logo2, 0, 2, 1, 1)


        self.verticalLayout.addWidget(self.frame_logo)

        self.btn_hide_sidebar = QPushButton(self.frame_sidebar)
        self.btn_hide_sidebar.setObjectName(u"btn_hide_sidebar")

        self.verticalLayout.addWidget(self.btn_hide_sidebar)


        self.gridLayout.addWidget(self.frame_sidebar, 0, 0, 1, 1)

        self.frame_chart = QFrame(Plotter)
        self.frame_chart.setObjectName(u"frame_chart")
        self.frame_chart.setFrameShape(QFrame.StyledPanel)
        self.frame_chart.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_2 = QHBoxLayout(self.frame_chart)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.chart = GraphicsLayoutWidget(self.frame_chart)
        self.chart.setObjectName(u"chart")

        self.horizontalLayout_3.addWidget(self.chart)

        self.legend = GraphicsLayoutWidget(self.frame_chart)
        self.legend.setObjectName(u"legend")
        self.legend.setMaximumSize(QSize(200, 16777215))

        self.horizontalLayout_3.addWidget(self.legend)


        self.horizontalLayout_2.addLayout(self.horizontalLayout_3)

        self.scrollbar_tracks = QScrollBar(self.frame_chart)
        self.scrollbar_tracks.setObjectName(u"scrollbar_tracks")
        self.scrollbar_tracks.setOrientation(Qt.Vertical)

        self.horizontalLayout_2.addWidget(self.scrollbar_tracks)

        self.frame_table = QFrame(self.frame_chart)
        self.frame_table.setObjectName(u"frame_table")
        self.frame_table.setMaximumSize(QSize(300, 16777215))
        self.frame_table.setFrameShape(QFrame.StyledPanel)
        self.frame_table.setFrameShadow(QFrame.Raised)
        self.verticalLayout_2 = QVBoxLayout(self.frame_table)
        self.verticalLayout_2.setSpacing(6)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.lbl_table = QLabel(self.frame_table)
        self.lbl_table.setObjectName(u"lbl_table")

        self.verticalLayout_2.addWidget(self.lbl_table)

        self.table = QTableWidget(self.frame_table)
        self.table.setObjectName(u"table")
        self.table.setGridStyle(Qt.NoPen)
        self.table.verticalHeader().setVisible(False)

        self.verticalLayout_2.addWidget(self.table)

        self.btn_hide_table = QPushButton(self.frame_table)
        self.btn_hide_table.setObjectName(u"btn_hide_table")

        self.verticalLayout_2.addWidget(self.btn_hide_table)


        self.horizontalLayout_2.addWidget(self.frame_table)


        self.gridLayout.addWidget(self.frame_chart, 0, 2, 1, 1)


        self.retranslateUi(Plotter)

        QMetaObject.connectSlotsByName(Plotter)
    # setupUi

    def retranslateUi(self, Plotter):
        Plotter.setWindowTitle(QCoreApplication.translate("Plotter", u"Form", None))
        self.lbl_sidebar_title.setText(QCoreApplication.translate("Plotter", u"PLOTTER", None))
        self.btn_freeze.setText(QCoreApplication.translate("Plotter", u"Pause Viewer", None))
        self.group_channels.setTitle(QCoreApplication.translate("Plotter", u"Channels", None))
        self.btn_enable_all_channels.setText(QCoreApplication.translate("Plotter", u"Enable all", None))
        self.btn_disable_all_channels.setText(QCoreApplication.translate("Plotter", u"Disable all", None))
        self.btn_autoscale.setText(QCoreApplication.translate("Plotter", u"Autoscale", None))
        self.group_amplitude.setTitle(QCoreApplication.translate("Plotter", u"Amplitude UNI", None))
        self.btn_amplitude_increase.setText(QCoreApplication.translate("Plotter", u"Increase", None))
        self.btn_amplitude_decrease.setText(QCoreApplication.translate("Plotter", u"Decrease", None))
        self.group_plotter_zoom.setTitle(QCoreApplication.translate("Plotter", u"Zoom (x)", None))
        self.btn_plotter_zoom_decrease.setText(QCoreApplication.translate("Plotter", u"Decrease", None))
        self.btn_plotter_zoom_increase.setText(QCoreApplication.translate("Plotter", u"Increase", None))
        self.group_rotation.setTitle(QCoreApplication.translate("Plotter", u"Tail orientation", None))
        self.cb_rotation_angles.setCurrentText("")
        self.group_window_size.setTitle(QCoreApplication.translate("Plotter", u"Window size", None))
        self.btn_time_window_decrease.setText(QCoreApplication.translate("Plotter", u"Decrease", None))
        self.btn_time_window_increase.setText(QCoreApplication.translate("Plotter", u"Increase", None))
        self.label_logo.setText("")
        self.btn_hide_sidebar.setText(QCoreApplication.translate("Plotter", u"<<", None))
        self.lbl_table.setText("")
        self.btn_hide_table.setText(QCoreApplication.translate("Plotter", u">>", None))
    # retranslateUi

