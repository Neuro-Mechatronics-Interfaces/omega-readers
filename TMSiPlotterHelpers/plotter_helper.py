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
 * @file ${plotter_helper.py}
 * @brief This file is a general helper to make a plotter in the GUI
 *
 */
'''

import numpy as np
from TMSiBackend.buffer import Buffer

class PlotterHelper:
    def __init__(self, device, monitor_class, consumer_thread_class):
        self.device = device
        self.sampling_frequency = self.device.get_device_sampling_frequency()
        self.monitor_class = monitor_class
        self.consumer_thread_class = consumer_thread_class
        self._last_pointer = None        

    def callback(self, response):
        print("callback plotter helper")

    @staticmethod
    def generate_time_ticks(elapsed_time, window_size):
        time_ticks = [i for i in range(window_size + 1)]
        if elapsed_time > window_size:
            new_max = int((elapsed_time // window_size) * window_size)
            time_ticks = [i for i in range(new_max - window_size, new_max + 1)]
            for i in range(len(time_ticks)):
                if time_ticks[i] <= elapsed_time - window_size:
                        time_ticks[i] = time_ticks[i] + window_size
        time_values = [i for i in range(window_size + 1)]
        return time_values, time_ticks

    @staticmethod
    def generate_new_plotting_buffer(plotting_buffer, main_buffer, elapsed_time, window_size, sampling_frequency, last_counter):
        secondary_buffer_generation_start_second = int(elapsed_time // window_size) * window_size
        secondary_buffer_generation_start = secondary_buffer_generation_start_second * sampling_frequency
        secondary_buffer_generation_start_position = secondary_buffer_generation_start % main_buffer.size_buffer
        secondary_buffer_generation_stop_position = int(last_counter) % main_buffer.size_buffer
        dataset_to_copy = []
        if secondary_buffer_generation_start_position < secondary_buffer_generation_stop_position:
            dataset_to_copy.extend(main_buffer.dataset[:, secondary_buffer_generation_start_position: secondary_buffer_generation_stop_position].tolist())
        elif secondary_buffer_generation_start_position > secondary_buffer_generation_stop_position:
            if secondary_buffer_generation_stop_position == 0:
                dataset_to_copy.extend(main_buffer.dataset[:, secondary_buffer_generation_start_position: secondary_buffer_generation_stop_position].tolist())
            else:
                initial_part = main_buffer.dataset[:, secondary_buffer_generation_start_position:]
                final_part = main_buffer.dataset[:, :secondary_buffer_generation_stop_position]
                extended_array = np.hstack((initial_part, final_part))
                dataset_to_copy.extend(extended_array.tolist())
        plotting_buffer = Buffer(window_size * sampling_frequency)
        plotting_buffer.append(dataset_to_copy)
        last_pointer = main_buffer.pointer_buffer
        return plotting_buffer, last_pointer

    @staticmethod
    def get_plotting_buffer(plotting_buffer, main_buffer, elapsed_time, window_size, sampling_frequency, last_counter, last_pointer):
        if plotting_buffer is None:
            return PlotterHelper.generate_new_plotting_buffer(plotting_buffer, main_buffer, elapsed_time, window_size, sampling_frequency, last_counter)
        else:
            return PlotterHelper.update_current_plotting_buffer(plotting_buffer, main_buffer, last_pointer)

    def initialize(self):
        print("initialize function plotter helper")

    def monitor_function(self):
        print("monitor function plotter helper")

    def on_error(self, response):
        print("on_error plotter helper")

    def start(self, measurement_type):
        raise NotImplementedError("This method must be implemented for each plotter helper")

    def stop(self):
        self.monitor.stop()
        self.consumer.close()
        self.device.stop_measurement()

    @staticmethod
    def update_current_plotting_buffer(plotting_buffer, main_buffer, last_pointer):
        current_pointer = main_buffer.pointer_buffer
        if last_pointer < current_pointer:
            samples = main_buffer.dataset[:,last_pointer:current_pointer]
        elif last_pointer == current_pointer:
            return
        else:
            samples = np.concatenate(
                (main_buffer.dataset[:,last_pointer:],
                main_buffer.dataset[:,:current_pointer]),
                axis=1)
        plotting_buffer.append(samples)
        last_pointer = current_pointer
        return plotting_buffer, last_pointer
