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
 * @file wavex_info.py
 * @brief WaveX device info.
 *
 */


'''

class WaveXInfo():
    def __init__(self):
        self.__device_name = "Unknown"
        self.__serial_number = "Undefined"
        self.__num_channels = 0
        self.__num_active_channels = 0
        self.__dev_mode = None
        self.__dev_type = None

    def get_name(self):
        return self.__device_name
    
    def get_num_active_channels(self):
        return self.__num_active_channels
    
    def get_num_channels(self):
        return self.__num_channels
    
    def get_serial_number(self):
        return self.__serial_number
    
    def set_device_mode(self, dev_mode):
        self.__dev_mode = dev_mode

    def set_device_type(self, dev_type):
        self.__dev_type = dev_type
    
    def set_num_active_channels(self, num_active_channels):
        self.__num_active_channels = num_active_channels

    def set_num_channels(self, num_channels):
        self.__num_channels = num_channels