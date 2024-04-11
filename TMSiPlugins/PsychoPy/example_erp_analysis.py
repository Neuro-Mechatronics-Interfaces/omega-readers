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
 * @file ${example_erp_analysis.py} 
 * @brief Example how to post process Poly5 data with MNE for evoked potentials. 
     Example is designed for an oddball experiment, but can be configured by user. 
 *
 */


'''

# Load packages
import sys
from os.path import join, dirname, realpath
Plugin_dir = dirname(realpath(__file__)) # directory of this file
modules_dir = join(Plugin_dir, '..', '..') # directory with all modules
measurements_dir = join(Plugin_dir, '../../measurements') # directory with all measurements
sys.path.append(modules_dir)
import mne
from IPython import get_ipython
import matplotlib.pyplot as plt
import numpy as np
from TMSiFileFormats.file_readers import Poly5Reader
import tkinter as tk
from tkinter import filedialog
from mne.preprocessing import ICA
import easygui
from mne.preprocessing import peak_finder
import pandas as pd

ipython = get_ipython()
ipython.magic("matplotlib qt")

#%% Set variables by user
device_type = 'APEX'

# Event values
target_value = 16       # Stored value in STATUS channel for target stimulus
nontarget_value = 2   # Stored value in STATUS channel for nontarget stimulus

full_version = easygui.buttonbox("Would you like to run the full version?", choices=["Yes","No"])
if full_version == "Yes":
    a_flag=True
elif full_version == "No":
    a_flag=False
else:
    a_flag=False


root = tk.Tk()
filename = filedialog.askopenfilename(title = 'Select data file', filetypes = (('data-files', '*.poly5'),('All files', '*.*')))
root.withdraw()

try:
    if filename.lower().endswith('poly5'):
        data = Poly5Reader(filename)

        # Conversion to MNE raw array
        mne_object = data.read_data_MNE() 

    elif not filename:
        tk.messagebox.showerror(title='No file selected', message = 'No data file selected.')
    else:
        tk.messagebox.showerror(title='Could not open file', message = 'File format not supported. Could not open file.')

    if mne_object:
        if filename[-32:] == "sample_data_erp_experiment.poly5":
            # Channels CP6 and POz were not connected in this file. 
            mne_object.info['bads'].extend(['CP6', 'POz'])
        
        # Retrieve the MNE RawArray info, channel names, sample data, and sampling frequency [Hz]
        info_mne = mne_object.info
        ch_names = mne_object.info['ch_names']
        samples_mne = mne_object._data
        fs = data.sample_rate

        # Do not show disconnected channels
        show_chs = []
        for idx, ch in enumerate(mne_object._data):
            if ch.any():
                show_chs = np.hstack((show_chs,mne_object.info['ch_names'][idx]))
        data_object = mne_object.copy().pick(show_chs)
        if a_flag: # To display raw EEG time series and PSD plot of raw EEG signals.
            fig_psd, ax_psd = plt.subplots()
            raw_data_psd = data_object.compute_psd(method='welch', fmin=0.1, fmax=50)
            raw_data_psd.plot(average=True, picks="eeg", exclude="bads", show=False, axes=ax_psd)
            ax_psd.set_title("Average PSD plot of raw EEG data of all non-zero channels.")
            data_object.plot(scalings=dict(eeg = 250e-6), start= 0, duration = 5, n_channels = 5, title = filename, block = True)
except:
    tk.messagebox.showerror(title='Could not open file', message = 'Something went wrong. Could not view file.')

# Poly5 dataformat cannot store the channeltypes. Therefore, the researcher should manually
# enter the types of data each channel holds. Channels are always ordered in the same way:
    # First channel is common reference, if enabled ('misc' channel)
    # all UNI channels that are enabled ('eeg' channels by default)
    # BIP channels (channel type depends on research)
    # TRIGGER channel ('misc' channel)
    # Status & counter channel ('misc' channels)

# Define channels in use (1 = enabled, 0 = disabled)
CREF_used = 0       # If measured with a common reference, set to 1,  otherwise 0
BIP1_used = 0       # If BIP channel 1 is used, set to 1, otherwise 0
BIP2_used = 0       # If BIP channel 2 is used, set to 1, otherwise 0
BIP3_used = 0       # If BIP channel 3 is used, set to 1, otherwise 0
BIP4_used = 0       # If BIP channel 4 is used, set to 1, otherwise 0
TRIGGER_used = 1    # If TRIGGER channel was enabled, set to 1, otherwise 0

# Fill out the number of EEG channels
number_eeg = 32

# Channel type for undefined channels
# Possible channel options include 'eog', 'eeg', 'ecg', 'emg', 'misc'
BIP1_type = 'eog'     # Signal type for BIP channel 1
BIP2_type = 'eog'     # Signal type for BIP channel 2
BIP3_type = 'ecg'     # Signal type for BIP channel 3
BIP4_type = 'emg'     # Signal type for BIP channel 4


# Define a variable for MNE that includes all channel types and all channels that are used in the correct order
if device_type == 'SAGA':
    channel_types = CREF_used * ['misc'] + number_eeg * ['eeg'] + BIP1_used * [BIP1_type] + BIP2_used * [BIP2_type] + BIP3_used * [BIP3_type] + BIP4_used * [BIP4_type] + TRIGGER_used * ['misc'] + 2 * ['misc']
elif device_type == 'APEX':
    channel_types = number_eeg * ['eeg'] + TRIGGER_used * ['misc'] + 4 * ['misc']

# Add montage & electrode location information to the MNE object
info_mne.set_montage('standard_1020')
# Create the new object
mne_object = mne.io.RawArray(mne_object._data, info_mne)

# Create a mask to identify EEG channels
eeg_mask = [ch_type == 'eeg' for ch_type in channel_types]

# Re-referencing to the mastoids
EEGraw_reref = mne_object.set_eeg_reference(ref_channels=['M1', 'M2'])

#%% Preprocessing
selected_channels = ['Fz','F3','F4','Pz', 'P3', 'P4','Cz','C3','C4']
reref_psd = EEGraw_reref.compute_psd(method='welch', fmin=0.1, fmax=50)
# Show unfiltered data
if a_flag:
    EEGraw_reref.plot(scalings=dict(eeg = 100e-6),title="Re-refrenced, unfiltered EEG")
    #PSD plot of re-referenced unflitered EEG. Only for selected channels.
    fig_psd2, ax_psd2 = plt.subplots()
    reref_psd.plot(average=False, picks=selected_channels, exclude="bads", show=False, axes=ax_psd2)
    ax_psd2.set_title("PSD plot of re-referenced unfiltered EEG for selected channels.")
    plt.show()

# Filter variables
f_l = 0.5;           # Lower frequency of band-pass (thus, high-pass filter)
f_h = 35             # Higher frequency of band-pass (thus, low-pass filter)

# Filter the data (high pass + lowpass)
preprocessed_data= EEGraw_reref.copy().filter(l_freq=f_l, h_freq=f_h,method='iir',phase = 'zero-double')

#%% Applying ICA to remove ocular artefacts
ICAapplied_data = preprocessed_data.copy()
number_components = 20
ica = ICA(n_components=number_components, max_iter='auto', random_state=97)
ica.fit(ICAapplied_data)

# Plot ICA sources and components to analyse them by hand
ica.plot_sources(ICAapplied_data)
ica.plot_components()

# Based on visual inspection, manually exclude components to remove EOG artefacts
# Display a dialog for component exclusion
msg = "Select ICA components to exclude"
choices = [f"ICA component {i}" for i in range(number_components)]
selected_choices = easygui.multchoicebox(msg, "ICA Component Exclusion", choices)

if selected_choices is None:
    excluded_components = []  # No components selected
else:
    excluded_components = [int(choice.split(" ")[-1]) for choice in selected_choices if choice.startswith("ICA component")]

if excluded_components:
    print(f"Excluded ICA components: {excluded_components}")
    ica.exclude = excluded_components
else:
    print("No ICA components selected for exclusion.")
    
# Reconstruct original signals with artefacts removed
ica.apply(ICAapplied_data)

#%% Retrieving epoched data

# Find the index of the TRIGGER channel (for APEX, change to STATUS to find stored triggers)
for i in range(len(mne_object.ch_names)):    
     if mne_object.ch_names[i] == 'STATUS':
         trigger_chan_num = i

# Find the samples of the TRIGGER channel
trigger_chan_data = samples_mne[trigger_chan_num] -32 # removing baseline
trigger_chan_data = [0 if value == 30 else value for value in trigger_chan_data] # remove synchronisation issue

# Find events in the data
ICAapplied_data._data[trigger_chan_num] = trigger_chan_data
events = mne.find_events(ICAapplied_data, stim_channel = 'STATUS', output = 'onset')

# Assign target and non-target value
event_dict = {'target stimulus': target_value, 'non-target stimulus': nontarget_value}

# Epoch data based on events found (-200 ms to +800 ms)
epochs_nobaseline_noICA = mne.Epochs(preprocessed_data, events, event_id=event_dict, tmin=-0.2, tmax=0.8,baseline=None,
                    preload=True) # only needed for counting ocular artefacts per epoch
epochs = mne.Epochs(ICAapplied_data, events, event_id=event_dict, tmin=-0.2, tmax=0.8,baseline=(-0.2, 0),
                    preload=True)

if a_flag:
    mne.viz.plot_epochs(epochs, title='Individual Epochs', scalings=dict(eeg = 30e-6))  
         
#%% Plot ERPs

# Average epochs per channel
erp_target =  epochs['target stimulus'].average()
erp_nontarget =  epochs['non-target stimulus'].average() 

# Plot the results for both events per location of electrode
mne.viz.plot_evoked_topo([erp_target, erp_nontarget],scalings = None, title = "Topological overview target and nontarget")


# Get the channel indices corresponding to the selected channel names
channel_indices = [epochs.info['ch_names'].index(ch) for ch in selected_channels]

# Plot the average ERPS for the selected channels of interest
fig, axs = plt.subplots(2, 1) # figure with two subplots
fig.suptitle('Average over trials for selected channels', fontsize=16)

# Target stimulus in the first subplot average of trials
axs[0].grid(True)
erp_target.plot(spatial_colors=True,scalings = None, picks=channel_indices, axes=axs[0],show=False)
axs[0].set_title('Average ERP - Target Stimulus')
axs[0].set_ylabel('Amplitude (μV)')
axs[0].set_ylim(-15,30)
# Non-target stimulus in the second subplot average of trials
axs[1].grid(True)
erp_nontarget.plot(spatial_colors=True,scalings = None, picks=channel_indices, axes=axs[1],show=False)
axs[1].set_title('Average ERP - Non-Target Stimulus')
axs[1].set_ylabel('Amplitude (μV)')  
axs[1].set_ylim(-15,30)
fig.set_tight_layout(True)
plt.show()

#%% Plot ERPs per trial

# Get the individual trials for both conditions
trials_target = epochs['target stimulus'].get_data()[:, channel_indices, :]
trials_nontarget = epochs['non-target stimulus'].get_data()[:, channel_indices, :]

# #%% Subtracting nontarget ERP from target ERP
erp_diff  = mne.combine_evoked([erp_target, erp_nontarget], weights=[1,-1])
if a_flag: # plots the difference between target and non-target values
    fig_diff, ax_diff = plt.subplots()
    erp_diff.plot(spatial_colors=True,scalings = None, picks=channel_indices,show=False, axes=ax_diff)
    ax_diff.set_title("Non-target values are subtracted from target values.")
    ax_diff.grid()
    fig_diff.set_tight_layout(True)
    
#%% Finding P300 peak

# Define the time range of interest in seconds
start_time = 0.25  
end_time = 0.5    
start_baseline = -0.2
stop_baseline = 0

# Initialize lists to store peak information for each channel and epoch
P300_indx = [[] for _ in selected_channels]         # P300 index
P300_mags = [[] for _ in selected_channels]         # P300 magnitude
P300_latency = [[] for _ in selected_channels]      # P300 latency
P300_amplitude = [[] for _ in selected_channels]    # P300 amplitude
P300_meanvoltage = [[] for _ in selected_channels]  # P300 mean voltage

# Loop over all channels
for channel_idx,channel_name in enumerate(selected_channels):
    # Loop over all epochs    
    for epoch_idx in range(len(erp_diff.data)):
        epoch_peak_amplitudes = []  # Initialize a list for this epoch's peak amplitudes
    
        # Select epoch data for the channel
        data = epochs[epoch_idx].pick([channel_name])
        data = data.get_data(units = 'uV')[0,0]

        # Select the time range of interest
        time_indices = np.where((epochs.times >= start_time) & (epochs.times <= end_time))  # selecting time indices of time range
        channel_data = data[time_indices] # selecting data points in time range
        time_data = epochs.times[time_indices]  # selecting time data points in time range
        
        # Select time range of pre-stimulus baseline 
        time_idx_base = np.where((epochs.times >= start_baseline) & (epochs.times <= stop_baseline))
        baseline_data = data[time_idx_base]
        
        # Compute the mean voltage
        mean_voltage_baseline = np.mean(baseline_data)  # mean voltage pre-stimulus baseline
        mean_voltage_timerange = np.mean(channel_data)  # mean voltage P300 time range
        
        # Find peaks
        locs, mags = peak_finder(channel_data, extrema=1)
        
        # Determine the highest peak
        highest_peak_mags = max(mags)  # magnitude
        highest_peak_loc = locs[np.argmax(mags)] # index
        highest_peak_lat = time_data[highest_peak_loc]*1000 # latency in ms
        highest_peak_amp = highest_peak_mags - mean_voltage_baseline 
        
        # Removing end-point detected "peaks"
        if highest_peak_lat == 500:
            highest_peak_lat = 0
            highest_peak_amp = 0 
        if highest_peak_lat == 250:
            highest_peak_lat = 0
            highest_peak_amp = 0

        # Append the locations and magnitudes for this epoch to the respective lists
        P300_indx[channel_idx].append(highest_peak_loc)
        P300_mags[channel_idx].append(highest_peak_mags)
        
        P300_latency[channel_idx].append(highest_peak_lat)
        P300_amplitude[channel_idx].append(highest_peak_amp)
        P300_meanvoltage[channel_idx].append(mean_voltage_timerange)
        
        # Save all peak data
        epoch_peak_amplitudes.append(locs)  # Store the peak amplitude and time for this channel

#%% Quality measures - mean + std P300 latency, amplitude, mean voltage
# Initialize lists for mean and standard deviation
mean_P300_latency = []
std_P300_latency = []
mean_P300_amplitude = []
std_P300_amplitude = []
mean_P300_meanvoltage = []
std_P300_meanvoltage = []

for latency_list, amplitude_list, meanvoltage_list in zip(P300_latency, P300_amplitude, P300_meanvoltage):
    # Convert the lists to NumPy arrays for calculations
    latency_array = np.array(latency_list)
    amplitude_array = np.array(amplitude_list)
    meanvoltage_array = np.array(meanvoltage_list)
    
    # Calculate mean and standard deviation for latency
    mean_latency = np.mean(latency_array)
    std_latency = np.std(latency_array)
    
    # Calculate mean and standard deviation for amplitude
    mean_amplitude = np.mean(amplitude_array)
    std_amplitude = np.std(amplitude_array)
    
    # Calculate mean and standard deviation for mean voltage
    mean_meanvoltage = np.mean(meanvoltage_array)
    std_meanvoltage = np.std(meanvoltage_array)
    
    # Append the results to the respective lists
    mean_P300_latency.append(mean_latency)
    std_P300_latency.append(std_latency)
    mean_P300_amplitude.append(mean_amplitude)
    std_P300_amplitude.append(std_amplitude)
    mean_P300_meanvoltage.append(mean_meanvoltage)
    std_P300_meanvoltage.append(std_meanvoltage)


# Plotting mean, std for P300 latency, amplitude, and mean voltage
num_channels = len(selected_channels)
categories = ['Latency', 'Amplitude', 'Mean Voltage']
channel_labels = selected_channels
fig2, axs2 = plt.subplots(nrows=len(categories), ncols=1, figsize=(10, 6))

for i, category in enumerate(categories):
    ax = axs2[i]
    mean_values = [mean_P300_latency, mean_P300_amplitude, mean_P300_meanvoltage][i]
    std_values = [std_P300_latency, std_P300_amplitude, std_P300_meanvoltage][i]
    x = np.arange(num_channels)

    ax.errorbar(x, mean_values, yerr=std_values, fmt='o', markersize=6, alpha=0.7) 
    ax.set_title(f'{category} by Channel')
    ax.set_xticks(x)
    ax.set_xticklabels(channel_labels)
    ax.grid(axis='y', linestyle='--', alpha=0.6)

axs2[0].set_ylabel('Latency (ms)')
axs2[1].set_ylabel('Amplitude (μV)')
axs2[2].set_ylabel('Mean Voltage (μV)')

fig2.set_tight_layout(True)
plt.show()

# Create empty DataFrame
data = {'Category': [], 'Channel': [], 'Mean': [], 'Std': []}
df = pd.DataFrame(data)

# Populate the DataFrame with mean and std values
for i, category in enumerate(categories):
    for j, channel_name in enumerate(channel_labels):
        mean = [mean_P300_latency, mean_P300_amplitude, mean_P300_meanvoltage][i][j]
        std = [std_P300_latency, std_P300_amplitude, std_P300_meanvoltage][i][j]
        df = df.append({'Category': category, 'Channel': channel_name, 'Mean': mean, 'Std': std}, ignore_index=True)

# Display the DataFrame
print(df)