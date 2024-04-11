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
 * @file ${signal_plotter_helper.py}
 * @brief This file is used as helper to make a signal plotter in the GUI
 *
 */   
'''

import numpy as np
from os.path import join, dirname, realpath, normpath, exists
import json

from TMSiBackend.data_consumer.consumer import Consumer
from TMSiBackend.data_consumer.consumer_thread import ConsumerThread
from TMSiBackend.data_consumer.consumer_thread_apex import ConsumerThreadApex
from TMSiBackend.data_monitor.monitor import Monitor

from TMSiSDK.device.tmsi_device_enums import MeasurementType
from TMSiSDK.tmsi_sdk import ChannelType

from .plotter_helper import PlotterHelper
from .real_time_signal_plotter import RealTimeSignalPlotter

class SignalPlotterHelper(PlotterHelper):
    def __init__(self, device, grid_type = None):
        if device.get_device_type() == "APEX":
            super().__init__(device = device, monitor_class = Monitor, consumer_thread_class = ConsumerThreadApex) 
        else:
            super().__init__(device = device, monitor_class = Monitor, consumer_thread_class = ConsumerThread) 
        self.main_plotter = RealTimeSignalPlotter()
        self._current_window_size = self.main_plotter.window_size   
        self.grid_type = grid_type
    
    def callback(self, callback_object):
        if "live_impedances" in callback_object and self.main_plotter.table.isVisible():
            live_impedances = callback_object["live_impedances"]
            table_impedances = {}
            max_n_channel = self.device.get_num_impedance_channels()
            keys = [key for key in live_impedances if int(key) < max_n_channel]
            keys.sort()
            for key in keys:
                table_impedances[self.device.get_device_channels()[key - 1].get_channel_name()] = "{} k\u03A9".format(int(live_impedances[key]["Re"]))
            self.main_plotter.set_table_values(table_impedances)

        response = callback_object["buffer"]
        # Wait until data is coming in
        if response.dataset is None:
            return

        # Set x-axis time ticks based on the counter channel
        main_buffer = response.copy()
        last_counter = main_buffer.get_last_value()[-1]
        elapsed_time = last_counter // self.sampling_frequency
        window_size = self.main_plotter.window_size

        time_values, time_ticks = self.generate_time_ticks(
            elapsed_time = elapsed_time, window_size = window_size)
        self.main_plotter.set_time_ticks(
            time_values = time_values, time_ticks = time_ticks)
        
        # Define the plotting buffer based on the time window
        if self._current_window_size != window_size:
            self._plotting_buffer = None
            self._current_window_size = window_size
        if self._current_window_size == 10:
            self._plotting_buffer =  main_buffer
        else:
            self._plotting_buffer, self._last_pointer = self.get_plotting_buffer(
                plotting_buffer = self._plotting_buffer, 
                main_buffer = main_buffer, 
                elapsed_time = elapsed_time, 
                window_size = window_size, 
                sampling_frequency = self.sampling_frequency, 
                last_counter = last_counter,
                last_pointer = self._last_pointer
            )

        pointer_data_to_plot = self._plotting_buffer.pointer_buffer
        if not hasattr(self._plotting_buffer, 'dataset'):
            return
        data_to_plot = self._plotting_buffer.dataset.copy()
        
        # Compute markers
        time_keys, marker_keys = self._compute_markers(data_to_plot = data_to_plot, pointer_data_to_plot = pointer_data_to_plot)

        # Delete old markers
        current_markers = self.main_plotter.get_time_markers().copy()
        self._clean_old_markers(current_markers = current_markers, last_counter = last_counter)

        # Add new markers
        for time_key in time_keys:
            if str(time_key) not in current_markers:
                if time_key in marker_keys:
                    self.main_plotter.add_time_marker(key=time_key, time_value=time_key % self.main_plotter.window_size, color=(34, 155, 34))
                else:
                    self.main_plotter.add_time_marker(key=time_key, time_value=time_key % self.main_plotter.window_size, color=(252, 76,2))
                self.main_plotter.update_time_marker(key=time_key, time_value = time_key % self.main_plotter.window_size)
            
        # Add whitening zone to the plotted data
        size_dataset = np.shape(data_to_plot)[1]
        n_channels = np.shape(data_to_plot)[0]

        if pointer_data_to_plot != size_dataset:
            num_time_samples = self.sampling_frequency * self.main_plotter.window_size
            whitening_zone = int(self.whitening_zone * num_time_samples)
            if pointer_data_to_plot < whitening_zone:
               self.main_plotter.remove_offset() 
            space_to_fill = size_dataset - pointer_data_to_plot
            if space_to_fill < whitening_zone:
                data_to_plot[:, pointer_data_to_plot:] = \
                    np.full((n_channels, space_to_fill), np.nan)
            else:
                data_to_plot[:, pointer_data_to_plot:pointer_data_to_plot+whitening_zone] = \
                    np.full((n_channels, whitening_zone), np.nan)

        # Reorder data 
        # Send data to plotter and update chart
        self.main_plotter.update_chart(data_to_plot = data_to_plot[self.channel_conversion_list], time_span = self.time_span)

    def initialize(self):
        self.channels_default =self.device.get_device_active_channels() 
        if self.device.get_device_type() == 'SAGA':
            self.measurement_type = MeasurementType.SAGA_SIGNAL
            if self.channels_default[-3].get_channel_type() == ChannelType.status:
                self._get_trigger_event = self._get_trigger_event_saga_trigger
        elif self.device.get_device_type() == 'APEX':
            self.measurement_type = MeasurementType.APEX_SIGNAL
            self._get_trigger_event = self._get_trigger_event_apex_trigger
            # if real time impedance active, enable the real time frame
            if self.device.get_live_impedance():
                self.main_plotter.enable_frame_table()
                self.main_plotter.initialize_table(["Name","Impedance"], {})
        
        self.whitening_zone = 0.02
        self.time_span = np.arange(0,10,1.0/self.sampling_frequency)

        self._read_grid_info()    
        self._get_channel_conversion_list()
        # Reorder channels, reorders the channel names and controls;
        # Data is reordered in callback
        self.channels=[self.channels_default[idx] for idx in self.channel_conversion_list] 
        # Initialize components to control the plotting of the channels
        self.main_plotter.initialize_channels_components(self.channels)
        
    def monitor_function(self):
        reading = {}
        reading["status"] = 200
        reading["buffer"] = self.consumer_thread.original_buffer.copy()
        if self.device.get_device_type() == "APEX":
            reading["live_impedances"] = self.consumer_thread.cycling_impedance
        return reading
        
    def on_error(self, response):
        print("ERROR! {}".format(response))
    
    def start(self):
        # Initialize queue
        self.consumer = Consumer()
        # Initialize thread
        self.consumer_thread = self.consumer_thread_class(
            consumer_reading_queue=self.consumer.reading_queue,
            sample_rate=self.device.get_device_sampling_frequency()
        )
        # Register device to sample data server and start reading samples
        self.consumer.open(
            server = self.device,
            reading_queue_id = self.device.get_id(),
            consumer_thread=self.consumer_thread)
        # Start measurement
        self.device.start_measurement(self.measurement_type)
        # Apply monitor function and send data to callback
        self.monitor = self.monitor_class(monitor_function = self.monitor_function, callback=self.callback, on_error=self.on_error)
        self.monitor.start()

    def stop(self):
        super().stop()

    def _compute_markers(self, data_to_plot, pointer_data_to_plot):
        # Prepare (and plot) trigger/marker events as vertical line
        marker_event = self._get_marker_event(data_to_plot = data_to_plot)
        trigger_event = self._get_trigger_event(data_to_plot = data_to_plot)
        event_line = np.logical_or(marker_event, trigger_event)
        # Correct for length difference
        event_line = np.insert(event_line, 0, False)
        # Ignore the whitening zone for the event marker line
        whitening_zone = int(self.whitening_zone * self.sampling_frequency * self.main_plotter.window_size)
        if len(event_line) > pointer_data_to_plot:
            if len(event_line) > pointer_data_to_plot+whitening_zone:
                event_line[pointer_data_to_plot:pointer_data_to_plot+whitening_zone] = False
            else:
                event_line[pointer_data_to_plot:] = False

        # Compute the marker keys
        event_counters = data_to_plot[-1, event_line]
        marker_keys = data_to_plot[-1, np.insert(marker_event, 0, False)] / self.sampling_frequency
        time_keys = event_counters / self.sampling_frequency
        return time_keys, marker_keys
        
    def _clean_old_markers(self, current_markers, last_counter):
        # Clean markers that are from longer ago than the size of the window
        for marker in current_markers:
            if float(current_markers[marker]['key']) < (last_counter / self.sampling_frequency - self.main_plotter.window_size):
                self.main_plotter.delete_time_marker(key=current_markers[marker]['key'])

    def _get_channel_conversion_list(self):
        if self.grid_type in self.conversion_data:
            # Read conversion list of the specified grid type
            conversion_list= np.array(self.conversion_data[self.grid_type]['channel_conversion'])

            # Check number of channels in grid
            if '4' in self.grid_type or self.grid_type[-1]=='1' or self.grid_type[-1]==2:
                nChan_grid=32
            else:
                nChan_grid=64

            # Check whether grid type can be used with device
            if self.device.get_num_channels() > nChan_grid:
                print('Use grid channel order of grid type ', self.grid_type)
                offset = 0
                #Add CREF channel and remove disabled channels, when present in conversion_list
                conversion_list = np.hstack((0, conversion_list))
                for ch_idx, ch in enumerate(self.device.get_device_channels()):
                    if not ch._enabled:
                        if ch_idx<(nChan_grid+1):
                            conversion_list = np.delete(conversion_list,(conversion_list == ch_idx-offset))
                            conversion_list[conversion_list>(ch_idx-offset)] = conversion_list[conversion_list>(ch_idx-offset)] - 1
                            offset = offset + 1

                # add other device channels
                self.channel_conversion_list = np.hstack((conversion_list, np.arange(len(conversion_list), len(self.channels_default),dtype=int)))
            else:
                print('Can not use ordening of 64channel grid on 32channel device. Default channel ordening is used.')
                self.channel_conversion_list = np.arange(len(self.channels_default), dtype=int)
        else:
            print('Default channel ordening is used.')
            self.channel_conversion_list = np.arange(len(self.channels_default), dtype=int)

    def _get_marker_event(self, data_to_plot):
        return np.diff(data_to_plot[len(data_to_plot)-2,:]) == 1
    
    def _get_trigger_event(self, data_to_plot):
        return np.full(np.shape(data_to_plot[0][:-1]), False)
   
    def _get_trigger_event_apex_trigger(self, data_to_plot):
        return np.diff(data_to_plot[len(data_to_plot)-2,:].astype(int) & 0b11110) != 0

    def _get_trigger_event_saga_trigger(self, data_to_plot):
        return np.diff(data_to_plot[len(data_to_plot)-3,:]) != 0

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

    