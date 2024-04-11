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
 * @file wavex_channel.py
 * @brief WaveX device channel.
 *
 */


'''

from TMSiSDK.device.tmsi_channel import TMSiChannel

class WaveXChannel(TMSiChannel):
    def set_channel_information(self,
                index,
                sensor_number,
                enabled,
                sensor_model,
                sensor_mode,
                accelerometer_full_scale,
                gyroscope_full_scale,
                signal_type,
                unit_name):
        self._index = index
        self._sensor_number = sensor_number
        self._enabled = enabled
        self._sensor_model = sensor_model
        self._sensor_mode = sensor_mode
        self._accelerometer_fs = accelerometer_full_scale
        self._gyroscope_fs = gyroscope_full_scale
        self._unit_name = unit_name
        self._signal_type = signal_type
        self._alt_name = "sensor {} {}".format(self._sensor_number, self._signal_type, self._sensor_model)
        
    def enable(self, enabled = True):
        self._enabled = enabled
    
    def get_signal_type(self):
        return self._signal_type
    
    def get_sensor_mode(self):
        return self._sensor_mode
    
    def get_sensor_model(self):
        return self._sensor_model
    
    def get_sensor_number(self):
        return self._sensor_number
    
    def is_enabled(self):
        return self._enabled
    
    def __str__(self) -> str:
        return self.get_channel_name()
        