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
 * @file ${example_export_to_eeglab.py} 
 * @brief This example loads recorded files and shows how to export the recorded file to the EEGLAB 
 * .set data format.
 *
 */


'''

import sys
from os.path import join, dirname, realpath
from PySide2 import QtWidgets
import mne

Example_dir = dirname(realpath(__file__)) # directory of this file
modules_dir = join(Example_dir, '..') # directory with all modules
measurements_dir = join(Example_dir, '../measurements') # directory with all measurements
sys.path.append(modules_dir)

from TMSiFileFormats.file_readers import Poly5Reader, Xdf_Reader, Edf_Reader

app = QtWidgets.QApplication(sys.argv)
file_types = "Data Files (*.poly5 *.xdf *.edf)"
file_dialog = QtWidgets.QFileDialog()
file_dialog.setFileMode(QtWidgets.QFileDialog.ExistingFiles)
file_dialog.setNameFilters(file_types)

file_names = file_dialog.getOpenFileNames(filter = file_types)

for filename in file_names[0]:
    if filename.lower().endswith('poly5'):
        reader = Poly5Reader(filename)

        # Conversion to MNE raw array
        mne_object = reader.read_data_MNE(add_ch_locs = True) 
        file_name = filename[:-5] + 'set'

    elif filename.lower().endswith('xdf'):
        reader = Xdf_Reader(filename, add_ch_locs = True)
        
        # Get MNE raw array
        mne_object, timestamps = reader.data, reader.time_stamps
        mne_object = mne_object[0]
        file_name = filename[:-3] + 'set'

    elif filename.lower().endswith('edf'):
        reader = Edf_Reader(filename, add_ch_locs = True)
        
        # Get MNE raw array
        mne_object = reader.mne_object
        file_name = filename[:-3] + 'set'

    mne.export.export_raw(file_name, mne_object, fmt = 'eeglab')
