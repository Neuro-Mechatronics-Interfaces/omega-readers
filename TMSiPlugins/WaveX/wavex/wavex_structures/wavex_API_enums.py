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
 * @file wavwx_API_enums.py
 * @brief Enums for API of WaveX
 *
 */


'''

from enum import Enum, unique

@unique
class SensorMode(Enum):
    EMG_ACC = 0
    INERTIAL = 1
    ANALOG_GP = 2
    FSW_SENSOR = 3
    EMG_INERTIAL = 4
    EMG = 5
    
@unique
class ImuAcqXType(Enum):
    RawAccGyroMagData_400Hz = 0
    RawAccGyroData_500Hz = 1
    Fused6xData_400Hz = 2
    Fused9xData_400Hz = 3
    Mixed6xData_200Hz = 4
    Mixed9xData_200Hz = 5

@unique
class EmgAcqXType(Enum):
    Emg_2kHz = 0

@unique
class EmgImuAcqXType(Enum):
    Emg_2kHz = 0
    Emg_4kHz = 1
    Emg_2kHz_RawAccGyroMagData_100Hz = 2
    Emg_2kHz_RawAccGyroData_200Hz = 3
    Emg_2kHz_Fused6xData_100Hz = 4
    RawAccGyroMagData_400Hz = 5
    RawAccGyroData_500Hz = 6
    Fused6xData_400Hz = 7
    Fused9xData_400Hz = 8
    Mixed6xData_200Hz = 9
    Mixed9xData_200Hz = 10

@unique
class SensorModel(Enum):
    Undefined = 0
    Mini_Emg = 1
    Imu = 2
    Mini_EmgImu = 3
    Pico_Lite = 4

@unique
class GyroscopeFullScale(Enum):
    dps_250 = 0
    dps_500 = 1
    dps_1000 = 2
    dps_2000 = 3

@unique
class AccelerometerFullScale(Enum):
    g_2 = 0
    g_4 = 1
    g_8 = 2
    g_16 = 3

@unique
class DataAvailableEventPeriod(Enum):
    ms_100 = 0
    ms_50 = 1
    ms_25 = 2
    ms_10 = 3

@unique
class SignalType(Enum):
    EMG = "EMG signal"
    IMU = "IMU signal"
    ACC = "ACC signal"
    GYR = "GYR signal"
    MAG = "MAG signal"