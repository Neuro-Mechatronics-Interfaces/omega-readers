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
 * @file ${example_psychopy_erp_experiment_saga.py} 
 * @brief This example shows how to combine sending triggers to SAGA with running a 
 * pre-coded experiment with PsychoPy with the TTL trigger module
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

import os
os.environ["PYQTGRAPH_QT_LIB"] = 'PySide2'

from TMSiSDK.tmsi_sdk import TMSiSDK, DeviceType, DeviceInterfaceType, DeviceState
from TMSiSDK.tmsi_errors.error import TMSiError
from TMSiSDK.device.devices.saga.saga_API_enums import SagaBaseSampleRate
from TMSiSDK.device import ChannelType
from TMSiSDK.device.tmsi_device_enums import MeasurementType
from TMSiSDK.tmsi_utilities.mask_type import MaskType

from PySide2.QtWidgets import *
from TMSiGui.gui import Gui
from TMSiPlotterHelpers.impedance_plotter_helper import ImpedancePlotterHelper
from TMSiPlotterHelpers.signal_plotter_helper import SignalPlotterHelper
from TMSiFileFormats.file_writer import FileWriter, FileFormat
from TMSiPlugins.PsychoPy.experiment_psychopy import PsychopyExperimentSetup
from TMSiPlugins.PsychoPy.erp_training_routine import PsychopyTrainingSetup
from TMSiPlugins.external_devices.usb_ttl_device import TTLError

import time
from threading import Thread
import easygui 
from PIL import Image

def display_background_image(image_path):
    # Open and display the image using PIL
    image = Image.open(image_path)
    image.show()
    easygui.msgbox("Click 'OK' to continue once you see the image.")
    

# Check whether the sound level on laptop is set to 40 ~ corresponding to 60 dB
while True:
    sound_choice = easygui.buttonbox("Is the laptop sound turned on at volume 40?", choices=["Yes","No"])
    
    if sound_choice == "Yes":
        easygui.msgbox("Well done, you can continue")
        break
    elif sound_choice == "No":
        easygui.msgbox("Adjust the volume please")
        continue
    else:
        break        

try:
    # Execute a device discovery. This returns a list of device-objects for every discovered device.
    TMSiSDK().discover(dev_type = DeviceType.saga, dr_interface = DeviceInterfaceType.docked, ds_interface = DeviceInterfaceType.usb)
    discoveryList = TMSiSDK().get_device_list(DeviceType.saga)

    # Set up device
    if (len(discoveryList) > 0):
        # Get the handle to the first discovered device.
        dev = discoveryList[0]
        
        # Open a connection to the SAGA-system
        dev.open()
        
        # Load the EEG channel set and configuration
        print("load EEG config")
        if dev.get_num_channels()<64:
            dev.import_configuration(join(configs_dir, "saga_config_EEG32.xml"))
        else:
            dev.import_configuration(join(configs_dir, "saga_config_EEG64.xml")) 
            
        # Set the sample rate of the AUX channels to 4000 Hz
        dev.set_device_sampling_config(base_sample_rate = SagaBaseSampleRate.Decimal)
        dev.set_device_triggers(True)
               
        # Downsample
        dev.set_device_sampling_config(channel_type = ChannelType.UNI, channel_divider = 4)
        dev.set_device_sampling_config(channel_type = ChannelType.BIP, channel_divider = 4)
        dev.set_device_sampling_config(channel_type = ChannelType.AUX, channel_divider = 4)
    
        # Initialize PsychoPy Experiment, for arguments description see class
        print('\n Initializing PsychoPy experiment and TTL module \n')
        print('\n  Please check if red and green LEDs are turned on ... \n')

        # Experiment settings
        n_trials = 60
        interval = 1.5 
        duration = 0.05
        probability = 0.2

        # !! NOTE: Available options for the (non)target_value inputs are all numbers between 0 and 255 for SAGA
        # Check COM_port on which the USB-TTL module can be found and change accordingly. 
        experiment = PsychopyExperimentSetup(TMSiDevice="SAGA", COM_port = 'COM5', n_trials = n_trials, target_value = 17, nontarget_value= 1,
                                             interval = interval, probability = probability, duration = duration)
        
        # Check if there is already a plotter application in existence
        app = QApplication.instance()
        
        # Initialise the plotter application if there is no other plotter application
        if not app:
            app = QApplication(sys.argv)
        
        # Initialise the helper
        plotter_helper = ImpedancePlotterHelper(device=dev,
                                                is_head_layout=True, 
                                                file_storage = join(measurements_dir,"Example_PsychoPy_ERP_experiment"))
        # Define the GUI object and show it 
        gui = Gui(plotter_helper = plotter_helper)
        # Enter the event loop
        app.exec_()
        
        # Pause for a while to properly close the GUI after completion
        time.sleep(1)
        
        # Find the trigger channel index number
        channels = dev.get_device_active_channels()
        for i in range(len(channels)):   
            if channels[i].get_channel_name() == 'TRIGGERS':
                trigger_channel = i    

        # Apply mask on trigger channel. This mask is applied because SAGA TRIGGER input has inverse logic. 
        # By applying the mask, the baseline of the triggers is low again
        dev.apply_mask([trigger_channel],[MaskType.REVERSE])

        # Set up background image 
        background_image_path = join(Plugin_dir, 'psychopy_resources', 'cross.png')

        while True:
            # are you ready for the training?
            ready_choice = easygui.buttonbox("Are you ready for the training?", choices=["Yes", "No"])
            
            if ready_choice == "Yes":
                
                # Display the background image
                display_background_image(background_image_path)
        
                # Create an instance of the PsychopyTrainingSetup class with the background image
                training_setup = PsychopyTrainingSetup(background_image_path)
                
                # Run the training
                training_setup.runTraining()
            
                # Ask the participant if they want to do it again or continue
                choice = easygui.buttonbox("Do you want to do the training again?", choices=["Yes", "No"])

                if choice == "No":
                    break  # Exit the loop if the participant chooses "No"
            elif ready_choice == "No":
                continue
            else:
                break
        
        # Initialise a file-writer class (XDF-format) and state its file path
        file_writer = FileWriter(FileFormat.xdf, join(measurements_dir,"Example_PsychoPy_ERP_experiment.xdf"))
        
        # Check to see if the participant is ready for the experiment
        while True:
            exp_choice = easygui.buttonbox("Are you ready for the experiment?", choices=["Yes","No"])
            
            if exp_choice == "Yes":
                easygui.msgbox("Alright, the experiment will start in a bit. \n\nPlease make the image fullscreen after clicking 'OK' ")
                break
            elif exp_choice == "No":
                easygui.msgbox("Alright take your time")
                continue
            else:
                break   
            
        # Define the handle to the device
        file_writer.open(dev)
        
        # Define thread to run the experiment
        thread = Thread(target=experiment.runExperiment)
        
        # Start a measurement on SAGA
        dev.start_measurement(MeasurementType.SAGA_SIGNAL)
        
        # Start the PsychoPy thread
        thread.start()
        
        # Acquisition time, based on experiment timing (with some additional time at the end)
        time.sleep(n_trials * (interval + duration) + 10)
        
        # Stop the measurement on SAGA
        dev.stop_measurement()

        # Close the file writer after GUI termination
        file_writer.close()
        
        # Close the connection to SAGA
        dev.close()
        

except TMSiError as e:
    print(e)

except TTLError as e:
   raise TTLError("Is the TTL module connected? Please try again")
        
finally:
    if 'dev' in locals():
        # Close the connection to the device when the device is opened
        if dev.get_device_state() == DeviceState.connected:
            dev.close()