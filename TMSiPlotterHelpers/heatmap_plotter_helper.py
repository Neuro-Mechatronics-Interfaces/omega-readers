'''
(c) 2023,2024 Twente Medical Systems International B.V., Oldenzaal The Netherlands

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
 * @file ${heatmap_plotter_helper.py}
 * @brief This file shows how to make a heatmap plotter from the filtered 
 * signal plotter, assuming a plotter that converts the data to heatmap is 
 * already available. The signal acquisition part is taken care of by the 
 * (filtered) signal plotter helper and here we focus on transfering the device 
 * data to a heatmap plot.
 * More information about how to make your own plotters can be found in the documentation.
 *
 */
'''

import numpy as np
from PySide2 import QtWidgets
from os.path import join, dirname, realpath, normpath, exists
import json

from TMSiBackend.data_monitor.monitor import Monitor

from TMSiSDK.device.tmsi_device_enums import MeasurementType
from TMSiSDK.tmsi_sdk import ChannelType

from TMSiFrontend.plotters.heatmap_plotter import HeatmapPlotter
from TMSiFrontend.utilities.tmsi_headcaps import TMSiHeadcaps
from TMSiFrontend.utilities.tmsi_grids import TMSiGrids

from .signal_plotter_helper import SignalPlotterHelper
from .filtered_signal_plotter_helper import FilteredSignalPlotterHelper, FilteredConsumerThread


class HeatmapPlotterHelper(FilteredSignalPlotterHelper):
    def __init__(self, device, grid_type = None, is_head_layout = False, hpf = 5, lpf = 0, order = 1):
        # call super of SignalAcquisitionHelper, initializing acquisition details
        super(SignalPlotterHelper, self).__init__(device = device, monitor_class = Monitor, consumer_thread_class = FilteredConsumerThread )
        
        if self.device.get_device_type() == 'SAGA':
            self.measurement_type = MeasurementType.SAGA_SIGNAL
        elif self.device.get_device_type() == 'APEX':
            self.measurement_type = MeasurementType.APEX_SIGNAL

        self.head_layout = is_head_layout
        self.grid_type = grid_type
        self.main_plotter = HeatmapPlotter(device_type=device.get_device_type(), is_headcap=is_head_layout)
        
        # filter settings
        self.hpf = hpf
        self.lpf = lpf
        self.order = order

    def callback(self, callback_object):
        response = callback_object["buffer"]
        # The function that provides the plotter from data
        pointer = response.pointer_buffer
        # Wait for data to come in
        if response.dataset is None:
            return
          
        # Get data in time window
        if len(response.dataset[0]) <= self.window_length:
            data = response.dataset
        elif pointer < self.window_length:
            data = np.hstack((response.dataset[:,-(self.window_length-pointer):], response.dataset[:,:pointer]))
        else:
            data = response.dataset[:,(pointer-self.window_length):pointer]
        # Calulate rms
        rms_data = np.sqrt(np.mean(data**2, axis = 1))
        self.main_plotter.update_chart(rms_data[self.heatmap_channels])

    def initialize(self):
        self.window_length = int(self.sampling_frequency/4)
        self.channels_default = self.device.get_device_channels()
        self.active_channels = self.device.get_device_active_channels()
        # get electrode positions and channel ordening
        coordinates = self._get_coordinates()
        original_channels = []
        self.heatmap_channels = []
        self.n_unfiltered_channels = 0
        for idx,channel in enumerate(self.active_channels):
            if channel.get_channel_type() == ChannelType.UNI and channel.get_channel_index() > 0:
                original_channels.append(channel)
                self.heatmap_channels.append(idx)
            elif channel.get_channel_type() != ChannelType.UNI and channel.get_channel_type() != ChannelType.BIP:
                self.n_unfiltered_channels +=1
        
        if hasattr(self, 'conversion_list'): 
            self.main_plotter.set_electrode_position(channels = original_channels, coordinates = coordinates, reordered_indices = self.conversion_list.tolist())
        else:
            self.main_plotter.set_electrode_position(channels = original_channels, coordinates = coordinates)

    def _read_grid_info(self):
        file_dir = dirname(realpath(__file__)) # directory of this file
        # Get the HD-EMG conversion file
        config_file = join(file_dir, '../TMSiSDK/tmsi_resources', 'HD_EMG_grid_channel_configuration.json')
        
        # Open the file if it exists, notify the user if it does not
        if exists(config_file):
            # Get the HD-EMG conversion table
            with open(config_file) as json_file:
                self.conversion_data = json.load(json_file)
        else:
            self.conversion_data = []
            print("Couldn't load HD-EMG conversion file. Default channel order is used.")

    def _get_coordinates(self):
        if self.head_layout:
            if len(self.channels_default) < 32:
                coordinates = TMSiHeadcaps().headcaps["eeg24"]
            elif len(self.channels_default) <64:
                coordinates = TMSiHeadcaps().headcaps["eeg32"]
            else:
                coordinates = TMSiHeadcaps().headcaps["eeg64"]
        else: 
            self._read_grid_info()             
            if self.grid_type in self.conversion_data:
                self.conversion_list= np.array(self.conversion_data[self.grid_type]['channel_conversion'])
            if len(self.channels_default)<64:
                if '6' in self.grid_type:
                    if self.grid_type[-1]=='2':
                        coordinates = TMSiGrids().grids["6-11-2"]
                    else:
                        coordinates = TMSiGrids().grids["6-11-1"]
                else:
                    coordinates = TMSiGrids().grids["4-8"]
            else:
                if '6' in self.grid_type:
                    if self.grid_type[-1]=='2':
                        coordinates = TMSiGrids().grids["6-11-2"]
                    elif self.grid_type[-1]=='1':
                        coordinates = TMSiGrids().grids["6-11-1"]
                    else:
                        coordinates = TMSiGrids().grids["6-11"]
                else:
                    if (self.grid_type[-1]=='1' or self.grid_type[-1]=='2') or '4' in self.grid_type:
                        coordinates = TMSiGrids().grids["4-8"]
                    else:
                        coordinates = TMSiGrids().grids["8-8"]
        return coordinates
