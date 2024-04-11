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
 * @file wavex_config.py
 * @brief WaveX device config.
 *
 */


'''

FREQ_EMG_2K = 2000

class WaveXConfig():
    def __init__(self):
        self.__emg_channels = []

    def get_active_channels(self):
        active_channels = []
        active_channels.extend(self.get_active_emg_channels())
        active_channels.extend(self.get_active_imu_channels())
        active_channels.extend(self.get_active_acc_channels())
        active_channels.extend(self.get_active_gyr_channels())
        active_channels.extend(self.get_active_mag_channels())
        active_channels.extend(self.get_active_trigger_channels())
        return active_channels
    
    def get_active_acc_channels(self):
        return [i for i in self.__acc_channels if i.is_enabled()]
    
    def get_active_emg_channels(self):
        return [i for i in self.__emg_channels if i.is_enabled()]
    
    def get_active_gyr_channels(self):
        return [i for i in self.__gyr_channels if i.is_enabled()]
    
    def get_active_imu_channels(self):
        return [i for i in self.__imu_channels if i.is_enabled()]
    
    def get_active_mag_channels(self):
        return [i for i in self.__mag_channels if i.is_enabled()]
    
    def get_active_trigger_channels(self):
        return self.__trigger_channels
    
    def get_channels(self):
        channels = []
        channels.extend(self.__emg_channels)
        channels.extend(self.__imu_channels)
        channels.extend(self.__acc_channels)
        channels.extend(self.__gyr_channels)
        channels.extend(self.__mag_channels)
        channels.extend(self.__trigger_channels)
        return channels
    
    def get_acc_channels(self):
        channels = []
        channels.extend(self.__acc_channels)
        return channels
    
    def get_emg_channels(self):
        channels = []
        channels.extend(self.__emg_channels)
        return channels
    
    def get_gyr_channels(self):
        channels = []
        channels.extend(self.__gyr_channels)
        return channels
    
    def get_imu_channels(self):
        channels = []
        channels.extend(self.__imu_channels)
        return channels
    
    def get_mag_channels(self):
        channels = []
        channels.extend(self.__mag_channels)
        return channels
    
    def get_trigger_channels(self):
        channels = []
        channels.extend(self.__trigger_channels)
        return channels
    
    def get_sampling_frequency(self):
        sampling_frequency = None
        for channel in self.get_active_channels():
            sensor_mode = str(channel.get_sensor_mode())
            if "EMG" in sensor_mode:
                return FREQ_EMG_2K
            else:
                sampling_frequency = self.__imu_sampling_frequency
        if sampling_frequency is not None:
            return sampling_frequency
        return FREQ_EMG_2K
    
    def set_channels(self, emg_channels = [], imu_channels = [], acc_channels = [], gyr_channels = [], mag_channels = [], trigger_channels = []):
        self.__emg_channels = emg_channels
        self.__imu_channels = imu_channels
        self.__acc_channels = acc_channels
        self.__gyr_channels = gyr_channels
        self.__mag_channels = mag_channels
        self.__trigger_channels = trigger_channels

    def set_sampling_modes(self, emg_mode, emg_imu_mode, imu_mode):
        self.__emg_sampling_mode = emg_mode
        self.__emg_imu_sampling_mode = emg_imu_mode
        self.__imu_sampling_mode = imu_mode
        self.__imu_sampling_frequency = str(self.__imu_sampling_mode).split('_')[-1]
        self.__imu_sampling_frequency = ''.join(c for c in self.__imu_sampling_frequency if c.isdigit())
        self.__imu_sampling_frequency = int(self.__imu_sampling_frequency)
