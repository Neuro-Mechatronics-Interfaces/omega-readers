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
 * @file consumer_thread_apex.py
 * @brief 
 * Consumer thread optimized for Apex
 */


'''
import numpy as np

from TMSiSDK.tmsi_utilities.support_functions import array_to_matrix as Reshape

from .consumer_thread import ConsumerThread

class ConsumerThreadApex(ConsumerThread):
    def __init__(self, consumer_reading_queue, sample_rate):
        super().__init__(consumer_reading_queue, sample_rate)
        self.cycling_impedance = dict()

    def process(self, sample_data):
        reshaped = np.array(Reshape(sample_data.samples, sample_data.num_samples_per_sample_set))
        self.original_buffer.append(reshaped)
        for idx in range(len(reshaped[-5,:])):
                index = int(reshaped[-5,idx])+1
                if index in self.cycling_impedance:
                    self.cycling_impedance[index]["Re"] = reshaped[-4,idx]
                    self.cycling_impedance[index]["Im"] = reshaped[-3,idx]
                else:
                    self.cycling_impedance[index] = dict()
                    self.cycling_impedance[index]["Re"] = reshaped[-4,idx]
                    self.cycling_impedance[index]["Im"] = reshaped[-3,idx]
        