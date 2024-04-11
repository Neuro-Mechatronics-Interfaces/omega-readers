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
 * @file signal_measurement.py
 * @brief WaveX signal measurement object
 *
 */


'''

import numpy as np

from TMSiSDK import TMSiLogger, TMSiLoggerActivity
from TMSiSDK.tmsi_utilities.decorators import LogPerformances
from TMSiSDK.device.tmsi_measurement import TMSiMeasurement
from TMSiSDK.sample_data_server.sample_data import SampleData
from TMSiSDK.sample_data_server.sample_data_server import SampleDataServer
from TMSiSDK.tmsi_utilities import support_functions

import WaveX.Common.Definitions as Definitions

class SignalMeasurement(TMSiMeasurement):
    """Class to handle the Signal measurements."""
    def __init__(self, dev, name = "Signal Measurement"):
        """Initialize the Signal measurement.

        :param dev: Device to measure from.
        :type dev: TMSiDevice
        :param name: name of the measurement, defaults to "Signal Measurement"
        :type name: str, optional
        """
        self._dev = dev
        self._name = name
        self._sampling_thread = None
        self._thread_refresh = Definitions.DataAvailableEventPeriod.ms_10
        self.__trigger_active = False

    def set_sampling_pause(self, thread_refresh):
        self._thread_refresh = thread_refresh
    
    def start(self):
        # define which channels will need to be read:
        self.active_emg_indices = [i.get_channel_index() for i in self._dev.get_device_active_emg_channels()]
        TMSiLogger().debug("active_emg: {}".format(self.active_emg_indices))
        self.active_imu_indices = [i.get_channel_index() for i in self._dev.get_device_active_imu_channels()]
        TMSiLogger().debug("active_imu: {}".format(self.active_imu_indices))
        self.active_acc_indices = [i.get_channel_index() for i in self._dev.get_device_active_acc_channels()]
        TMSiLogger().debug("active_acc: {}".format(self.active_acc_indices))
        self.active_gyr_indices = [i.get_channel_index() for i in self._dev.get_device_active_gyr_channels()]
        TMSiLogger().debug("active_gyr: {}".format(self.active_gyr_indices))
        self.active_mag_indices = [i.get_channel_index() for i in self._dev.get_device_active_mag_channels()]
        TMSiLogger().debug("active_mag: {}".format(self.active_mag_indices))
        

        TMSiLoggerActivity().log("{}->>WAVEX-SDK: add callback function".format(self.get_name()))
        self._dev.set_data_available_callback(callback = self._sampling_function)
        TMSiLoggerActivity().log("{}->>WAVEX-SDK: set device sampling request ON".format(self.get_name()))
        self._dev.set_device_sampling_request(start = True, thread_refresh = self._thread_refresh)

    def stop(self):
        TMSiLoggerActivity().log("{}->>WAVEX-SDK: set device sampling request OFF".format(self.get_name()))
        self._dev.set_device_sampling_request(start = False)

    @LogPerformances
    def _sampling_function(self, sender, obj):
        emg_samples = np.array(obj.EmgSamples, dtype=np.float32)
        imu_samples = np.array(obj.ImuSamples, dtype=np.float32)
        accelerometer_samples = np.array(obj.AccelerometerSamples, dtype=np.float32)
        gyroscope_samples = np.array(obj.GyroscopeSamples, dtype=np.float32)
        magnetometer_samples = np.array(obj.MagnetometerSamples, dtype=np.float32)
        scan_number = obj.ScanNumber

        shape_imu_samples = np.shape(imu_samples)
        shape_acc_samples = np.shape(accelerometer_samples)
        shape_gyr_samples = np.shape(gyroscope_samples)
        shape_mag_samples = np.shape(magnetometer_samples)
        
        num_imu_channels = shape_imu_samples[0] * shape_imu_samples[1]
        num_acc_channels = shape_acc_samples[0] * shape_acc_samples[1]
        num_gyr_channels = shape_gyr_samples[0] * shape_gyr_samples[1]
        num_mag_channels = shape_mag_samples[0] * shape_mag_samples[1]

        reshaped_imu_samples = imu_samples.reshape((num_imu_channels, scan_number))
        reshaped_acc_samples = accelerometer_samples.reshape((num_acc_channels, scan_number))
        reshaped_gyr_samples = gyroscope_samples.reshape((num_gyr_channels, scan_number))
        reshaped_mag_samples = magnetometer_samples.reshape((num_mag_channels, scan_number))

        active_emg_samples = emg_samples[self.active_emg_indices]
        active_imu_samples = reshaped_imu_samples[self.active_imu_indices]
        active_acc_samples = reshaped_acc_samples[self.active_acc_indices]
        active_gyr_samples = reshaped_gyr_samples[self.active_gyr_indices]
        active_mag_samples = reshaped_mag_samples[self.active_mag_indices]
        # concatenate them all
        full_samples = np.concatenate((active_emg_samples, active_imu_samples, active_acc_samples, active_gyr_samples, active_mag_samples), axis=0)
        shape_full_samples = np.shape(full_samples)
        
        # add trigger
        if self.__trigger_active:
            trigger_signal = np.ones((1, shape_full_samples[1]))
        else:
            trigger_signal = np.zeros((1, shape_full_samples[1]))

        if obj.StartTriggerDetected and obj.StopTriggerDetected:
            if obj.StartTriggerScan > obj.StopTriggerDetected:
                trigger_signal[0, obj.StopTriggerScan:] = 0
                trigger_signal[0, obj.StartTriggerScan:] = 1
            else:
                trigger_signal[0, obj.StartTriggerScan:] = 1
                trigger_signal[0, obj.StopTriggerScan:] = 0
        elif obj.StartTriggerDetected:
            trigger_signal[0, obj.StartTriggerScan:] = 1
        elif obj.StopTriggerDetected:
            trigger_signal[0, obj.StopTriggerScan:] = 0

        full_samples = np.vstack((full_samples, trigger_signal))
        shape_full_samples = np.shape(full_samples)

        n_channels = shape_full_samples[0]
        n_samples = shape_full_samples[1]
        sd = SampleData(num_sample_sets = n_samples, 
                        num_samples_per_sample_set = n_channels, \
                        samples = full_samples.flatten(order='F').tolist())
        TMSiLoggerActivity().log("Sampling Thread->>SDS: PUT sample data")
        SampleDataServer().put_sample_data(self._dev.get_id(), sd)
        TMSiLogger().debug("Data delivered to sample data server: {} channels, {} samples".format(n_channels, n_samples))
