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
 * @file ${export_to_csv.py} 
 * @brief This example loads files and shows how to export the recorded file to
 * a .csv file.
 *
 */


'''

import sys
from os.path import join, dirname, realpath
import tkinter as tk
from tkinter import filedialog

Example_dir = dirname(realpath(__file__)) # directory of this file
modules_dir = join(Example_dir, '..') # directory with all modules
measurements_dir = join(Example_dir, '../measurements') # directory with all measurements
sys.path.append(modules_dir)

from TMSiFileFormats.file_readers import Poly5Reader, Xdf_Reader, Edf_Reader

# Open the desired file
root = tk.Tk()
filename = filedialog.askopenfilename(title = 'Select data file', filetypes = (('data-files', '*.poly5 .xdf .edf'),('All files', '*.*')))
root.withdraw()

# Load the file using the correct data format
try:
    if filename.lower().endswith('poly5'):
        reader = Poly5Reader(filename)

    elif filename.lower().endswith('xdf'):
        reader = Xdf_Reader(filename)

    elif filename.lower().endswith('edf'):
        reader = Edf_Reader(filename)

    elif not filename:
        tk.messagebox.showerror(title='No file selected', message = 'No data file selected.')

    else:
        tk.messagebox.showerror(title='Could not open file', message = 'File format not supported. Could not open file.')

except:
    tk.messagebox.showerror(title='Could not open file', message = 'Something went wrong. Could not open file.')

# Call the function export_to_csv from the file reader.
reader.export_to_csv()
