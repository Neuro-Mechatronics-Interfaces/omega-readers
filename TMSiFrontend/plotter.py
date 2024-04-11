'''
(c) 2023-2024 Twente Medical Systems International B.V., Oldenzaal The Netherlands

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.

#######  #     #   #####   #
   #     ##   ##  #        
   #     # # # #  #        #
   #     #  #  #   #####   #
   #     #     #        #  #
   #     #     #        #  #
   #     #     #  #####    #

/**
 * @file plotter.py 
 * @brief 
 * Plotter object
 */


'''

import os
from pkg_resources import resource_filename

from PySide2 import QtWidgets, QtGui
from PySide2.QtCore import QSize, Qt

from .designer._plotter import Ui_Plotter
from .chart import Chart
from .utilities.tmsi_style import TMSiStyle

MAX_SIZE = 16777215
MAX_SIZE_SIDEBAR = 300
MIN_SIZE_SIDEBAR = 45
HEIGHT_BUTTON = 38

# Get the path to the images directory
images_dir = resource_filename(__name__, 'media/images/')
images_dir = images_dir.replace("\\", "/")

if not os.path.exists(images_dir):
    # If it doesn't exist, try looking in the parent directory
    images_dir = resource_filename(__name__, '../media/images/')
    images_dir = images_dir.replace("\\", "/")

TMSI_LOGO_PATH = images_dir + "TMSi_logo.PNG"

