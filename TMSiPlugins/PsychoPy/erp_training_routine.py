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
 * @file erp_training_routine.py
 * @brief This file provides an implementation to show the experimental 
 * paradigm without needing to interface with a device. This can be used to
 * familiarise a subject with the experimental protocol. 
 *
 */


'''

from psychopy import sound
import random
import time

class PsychopyTrainingSetup():
    """ A class that sets up a training for an auditory oddball experiment 
        based on the PsychoPy library 
    """
    
    def __init__(self, background_image_path):
        """ Initialize the training setup
        
        Args:
            background_image_path (str): Path to the background image file.
        """
        self.background_image_path = background_image_path
        self.interval = 1.5  # Interstimulus interval in seconds
        self.n_stimuli = 10

    def runTraining(self):
        """ Run the training with stimuli
        """        
        # Create the auditory stimuli
        # Initialize lists for target and non-target stimuli
        target_stimuli = [sound.Sound(value=1000, secs=0.05, hamming=True) for _ in range(5)]
        non_target_stimuli = [sound.Sound(value=2000, secs=0.05, hamming=True) for _ in range(5)]
        
        # Shuffle the order of the stimuli
        all_stimuli = target_stimuli + non_target_stimuli
        random.shuffle(all_stimuli)
        
        for stim in all_stimuli:
            stim.play()
            time.sleep(self.interval)
