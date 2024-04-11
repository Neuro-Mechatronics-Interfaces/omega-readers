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
 * @file wavex_device.py
 * @brief WaveX device object.
 *
 */


'''

import os
from pkg_resources import resource_filename
import clr
# Get the path to the images directory
current_dir = resource_filename(__name__, '')
wave_x_assembly_path = os.path.join(current_dir, "./bin/WaveX")
clr.AddReference(wave_x_assembly_path)
from WaveX import DaqSystem
import WaveX.Common.Definitions as Definitions
from WaveX.Common.Definitions import DeviceState


from TMSiSDK.device.tmsi_device import TMSiDevice
from TMSiSDK.tmsi_errors.error import TMSiError, TMSiErrorCode
from TMSiSDK import TMSiLogger

from . import allowed_versions
from .wavex_structures.wavex_info import WaveXInfo
from .wavex_structures.wavex_config import WaveXConfig
from .wavex_structures.wavex_channel import WaveXChannel
from .measurements.measurement_type import MeasurementType

EMG_CHANNELS = 1
IMU_CHANNELS = 4
ACC_CHANNELS = 3
GYR_CHANNELS = 3
MAG_CHANNELS = 3
TRIGGER_CHANNELS = 1

class WaveXDevice(TMSiDevice):
    __DEVICE_TYPE = "WAVEX"

    def __init__(self) -> None:
        self.__dev = None
        self.__callback = None

    def close(self) -> None:
        TMSiLogger().info(message= "Closing device...")
        if self.__dev is None:
            TMSiLogger().warning("Device already closed")
            return
        self.__dev = None
        TMSiLogger().info(message= "Device Closed")

    def get_device_active_channels(self) -> list:
        """Gets the list of active channels.

        :raises TMSiError: TMSiErrorCode.device_error if get channels from the device fails.
        :raises TMSiError: TMSiErrorCode.device_not_connected if not connected.
        :return: The list of channels
        :rtype: list[WaveXChannel]
        """
        return self.__config.get_active_channels()
    
    def get_device_active_acc_channels(self) -> list:
        """Gets the list of active acceleration channels.

        :raises TMSiError: TMSiErrorCode.device_error if get channels from the device fails.
        :raises TMSiError: TMSiErrorCode.device_not_connected if not connected.
        :return: The list of acceleration channels
        :rtype: list[WaveXChannel]
        """
        return self.__config.get_active_acc_channels()
    
    def get_device_active_emg_channels(self) -> list:
        """Gets the list of active emg channels.

        :raises TMSiError: TMSiErrorCode.device_error if get channels from the device fails.
        :raises TMSiError: TMSiErrorCode.device_not_connected if not connected.
        :return: The list of emg channels
        :rtype: list[WaveXChannel]
        """
        return self.__config.get_active_emg_channels()
    
    def get_device_active_gyr_channels(self) -> list:
        """Gets the list of active gyroscopic channels.

        :raises TMSiError: TMSiErrorCode.device_error if get channels from the device fails.
        :raises TMSiError: TMSiErrorCode.device_not_connected if not connected.
        :return: The list of gyroscopic channels
        :rtype: list[WaveXChannel]
        """
        return self.__config.get_active_gyr_channels()
    
    def get_device_active_imu_channels(self) -> list:
        """Gets the list of active imu channels.

        :raises TMSiError: TMSiErrorCode.device_error if get channels from the device fails.
        :raises TMSiError: TMSiErrorCode.device_not_connected if not connected.
        :return: The list of imu channels
        :rtype: list[WaveXChannel]
        """
        return self.__config.get_active_imu_channels()
    
    def get_device_active_mag_channels(self) -> list:
        """Gets the list of active magnetic channels.

        :raises TMSiError: TMSiErrorCode.device_error if get channels from the device fails.
        :raises TMSiError: TMSiErrorCode.device_not_connected if not connected.
        :return: The list of magnetic channels
        :rtype: list[WaveXChannel]
        """
        return self.__config.get_active_mag_channels()
    
    def get_device_active_trigger_channels(self) -> list:
        """Gets the list of active trigger channels.

        :raises TMSiError: TMSiErrorCode.device_error if get channels from the device fails.
        :raises TMSiError: TMSiErrorCode.device_not_connected if not connected.
        :return: The list of trigger channels
        :rtype: list[WaveXChannel]
        """
        return self.__config.get_active_trigger_channels()
    
    def get_device_channels(self) -> list:
        """Gets the list of channels.

        :raises TMSiError: TMSiErrorCode.device_error if get channels from the device fails.
        :raises TMSiError: TMSiErrorCode.device_not_connected if not connected.
        :return: The list of channels
        :rtype: list[WaveXChannel]
        """
        return self.__config.get_channels()
    
    def get_device_name(self):
        """Get name of the device

        :return: name of the device
        :rtype: str
        """
        return self.__info.get_name()

    def get_device_sampling_frequency(self) -> int:
        """Gets the sampling frequency.

        :return: sampling frequency.
        :rtype: int
        """
        return self.__config.get_sampling_frequency()

    def get_device_serial_number(self) -> int:
        """Gets the serial number of the device.

        :return: serial number of the device.
        :rtype: int
        """
        return self.__info.get_serial_number()
    
    def get_device_state(self) -> DeviceState:
        if self.__dev is not None:
            return self.__dev.get_State()
        DaqSystem().get_State()
    
    def get_device_type(self) -> str:
        return WaveXDevice.__DEVICE_TYPE
    
    def get_driver_version() -> str:
        version = DaqSystem().get_SoftwareVersion()
        return "{}.{}.{}.{}".format(version.Major, version.Minor, version.Build, version.Revision)

    def get_id(self):
        return id(self)
    
    def get_num_active_channels(self) -> int:
        """Returns the number of active channels of the device.

        :return: number of active channels of the device.
        :rtype: int
        """
        return self.__info.get_num_active_channels()
    
    def get_num_channels(self) -> int:
        """Returns the number of channels of the device.

        :return: number of channels of the device.
        :rtype: int
        """
        return self.__info.get_num_channels()
    
    def open(self) -> None:
        if WaveXDevice.get_driver_version() not in allowed_versions:
            TMSiLogger().warning(message = "Impossible to open device, dll version not compatible.")
            raise TMSiError(error_code = TMSiErrorCode.missing_dll, 
                            message = "DLL version not compatible.")
        TMSiLogger().info(message = "Opening device...")
        self.__dev = DaqSystem()
        if self.get_device_state() == DeviceState.NotConnected:
            TMSiLogger().warning(message = "Impossible to open device")
            self.close()
            raise TMSiError(error_code = TMSiErrorCode.device_not_connected)
        self.__dev.DisableSensor(0)
        self.__initialize_config_info()
        TMSiLogger().info(message = "Device opened")

    def refresh_display(self):
        self.__dev.UpdateDisplay()
    
    def set_data_available_callback(self, callback):
        if self.__callback is not None:
            self.__remove_callback(self)
        self.__callback = callback
        self.__dev.DataAvailable += self.__callback
    
    def set_device_sampling_config(self,
        IMU_acq_type = None,
        EMG_acq_type = None,
        EMG_IMU_acq_type = None):
        config = self.__dev.CaptureConfiguration()
        if IMU_acq_type is not None:
            config.IMU_AcqXType = Definitions.ImuAcqXType(IMU_acq_type.value)
        if EMG_acq_type is not None:
            config.EMG_AcqXType = Definitions.EmgAcqXType(EMG_acq_type.value)
        if EMG_IMU_acq_type is not None:
            config.EMG_IMU_AcqXType = Definitions.EmgImuAcqXType(EMG_IMU_acq_type.value)
        self.__dev.ConfigureCapture(config)
        self.__config.set_sampling_modes(
            emg_imu_mode=config.EMG_IMU_AcqXType,
            emg_mode=config.EMG_AcqXType,
            imu_mode=config.IMU_AcqXType)
    
    def set_device_sampling_request(self, start, thread_refresh = None):
        if start:
            self.__start_capturing(thread_refresh = thread_refresh)
        else:
            self.__stop_capturing()

    def set_device_sensor_configuration(self, 
            sensor_number, 
            enable = None, 
            mode = None, 
            model = None, 
            acc_full_scale = None, 
            gyr_full_scale = None): 
        sensor = self.__dev.SensorConfiguration(sensor_number)
        if sensor is None:
            raise TMSiError(error_code=TMSiErrorCode.api_incorrect_argument, message="sensor_number must be included between 0 (all sensors) and num sensors.")
        if mode is not None:
            sensor.SensorMode = Definitions.SensorMode(mode.value)
        if model is not None:
            sensor.SensorModel = Definitions.SensorModel(model.value)
        if acc_full_scale is not None:
            sensor.AccelerometerFullScale = Definitions.AccelerometerFullScale(acc_full_scale.value)
        if gyr_full_scale is not None:
            sensor.GyroscopeFullScale = Definitions.GyroscopeFullScale(gyr_full_scale.value)
        if sensor_number > 0:
            for channel in self.get_device_channels():
                if channel.get_sensor_number() == sensor_number:
                    if enable is None:
                        enableSensor = channel.is_enabled()
                    elif enable is False:
                        enableSensor = False
                    else:
                        enableSensor = self.__check_channel_mode_compatibility(channel, sensor.SensorMode)
                    channel.set_channel_information(
                        index = channel.get_channel_index(),
                        sensor_number = channel.get_sensor_number(),
                        enabled = enableSensor,
                        sensor_model = sensor.SensorModel,
                        sensor_mode = sensor.SensorMode,
                        accelerometer_full_scale = sensor.AccelerometerFullScale,
                        gyroscope_full_scale = sensor.GyroscopeFullScale,
                        signal_type = channel.get_signal_type(),
                        unit_name = channel.get_channel_unit_name())
        else:
            for channel in self.get_device_channels():
                if enable is None:
                    enableSensor = channel.is_enabled()
                elif enable is False:
                    enableSensor = False
                else:
                    enableSensor = self.__check_channel_mode_compatibility(channel, sensor.SensorMode)
                channel.set_channel_information(
                    index = channel.get_channel_index(),
                    sensor_number = channel.get_sensor_number(),
                    enabled = enableSensor,
                    sensor_model = sensor.SensorModel,
                    sensor_mode = sensor.SensorMode,
                    accelerometer_full_scale = sensor.AccelerometerFullScale,
                    gyroscope_full_scale = sensor.GyroscopeFullScale,
                    signal_type = channel.get_signal_type(),
                    unit_name = channel.get_channel_unit_name())
        self.__info.set_num_active_channels(len(self.__config.get_active_channels()))
        self.__dev.ConfigureSensor(sensor, sensor_number)
        if enable is not None:
            if enable:
                self.__dev.EnableSensor(sensor_number)
            else:
                self.__dev.DisableSensor(sensor_number)

    def start_measurement(self, measurement_type: MeasurementType, thread_refresh = Definitions.DataAvailableEventPeriod.ms_10):
        """Starts the measurement requested.

        :param measurement_type: measurement to start
        :type measurement_type: MeasurementType
        :param thread_refresh: refresh time for sampling and conversion threads, defaults to 100 ms.
        :type thread_refresh: DataAvailableEventPeriod, optional.
        """
        if not isinstance(thread_refresh, Definitions.DataAvailableEventPeriod):
            thread_refresh = Definitions.DataAvailableEventPeriod(thread_refresh.value)
        self.__measurement = measurement_type(self)
        self.__measurement.set_sampling_pause(thread_refresh)
        self.__measurement.start()

    def stop_measurement(self):
        self.__measurement.stop()
    
    def __check_channel_mode_compatibility(self, channel, sensor_mode):
        sig_type = channel.get_signal_type()
        mode_type = str(sensor_mode)
        if "EMG" in sig_type:
            if "EMG" in mode_type:
                return True
        else:
            if "INERTIAL" in mode_type:
                return True
        return False

    def __initialize_config_info(self):
        self.__info = WaveXInfo()
        self.__config = WaveXConfig()
        self.__info.set_num_channels(num_channels = self.__dev.InstalledSensors)

        emg_channels = []
        imu_channels = []
        acc_channels = []
        gyr_channels = []
        mag_channels = []
        trigger_channels = []
        for i in range(self.__info.get_num_channels()):
            sensor_config = self.__dev.SensorConfiguration(i+1)
            channel = WaveXChannel()
            channel.set_channel_information(
                index = i,
                sensor_number = i + 1,
                enabled = False,
                sensor_model = sensor_config.SensorModel,
                sensor_mode = sensor_config.SensorMode,
                accelerometer_full_scale = sensor_config.AccelerometerFullScale,
                gyroscope_full_scale = sensor_config.GyroscopeFullScale,
                signal_type = "EMG signal",
                unit_name = "\u03BCVolt")
            emg_channels.append(channel)
            for n_acc in range(ACC_CHANNELS):
                channel = WaveXChannel()
                channel.set_channel_information(
                    index = i * ACC_CHANNELS + n_acc,
                    sensor_number = i + 1,
                    enabled = False,
                    sensor_model = sensor_config.SensorModel,
                    sensor_mode = sensor_config.SensorMode,
                    accelerometer_full_scale = sensor_config.AccelerometerFullScale,
                    gyroscope_full_scale = sensor_config.GyroscopeFullScale,
                    signal_type =  "ACC signal {}".format(n_acc),
                    unit_name = "g")
                acc_channels.append(channel)
            for n_gyr in range(GYR_CHANNELS):
                channel = WaveXChannel()
                channel.set_channel_information(
                    index = i * GYR_CHANNELS + n_gyr,
                    sensor_number = i + 1,
                    enabled = False,
                    sensor_model = sensor_config.SensorModel,
                    sensor_mode = sensor_config.SensorMode,
                    accelerometer_full_scale = sensor_config.AccelerometerFullScale,
                    gyroscope_full_scale = sensor_config.GyroscopeFullScale,
                    signal_type =  "GYR signal {}".format(n_gyr),
                    unit_name = "D/s")
                gyr_channels.append(channel)
            for n_mag in range(MAG_CHANNELS):
                channel = WaveXChannel()
                channel.set_channel_information(
                    index = i * MAG_CHANNELS + n_mag,
                    sensor_number = i + 1,
                    enabled = False,
                    sensor_model = sensor_config.SensorModel,
                    sensor_mode = sensor_config.SensorMode,
                    accelerometer_full_scale = sensor_config.AccelerometerFullScale,
                    gyroscope_full_scale = sensor_config.GyroscopeFullScale,
                    signal_type =  "MAG signal {}".format(n_mag),
                    unit_name = "\u03BCT")
                mag_channels.append(channel)
        for n_trigger in range(TRIGGER_CHANNELS):
            channel = WaveXChannel()
            channel.set_channel_information(
                index = -(n_trigger + 1),
                sensor_number = -1,
                enabled = True,
                sensor_model = "trigger",
                sensor_mode = None,
                accelerometer_full_scale = None,
                gyroscope_full_scale = None,
                signal_type =  "TRIGGER signal {}".format(n_trigger),
                unit_name = "a.u.")
            trigger_channels.append(channel)
        self.__config.set_channels(
            emg_channels = emg_channels, 
            imu_channels = imu_channels, 
            gyr_channels = gyr_channels, 
            mag_channels = mag_channels, 
            acc_channels = acc_channels,
            trigger_channels = trigger_channels)
        acq_modes = self.__dev.CaptureConfiguration()
        self.__config.set_sampling_modes(
            emg_mode = acq_modes.EMG_AcqXType,
            emg_imu_mode = acq_modes.EMG_IMU_AcqXType,
            imu_mode = acq_modes.IMU_AcqXType)
        self.__info.set_device_mode(dev_mode = self.__dev.Mode)
        self.__info.set_device_type(dev_type=self.__dev.Type)
    
    def __remove_callback(self):
        self.__dev.DataAvailable -= self.__callback
        self.__callback = None

    def __start_capturing(self, thread_refresh):
        self.__dev.StartCapturing(thread_refresh)

    def __stop_capturing(self):
        self.__dev.StopCapturing()
        self.__remove_callback()
    
    