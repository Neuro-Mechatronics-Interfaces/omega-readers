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
 * @file dialog_connect.py 
 * @brief 
 * Dialog object to communicate with the user to connect to the device.
 */


'''
from PySide2 import QtWidgets, QtCore

from ..designer._dialog_connect import Ui_DialogConnect
from ...utilities.tmsi_style import TMSiStyle

PAIRED = "paired"
NOT_PAIRED = "not paired"

class DialogConnect(QtWidgets.QMainWindow, Ui_DialogConnect):
    """DialogConnect object"""
    def __init__(self, discover, callback_connect, callback_pair, callback_search_again):
        """Initialize dialog connect

        :param discover: discover outcome
        :type discover: Discover
        :param callback_connect: function to go to connect
        :type callback_connect: function
        :param callback_pair: function to go to pair
        :type callback_pair: function
        :param callback_search_again: function to go to search again
        :type callback_search_again: function
        """
        super().__init__()
        self.setupUi(self)
        self.setStyleSheet(TMSiStyle)
        self.setWindowFlags(self.windowFlags() & ~QtCore.Qt.WindowMinMaxButtonsHint)
        self.setWindowModality(QtCore.Qt.ApplicationModal)
        self.discover = discover
        self.callback_connect = callback_connect
        self.callback_search_again = callback_search_again
        self.btn_search_again.clicked.connect(self.click_search_again)
        self.btn_connect.clicked.connect(self.click_connect)
        self.gb_group.setVisible(False)
        self.gb_available_dongles.setVisible(False)
        self.btn_pair.setVisible(False)
        self.btn_pair.setEnabled(False)
        self.btn_connect.setEnabled(False)
        self.list_av_dongles.clear()
        self.list_av_devs.clear()
        self.list_group.clear()
        if self.discover.device_type.name == "saga":
            self.list_av_devs.itemClicked.connect(self.click_available_saga)
            for dev in self.discover.device_list:
                self.list_av_devs.addItem("{}".format(dev.get_device_serial_number()))
        if self.discover.device_type.name == "flex":
            self.list_av_dongles.itemClicked.connect(self.click_available_dongle)
            self.list_av_devs.itemClicked.connect(self.click_available_flex)
            self.list_av_devs.itemDoubleClicked.connect(self.double_click_available_flex)
            self.list_group.itemDoubleClicked.connect(self.double_click_group)
            self.gb_group.setVisible(True)
            self.gb_available_dongles.setVisible(True)
            self.btn_pair.setVisible(True)
            for dongle in self.discover.dongle_list:
                self.list_av_dongles.addItem("{}".format(dongle.get_serial_number()))
        if self.discover.device_type.name == "apex":
            if self.discover.dr_interface.name == "bluetooth":
                self.gb_available_dongles.setVisible(True)
                self.btn_pair.setVisible(True)
                self.list_av_dongles.itemClicked.connect(self.click_available_dongle)
                self.list_av_devs.itemClicked.connect(self.click_available_apex)
                for dongle in self.discover.dongle_list:
                    self.list_av_dongles.addItem("{}".format(dongle.get_serial_number()))
            else:
                self.list_av_devs.itemClicked.connect(self.click_available_apex)
                for dev in self.discover.device_list:
                    self.list_av_devs.addItem("{}".format(dev.get_device_serial_number()))
            
    def click_available_apex(self):
        """Click available apex action"""
        dev_info = self.list_av_devs.currentItem().text().split(" - ")
        if len(dev_info) > 1:
            if dev_info[1] == NOT_PAIRED:
                self.btn_pair.setEnabled(True)
                self.btn_connect.setEnabled(False)
            else:
                self.btn_connect.setEnabled(True)
                self.btn_pair.setEnabled(False)
        else:
            selected_dev = self.list_av_devs.currentRow()
            if selected_dev != -1:
                self.btn_connect.setEnabled(True)
            else:
                self.btn_connect.setEnabled(False)

    def click_available_dongle(self):
        """Click available dongle action"""
        self.list_av_devs.clear()
        self.list_group.clear()
        for dev in self.discover.device_list:
            paired = NOT_PAIRED
            if dev.get_pairing_status().value == 1 and str(dev.get_dongle_serial_number()) == self.list_av_dongles.currentItem().text():
                paired = PAIRED
            self.list_av_devs.addItem("{} - {}".format(dev.get_device_serial_number(), paired))

    def click_available_flex(self):
        """Click available flex action"""
        if self.list_av_devs.currentItem().text().split(" - ")[1] == NOT_PAIRED:
            self.btn_pair.setEnabled(True)
        else:
            self.btn_pair.setEnabled(False)
          
    def click_available_saga(self):
        """Click available saga action"""
        selected_dev = self.list_av_devs.currentRow()
        if selected_dev != -1:
            self.btn_connect.setEnabled(True)
        else:
            self.btn_connect.setEnabled(False)

    def click_connect(self):
        """Click connect action"""
        args = dict()
        args["dongle"] = None
        args["device"] = None
        if self.list_av_dongles.currentItem() is not None:
            args["dongle"] = self.list_av_dongles.currentItem().text()
        if self.list_av_devs.currentItem() is not None:
            args["device"] = self.list_av_devs.currentItem().text().split(" - ")[0]
        args["group"] = [self.list_group.item(i).text() for i in range(self.list_group.count())]
        self.close()
        self.callback_connect(args)
    
    def click_search_again(self):
        """Click search again action"""
        self.close()
        self.callback_search_again()

    def double_click_available_flex(self):
        """Doubleclick available flex action"""
        dev_info = self.list_av_devs.currentItem().text().split(" - ")
        if dev_info[1] == NOT_PAIRED:
            return
        items = [self.list_group.item(i).text() for i in range(self.list_group.count())]
        if dev_info[0] in items:
            return
        if len(items) >= 4:
            return
        self.list_group.addItem(dev_info[0])
        self.enable_connect()

    def double_click_group(self):
        """Doubleclick group action"""
        self.list_group.takeItem(self.list_group.currentRow())
        self.enable_connect()

    def enable_connect(self):
        """Enable connect"""
        if self.list_group.count() > 0:
            self.btn_connect.setEnabled(True)
        else:
            self.btn_connect.setEnabled(False)