class Plotter(QtWidgets.QWidget, Ui_Plotter):
    """Plotter interface
    """
    def __init__(self, name = "Plotter"):
        """Initialize Plotter

        :param name: name of the plotter, defaults to "Plotter"
        :type name: str, optional
        """
        super().__init__()
        self._max_side_bar = MAX_SIZE_SIDEBAR
        self._name = name
        self.setupUi(self)
        self.label_logo.setPixmap(QtGui.QPixmap(TMSI_LOGO_PATH))
        self.setStyleSheet(TMSiStyle)
        self._local_setup_ui()
        self.group_amplitude.setTitle("Amplitude UNI (\u03BCV)")
        self.legend.setVisible(False)
        self.lbl_sidebar_title.setText("")
        self.btn_hide_sidebar.clicked.connect(self.toggle_sidebar)
        self.btn_hide_table.clicked.connect(self.toggle_table)
        self.btn_freeze.clicked.connect(self._enable_update_chart)
        self.btn_amplitude_decrease.clicked.connect(lambda: self.increase_amplitude_range(False))
        self.btn_amplitude_increase.clicked.connect(lambda: self.increase_amplitude_range(True))
        self.btn_plotter_zoom_increase.clicked.connect(lambda: self.increase_plotter_zoom(True))
        self.btn_plotter_zoom_decrease.clicked.connect(lambda: self.increase_plotter_zoom(False))
        self.is_chart_update_enabled = True
        self._enabled_channels = []
        self._scales = {}
        self._offsets = {}

    def enable_frame_table(self, enable = True):
        self.frame_table.setVisible(enable)

    def increase_amplitude_range(self, isIncrease):
        if self.spin_amplitude.value() == 0:
            self.spin_amplitude.setValue(1)
        if isIncrease:
            self.spin_amplitude.setValue(self.spin_amplitude.value() * 2)
        else:
            self.spin_amplitude.setValue(self.spin_amplitude.value() // 2)

    def increase_plotter_zoom(self, isIncrease):
        if self.spin_plotter_zoom.value() < 1:
            self.spin_plotter_zoom.setValue(1)
        if isIncrease:
            self.spin_plotter_zoom.setValue(self.spin_plotter_zoom.value() * 2)
        else:
            self.spin_plotter_zoom.setValue(self.spin_plotter_zoom.value() // 2)
    
    def initialize_table(self, titles, values):
        self.set_table_title(titles)
        self.set_table_values(values)
    
    def set_table_title(self, titles):
        self.table.setColumnCount(len(titles))
        self.table.setHorizontalHeaderLabels(titles)
        self.table.horizontalHeader().setStretchLastSection(True) 
        self.table.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
    
    def set_table_values(self, values):
        self.table.setRowCount(len(values))
        n_row = 0
        for key, val in values.items():
            txt_key = QtWidgets.QTableWidgetItem(key)
            txt_key.setFlags(Qt.ItemIsEnabled)
            self.table.setItem(n_row, 0, txt_key)
            txt_val = QtWidgets.QTableWidgetItem(str(val))
            txt_val.setFlags(Qt.ItemIsEnabled)
            self.table.setItem(n_row, 1, txt_val)
            n_row = n_row + 1
                
    def toggle_table(self):
        """Toggle the visibility of the sidebar
        """
        set_visible = not self.table.isVisible()
        for widget in self.frame_table.children():
            if widget.objectName() == "lbl_table":
                if set_visible:
                    widget.setMaximumHeight(0)
                else:
                    widget.setMaximumHeight(MAX_SIZE)
                continue
            if widget.objectName() == "btn_hide_table":
                if set_visible:
                    widget.setText(">>")
                    self.frame_table.setMaximumSize(QSize(self._max_side_bar, MAX_SIZE))
                    self.frame_table.setMinimumSize(QSize(self._max_side_bar, MAX_SIZE))
                    self.btn_hide_table.setMinimumSize(QSize(self._max_side_bar-2,HEIGHT_BUTTON))
                    self.btn_hide_table.setMaximumSize(QSize(self._max_side_bar-2,HEIGHT_BUTTON))
                else:
                    widget.setText("<<")
                    self.frame_table.setMaximumSize(QSize(MIN_SIZE_SIDEBAR, MAX_SIZE))
                    self.frame_table.setMinimumSize(QSize(MIN_SIZE_SIDEBAR, MAX_SIZE))
                    self.btn_hide_table.setMinimumSize(QSize(MIN_SIZE_SIDEBAR-2,HEIGHT_BUTTON))
                    self.btn_hide_table.setMaximumSize(QSize(MIN_SIZE_SIDEBAR-2,HEIGHT_BUTTON))
                continue
            if hasattr(widget,"setVisible"):
                if widget.isEnabled():
                    widget.setVisible(set_visible)
            
    def toggle_sidebar(self):
        """Toggle the visibility of the sidebar
        """
        set_visible = not self.scrollArea.isVisible()
        for widget in self.frame_sidebar.children():
            if widget.objectName() == "lbl_sidebar_title":
                if set_visible:
                    widget.setMaximumHeight(0)
                else:
                    widget.setMaximumHeight(MAX_SIZE)
                continue
            if widget.objectName() == "btn_hide_sidebar":
                if set_visible:
                    widget.setText("<<")
                    self.frame_sidebar.setMaximumSize(QSize(self._max_side_bar, MAX_SIZE))
                    self.frame_sidebar.setMinimumSize(QSize(self._max_side_bar, MAX_SIZE))
                    self.btn_hide_sidebar.setMinimumSize(QSize(self._max_side_bar-2,HEIGHT_BUTTON))
                    self.btn_hide_sidebar.setMaximumSize(QSize(self._max_side_bar-2,HEIGHT_BUTTON))
                else:
                    widget.setText(">>")
                    self.frame_sidebar.setMaximumSize(QSize(MIN_SIZE_SIDEBAR, MAX_SIZE))
                    self.frame_sidebar.setMinimumSize(QSize(MIN_SIZE_SIDEBAR, MAX_SIZE))
                    self.btn_hide_sidebar.setMinimumSize(QSize(MIN_SIZE_SIDEBAR-2,HEIGHT_BUTTON))
                    self.btn_hide_sidebar.setMaximumSize(QSize(MIN_SIZE_SIDEBAR-2,HEIGHT_BUTTON))
                continue
            if hasattr(widget,"setVisible"):
                if widget.isEnabled():
                    widget.setVisible(set_visible)
            
    def update_chart(self, data_to_plot):
        """Update chart with data

        :param data_to_plot: data to be plotted
        :type data_to_plot: list[list]
        """
        if not self.is_chart_update_enabled:
            return
        self.chart.update_chart(data_to_plot)
    
    def _enable_update_chart(self):
        if self.is_chart_update_enabled:
            self.chart.snap()
        self.is_chart_update_enabled = not self.is_chart_update_enabled
        if self.is_chart_update_enabled:
            self.btn_freeze.setText("Pause Viewer")
        else:
            self.btn_freeze.setText("Continue Viewer")
            
    def _local_setup_ui(self):
        self.group_window_size.setVisible(False)
        self.group_window_size.setEnabled(False)
        self.group_plotter_zoom.setVisible(False)
        self.group_plotter_zoom.setEnabled(False)
        self.scrollbar_tracks.setVisible(False)
        self.scrollbar_tracks.setVisible(False)
        self.frame_table.setVisible(False)
        self.group_rotation.setEnabled(False)
        self.group_rotation.setVisible(False)