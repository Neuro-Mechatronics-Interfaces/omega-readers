'''
(c) 2024 Twente Medical Systems International B.V., Oldenzaal The Netherlands

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
 * @file signal_plotter_helper_wave_x.py
 * @brief This file is used as helper to make a signal plotter in the GUI
 *
 */


'''

import sys
from os.path import join, dirname, realpath
Plugin_dir = dirname(realpath(__file__)) # directory of this file
sys.path.append(Plugin_dir)

from TMSiSDK import TMSiLogger
from TMSiBackend.buffer import Buffer

from TMSiPlotterHelpers.signal_plotter_helper import SignalPlotterHelper
from wavex.measurements.measurement_type import MeasurementType

class SignalPlotterHelperWaveX(SignalPlotterHelper):
    @staticmethod
    def get_plotting_buffer(plotting_buffer, main_buffer, elapsed_time, window_size, sampling_frequency, last_counter, last_pointer):
        if plotting_buffer is None:
            plotting_buffer = Buffer(window_size * sampling_frequency)
            last_pointer = 0
            return plotting_buffer, last_pointer
        else:
            return SignalPlotterHelper.update_current_plotting_buffer(plotting_buffer, main_buffer, last_pointer)

    def initialize(self):
        super().initialize()
        self.measurement_type = MeasurementType.WAVEX_SIGNAL

    def monitor_function(self):
        TMSiLogger().debug("monitor call")
        return super().monitor_function()