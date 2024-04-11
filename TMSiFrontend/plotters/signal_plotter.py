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
 * @file signal_plotter.py 
 * @brief 
 * SignalPlotter object.
 */


'''
import math
import numpy as np

from PySide2 import QtWidgets

from TMSiSDK import LogPerformances

from ..plotter import Plotter
from ..charts.signal_chart import SignalChart
from ..components.channel_component import ChannelComponent


class SignalPlotter(Plotter):
    """SignalPlotter object
    """
    def __init__(self, get_data_callback = None, update_viewer_time_scrollbar_callback = None, name = "Signal Plotter"):
        """Initialize the SignalPlotter object

        :param get_data_callback: function to be called when the interface is updated (used in case of offline application), defaults to None
        :type get_data_callback: function, optional
        :param name: name of the signal plotter, defaults to "Signal Plotter"
        :type name: str, optional
        """
        super().__init__(name = name)
        self.chart = SignalChart(self.chart)
        self._get_data_callback = get_data_callback
        self._update_viewer_time_scrollbar_callback = update_viewer_time_scrollbar_callback
        self._update_enabled_disabled = False
        self._update_scales_disabled = False
        self._compute_autoscale = False
        self._compute_offset = False
        self.window_size = 10
        self.chart.set_time_range(self.window_size)
        self._connect_widgets_to_functions()

    def add_time_marker(self, time_value, key = None, color = "red"):
        """Add a time marker to the chart

        :param time_value: time coordinate on the chart
        :type time_value: float
        :param key: name of the marker, defaults to None
        :type key: str, optional
        :param color: color of the marker, defaults to "red"
        :type color: str, optional
        """
        self.chart.add_time_marker(time_value = time_value, key = key, color = color)
    
    def autoscale(self):
        """Autoscale amplitudes of the channels
        """
        self._compute_autoscale = True
        self._update_data()

    def delete_time_marker(self, key = None):
        """Delete time marker. If key is not specified, all time markers are cleared.

        :param key: name of the time marker to delete, defaults to None
        :type key: str, optional
        """
        self.chart.delete_time_marker(key = key)

    @LogPerformances
    def downsample_based_on_screen(self, data_to_plot, time_span):
        """Downsample data to plot and time span based on screen

        :param data_to_plot: data to plot
        :type data_to_plot: list of array
        :param time_span: time coordinates
        :type time_span: list
        :return: data to plot and time span
        :rtype: list of array, list
        """
        available_pixels = self.width()
        decimation_index = math.ceil(len(time_span)/available_pixels)
        data_to_plot = [array[::decimation_index] for array in data_to_plot]
        time_span = time_span[::decimation_index]
        return data_to_plot, time_span
    
    @LogPerformances
    def downsample_based_on_screen_max_min(self, data_to_plot, time_span):
        """Downsample data to plot and time span based on screen

        :param data_to_plot: data to plot
        :type data_to_plot: list of array
        :param time_span: time coordinates
        :type time_span: list
        :return: data to plot and time span
        :rtype: list of array, list
        """
        available_pixels = self.width()
        decimation_index = math.ceil(len(time_span)/available_pixels)
        time_span = time_span[::decimation_index]
        time_span = [val for val in time_span for _ in range(2)]
        available_data = len(data_to_plot)
        data_to_plot = [self._slice_and_get_maxs_mins(arr=array, N=decimation_index) for array in data_to_plot]
        return data_to_plot, time_span
    
    @LogPerformances
    def downsample_based_on_screen_mean(self, data_to_plot, time_span):
        """Downsample data to plot and time span based on screen

        :param data_to_plot: data to plot
        :type data_to_plot: list of array
        :param time_span: time coordinates
        :type time_span: list
        :return: data to plot and time span
        :rtype: list of array, list
        """
        available_pixels = self.width()
        decimation_index = math.ceil(len(time_span)/available_pixels)
        time_span = time_span[::decimation_index]
        available_data = len(data_to_plot)
        data_to_plot = [self._slice_and_get_means(arr=array, N=decimation_index) for array in data_to_plot]
        return data_to_plot, time_span
    
    def enable_all_channels(self, enabled = True):
        """Enable all channels to be seen

        :param enabled: True if to enable, False otherwise, defaults to True
        :type enabled: bool, optional
        """
        self._update_enabled_disabled = True
        for scroll_child in self.scrollAreaWidgetContents.children():
            if isinstance(scroll_child, QtWidgets.QFrame):
                for i in scroll_child.children():
                    if isinstance(i, QtWidgets.QCheckBox):
                        i.setChecked(enabled)
        self._update_enabled_disabled = False
        self.update_enabled_channels()

    def increase_time_window(self, isIncrease):
        if isIncrease:
            self.spin_time_window.setValue(self.spin_time_window.value() + 1)
        else:
            self.spin_time_window.setValue(self.spin_time_window.value() - 1)
        self._update_data()

    def get_time_markers(self):
        """Get time markers

        :return: The dictionary containing all the active time markers.
        :rtype: dict
        """
        return self.chart.get_time_markers()
    
    def initialize_channels_components(self, channels):
        """Initialize channels components

        :param channels: list of channels to be plotted and controlled. Can be TMSiChannel or just the channel name as string
        :type channels: list[TMSiChannel] or list[str]
        """
        # remove any possible channel component
        channel_components = [i for i in dir(self) if i.startswith("component_channel_")]
        for cc in channel_components:
            getattr(self,cc).delete()
            self.__dict__.pop(cc, None)
        # initialize new components
        self._channel_names = {}
        self._channel_units = {}
        for i in range(len(channels)):
            if isinstance(channels[i], str):
                channel_name = channels[i]
                channel_unit = "a.u."
                enable = True
            else:
                channel_name = channels[i].get_channel_name()
                channel_unit = channels[i].get_channel_unit_name()
                if channels[i].get_channel_type().value <= 4:
                    enable = True
                else:
                    enable = False
            if hasattr(self,"component_channel_{}".format(i)):
                getattr(self,"component_channel_{}".format(i)).set_text("{}".format(channel_name))
                continue
            component = ChannelComponent(
                index = i,
                layout = self.layout_channels,
                widget = self.scrollAreaWidgetContents,
                connect_chb = lambda: self.update_enabled_channels(),
                checked_state = enable,
                connect_offset = lambda: self.update_offsets(),
                connect_scale = lambda: self.update_scales(),
                connect_combo = lambda: self.update_enabled_channels(),
                name = channel_name
            )
            setattr(self,"component_channel_{}".format(i), component)
            self._channel_names[i] = channel_name
            self._channel_units[i] = channel_unit
        # set compute autoscale to avoid the tentative to plot without offset available
        self._compute_autoscale = True
        self.update_enabled_channels()
        self.update_scales()
        self._compute_autoscale = False
        self.update_offsets()
        self.chart.update_y_ticks(
            list_names = self._filter_lists_to_plot(self._channel_names),
            list_offsets = self._filter_lists_to_plot(self._offsets),
            list_scales = self._filter_lists_to_plot(self._scales),
            list_units = self._filter_lists_to_plot(self._channel_units))

    def manual_scale(self):
        """Manual set of the scale value"""
        new_val = self.spin_amplitude.value()
        self._update_scales_disabled = True
        channel_components = [i for i in dir(self) if i.startswith("component_channel_")]
        for channel_component in channel_components:
            cmp = getattr(self,channel_component)
            cmp.set_scale(new_val)
        self._update_scales_disabled = False
        self.update_scales()
    
    def remove_offset(self):
        """Remove offset of the channels
        """
        self._compute_offset = True
        self._update_data()
        
    def set_tracks_range(self, min, length):
        self.chart.set_vertical_range(min = min, length = length)
    
    def set_time_ticks(self, time_values, time_ticks):
        chart_time_ticks = [[]]
        for i in range(len(time_values)):
            chart_time_ticks[0].append((time_values[i], str(time_ticks[i])))
        self.chart.set_time_ticks(chart_time_ticks)
    
    @LogPerformances
    def update_chart(self, data_to_plot, time_span = None):
        """Update chart

        :param data_to_plot: data to be plotted
        :type data_to_plot: list[list]
        :param time_span: time span for the channels (None to be automatically plotted in the range), defaults to None
        :type time_span: list, optional
        """
        if not self.is_chart_update_enabled:
            return
        if self._compute_autoscale or self._compute_offset:
            self._update_scales_disabled = True
            channel_components = [i for i in dir(self) if i.startswith("component_channel_")]
            scales = []
            offsets = []
            for n_channel in range(len(data_to_plot)):
                max_val = np.nanmax(data_to_plot[n_channel])
                min_val = np.nanmin(data_to_plot[n_channel])
                if self._compute_autoscale:
                    scale = (max_val-min_val)/2.0
                    if scale <= 1e-3:
                        scale = 1
                    scales.append(scale)
                offset = np.nanmean(data_to_plot[n_channel,-int(0.1*np.shape(data_to_plot)[1]):])
                offsets.append(offset)
            for n_channel in range(len(channel_components)):
                cmp = getattr(self, channel_components[n_channel])
                if self._compute_autoscale:
                    cmp.set_scale(scales[cmp.get_index()])
                cmp.set_offset(offsets[cmp.get_index()])
            self._update_scales_disabled = False
            self.update_offsets()
            self.update_scales()
            self.chart.update_y_ticks(
                list_names = self._filter_lists_to_plot(self._channel_names),
                list_offsets = self._filter_lists_to_plot(self._offsets),
                list_scales = self._filter_lists_to_plot(self._scales),
                list_units = self._filter_lists_to_plot(self._channel_units))
            self._compute_autoscale = False
            self._compute_offset = False
        for i in range(len(data_to_plot)):
            data_to_plot[i] = - (data_to_plot[i] - self._offsets[i]) / self._scales[i]
        # filter data to plot
        data_to_plot = self._filter_data_to_plot(data_to_plot)
        data_to_plot, time_span = self.downsample_based_on_screen(data_to_plot, time_span)
        self.chart.update_chart(data_to_plot, time_span)
        
    def update_colors(self):
        """Update color of the chart based on the channel component
        """
        colors = {}
        channel_components = [i for i in dir(self) if i.startswith("component_channel_")]
        for channel_component in channel_components:
            cmp = getattr(self,channel_component)
            colors[cmp.get_index()] = cmp.get_color()
        colors = [colors[i] for i in range(len(colors)) if i in self._enabled_channels]
        self.chart.setup_signals(n_signals=len(colors), colors=colors)

    def update_enabled_channels(self):
        """Update the enabled channels based on channel component
        """
        if self._update_enabled_disabled:
            return
        self._enabled_channels = []
        for scroll_child in self.scrollAreaWidgetContents.children():
            if isinstance(scroll_child, QtWidgets.QFrame):
                for i in scroll_child.children():
                    if isinstance(i, QtWidgets.QCheckBox):
                        if i.isChecked():
                            self._enabled_channels.append(int(i.objectName().split("_")[-1]))
        self.update_colors()
        if not self._compute_autoscale:
            self._update_data()
            self.chart.update_y_ticks(
                list_names = self._filter_lists_to_plot(self._channel_names),
                list_offsets = self._filter_lists_to_plot(self._offsets),
                list_scales = self._filter_lists_to_plot(self._scales),
                list_units = self._filter_lists_to_plot(self._channel_units))
        self._update_visible_tracks(new_max=len(self._enabled_channels))
        
    def update_offsets(self):
        """Update the offset based on channel component
        """
        if self._update_scales_disabled:
            return
        self._offsets = {}
        channel_components = [i for i in dir(self) if i.startswith("component_channel_")]
        for channel_component in channel_components:
            cmp = getattr(self,channel_component)
            self._offsets[cmp.get_index()] = cmp.get_offset()
        if not self._compute_autoscale:
            self._update_data()
            self.chart.update_y_ticks(
                list_names = self._filter_lists_to_plot(self._channel_names),
                list_offsets = self._filter_lists_to_plot(self._offsets),
                list_scales = self._filter_lists_to_plot(self._scales),
                list_units = self._filter_lists_to_plot(self._channel_units))
        
    def update_scales(self):
        """Update the scale based on channel component
        """
        if self._update_scales_disabled:
            return
        self._scales = {}
        channel_components = [i for i in dir(self) if i.startswith("component_channel_")]
        for channel_component in channel_components:
            cmp = getattr(self,channel_component)
            self._scales[cmp.get_index()] = cmp.get_scale()
        if not self._compute_autoscale:
            self._update_data()
            self.chart.update_y_ticks(
                list_names = self._filter_lists_to_plot(self._channel_names),
                list_offsets = self._filter_lists_to_plot(self._offsets),
                list_scales = self._filter_lists_to_plot(self._scales),
            list_units = self._filter_lists_to_plot(self._channel_units))

    def update_time_marker(self, time_value, key = None):
        """Update time marker

        :param time_value: position of the marker
        :type time_value: float
        :param key: name of the marker, defaults to None
        :type key: str or float, optional
        """
        self.chart.update_time_marker(time_value = time_value, key = key)
    
    def update_time_ticks(self, start_time, end_time):
        """Update time ticks

        :param start_time: initial time value
        :type start_time: float
        :param end_time: final time tick
        :type end_time: float
        """
        self.chart.update_time_ticks(start_time=start_time, end_time=end_time)

    def update_time_window(self):
        self.window_size = self.spin_time_window.value()
        self.chart.set_time_range(self.window_size)
        if self._update_viewer_time_scrollbar_callback is not None:
            self._update_viewer_time_scrollbar_callback()
    
    def _connect_widgets_to_functions(self):
        self.btn_enable_all_channels.clicked.connect(lambda: self.enable_all_channels(True))
        self.btn_disable_all_channels.clicked.connect(lambda: self.enable_all_channels(False))
        self.btn_autoscale.clicked.connect(self.autoscale)
        self.spin_amplitude.valueChanged.connect(self.manual_scale)
        self.spin_time_window.valueChanged.connect(self.update_time_window)
        self.btn_time_window_increase.clicked.connect(lambda: self.increase_time_window(True))
        self.btn_time_window_decrease.clicked.connect(lambda: self.increase_time_window(False))

    def _filter_data_to_plot(self, data_to_plot):
        data_to_plot = [data_to_plot[row] for row in range(len(data_to_plot)) if row in self._enabled_channels]
        return data_to_plot
    
    def _filter_lists_to_plot(self, list_to_filter):
        return [list_to_filter[i] for i in range(len(list_to_filter)) if i in self._enabled_channels]
    
    def _local_setup_ui(self):
        super()._local_setup_ui()
        self.group_window_size.setVisible(True)
        self.group_window_size.setEnabled(True)
        self.scrollbar_tracks.setVisible(False)
        self.scrollbar_tracks.setEnabled(True)
        self.group_plotter_zoom.setVisible(True)
        self.group_plotter_zoom.setEnabled(True)
        self.spin_plotter_zoom.valueChanged.connect(lambda: self._update_visible_tracks(new_max = None))
        self.scrollbar_tracks.valueChanged.connect(self._update_tracks_range)
                        
    @LogPerformances
    def _slice_and_get_maxs_mins(self, arr, N):
        if len(arr) % N == 0:
            slices = arr.reshape(-1, N)
        else:
            available_data = (len(arr) // N) * N
            slices = arr[:available_data].reshape(-1, N)
        
        max_values = np.max(slices, axis=1)
        min_values = np.min(slices, axis=1)
        return np.array([x for pair in zip(max_values, min_values) for x in pair])
    
    @LogPerformances
    def _slice_and_get_means(self, arr, N):
        if len(arr) % N == 0:
            slices = arr.reshape(-1, N)
        else:
            available_data = (len(arr) // N) * N
            slices = arr[:available_data].reshape(-1, N)
        
        mean_values = np.mean(slices, axis=1)
        return mean_values
    
    def _update_data(self):
        if self._get_data_callback is not None:
            self._get_data_callback()

    def _update_tracks_range(self):
        max = self.spin_plotter_zoom.maximum() * 100
        val = self.spin_plotter_zoom.value() * 100
        length =  round(max/val)
        self.set_tracks_range(
            min = self.scrollbar_tracks.value(),
            length = length)
        return

    def _update_visible_tracks(self, new_max = None):
        if new_max is not None:
            if new_max < 1:
                new_max = 1
            self.spin_plotter_zoom.setMaximum(new_max)
        max = self.spin_plotter_zoom.maximum()
        val = self.spin_plotter_zoom.value()
        visible_tracks =  round(max/val)
        available_tracks = max
        self.scrollbar_tracks.setMaximum(available_tracks - visible_tracks)
        self.scrollbar_tracks.setVisible(self.scrollbar_tracks.maximum() != 0)
        self._update_tracks_range()