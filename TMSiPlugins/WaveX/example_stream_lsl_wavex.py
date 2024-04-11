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
 * @file example_stream_lsl_wavex.py
 * @brief This example shows the functionality to stream to LSL.
 *
 */


'''

import sys
from os.path import join, dirname, realpath
Plugin_dir = dirname(realpath(__file__)) # directory of this file
modules_dir = join(Plugin_dir, '..', '..') # directory with all modules
measurements_dir = join(Plugin_dir, '../../measurements') # directory with all measurements
configs_dir = join(Plugin_dir, '../../TMSiSDK\\tmsi_resources') # directory with configurations
sys.path.append(modules_dir)
repo_dir = join(Plugin_dir, '..', '..', '..') # directory with repo
sys.path.append(repo_dir)
sys.path.append(Plugin_dir)

from PySide2.QtWidgets import *
from wavex.wavex_device import WaveXDevice
from wavex.wavex_structures import wavex_API_enums

from TMSiSDK.tmsi_sdk import TMSiSDK, DeviceType, DeviceInterfaceType, DeviceState
from TMSiSDK.tmsi_errors.error import TMSiError
from TMSiFileFormats.file_writer import FileWriter, FileFormat
from TMSiGui.gui import Gui
from TMSiPlotterHelpers.filtered_signal_plotter_helper import FilteredSignalPlotterHelper
from TMSiPlugins.WaveX.signal_plotter_helper_wave_x import SignalPlotterHelperWaveX 
from TMSiSDK.device import ChannelType
from TMSiSDK.device.devices.saga.saga_API_enums import SagaBaseSampleRate

import logging
logging.basicConfig(level=logging.WARNING, handlers=[])

grid_type = '4-8-L'

try:
    # Execute a device discovery. This returns a list of device-objects for every discovered device.
    TMSiSDK().discover(dev_type = DeviceType.saga, dr_interface = DeviceInterfaceType.docked, ds_interface = DeviceInterfaceType.usb)
    discoveryList = TMSiSDK().get_device_list(DeviceType.saga)

    if (len(discoveryList) > 0):
        # Get the handle to the first discovered device and open the connection.
        for i,_ in enumerate(discoveryList):
            SAGA = discoveryList[i]
            if SAGA.get_dr_interface() == DeviceInterfaceType.docked:
                # Open the connection to SAGA
                SAGA.open()
                break

    # Configure the SAGA sampling configuration
    SAGA.import_configuration(join(configs_dir, "saga32_config_textile_grid_" + grid_type + ".xml"))
    SAGA.set_device_sampling_config(base_sample_rate = SagaBaseSampleRate.Decimal, 
                                    channel_type = ChannelType.all_types, 
                                    channel_divider = 2)

    # Get the handle to the first discovered device.
    WaveX = WaveXDevice()    
    # Open a connection to the device
    WaveX.open()

    # Configure the WaveX sensors
    WaveX.set_device_sensor_configuration(
        sensor_number = 3, 
        enable = True,
        mode = wavex_API_enums.SensorMode.EMG,
        model = wavex_API_enums.SensorModel.Mini_EmgImu,
        acc_full_scale = wavex_API_enums.AccelerometerFullScale.g_8,
        gyr_full_scale = wavex_API_enums.GyroscopeFullScale.dps_1000)
    WaveX.set_device_sensor_configuration(
        sensor_number = 4, 
        enable = True,
        mode = wavex_API_enums.SensorMode.EMG_INERTIAL,
        model = wavex_API_enums.SensorModel.Mini_EmgImu,
        acc_full_scale = wavex_API_enums.AccelerometerFullScale.g_8,
        gyr_full_scale = wavex_API_enums.GyroscopeFullScale.dps_1000)
    WaveX.set_device_sampling_config(
        EMG_acq_type=wavex_API_enums.EmgAcqXType.Emg_2kHz,
        EMG_IMU_acq_type=wavex_API_enums.EmgImuAcqXType.Emg_2kHz_RawAccGyroMagData_100Hz,
        IMU_acq_type=wavex_API_enums.ImuAcqXType.Mixed6xData_200Hz,
        )
    
    # Initialise and open the SAGA LSL stream
    stream_SAGA = FileWriter(FileFormat.lsl, "SAGA")
    stream_SAGA.open(SAGA)

    # Initialise and open the WaveX lsl-stream
    stream_WaveX = FileWriter(FileFormat.lsl, "WAVEX", lsl_offset = 0.040)
    stream_WaveX.open(WaveX)

    # Initialise the plotter application
    app = QApplication(sys.argv)
    plotter_helper_WaveX = SignalPlotterHelperWaveX(device=WaveX)
    plotter_helper_SAGA = FilteredSignalPlotterHelper(device = SAGA, hpf = 10, grid_type = grid_type)

    # Define the GUI object and show it 
    gui_WaveX = Gui(plotter_helper = plotter_helper_WaveX)
    gui_SAGA = Gui(plotter_helper = plotter_helper_SAGA)
    
    # Enter the event loop
    app.exec_()
    
    # Close the LSL stream after GUI termination
    stream_WaveX.close()
    stream_SAGA.close()

    # Close the connection to the devices
    WaveX.close()
    SAGA.close()
    
except TMSiError as e:
    print(e)
        
finally:
    # Close the connection to the device when the device is opened
    if SAGA.get_device_state() == DeviceState.connected:
        SAGA.close()