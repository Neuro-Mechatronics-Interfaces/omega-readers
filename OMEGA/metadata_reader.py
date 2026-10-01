
import json
import sys
from pathlib import Path
from os.path import join, dirname, realpath
import tkinter as tk
from tkinter import filedialog

Example_dir = dirname(realpath(__file__)) # directory of this file
modules_dir = join(Example_dir, '..') # directory with all modules
measurements_dir = join(Example_dir, '../measurements') # directory with all measurements
sys.path.append(modules_dir)

from TMSiFileFormats.file_readers import Poly5Reader, Poly6Reader, Xdf_Reader, Edf_Reader

# Open the desired file
root = tk.Tk()
root.withdraw()
filename = filedialog.askopenfilename(title = 'Select data file', filetypes = (('data-files', '*.poly5 *.poly6 *.xdf *.edf'),('All files', '*.*')))
root.destroy()

if not filename:
    raise SystemExit("No data file selected.")

try:
    if filename.lower().endswith('poly5'):
        reader = Poly5Reader(filename)

        ch_names = reader.ch_names
        sample_rate = reader.sample_rate
        num_channels = reader.num_channels

    elif filename.lower().endswith('poly6'):
        reader = Poly6Reader(filename)

        ch_names = reader.ch_names
        sample_rate = reader.sample_rate
        num_channels = reader.num_channels

    elif filename.lower().endswith('xdf'):
        reader = Xdf_Reader(filename)
        data = reader.data[0]

        ch_names = data.ch_names
        sample_rate = data.info['sfreq']
        num_channels = len(ch_names)

    elif filename.lower().endswith('edf'):
        reader = Edf_Reader(filename)
        data = reader.mne_object

        ch_names = data.ch_names
        sample_rate = data.info['sfreq']
        num_channels = len(ch_names)

    else:
        raise ValueError("File format not supported. Select a Poly5, Poly6, XDF, or EDF file.")

except Exception as error:
    raise SystemExit(f"Could not read file: {error}") from error

x_coordinate = input("Enter X coordinate: ").strip()
y_coordinate = input("Enter Y coordinate: ").strip()
orientation = input("Enter orientation: ").strip()

metadata = {
    "File": filename,
    "Sample rate (Hz)": sample_rate,
    "Number of channels": num_channels,
    "X coordinate": x_coordinate,#mm from navel, positive = up, negative = down
    "Y coordinate": y_coordinate, #mm from navel, positive = right, negative = left
    "Orientation": orientation, #degrees from left orientation, clockwise.
}

print("\nMetadata")
for field, value in metadata.items():
    print(f"{field}: {value}")

metadata_path = Path(filename).with_suffix(".json")
if metadata_path.exists():
    overwrite = input(f"{metadata_path.name} already exists. Replace it? [y/N]: ").strip().lower()
    if overwrite not in {"y", "yes"}:
        raise SystemExit("Metadata JSON was not saved.")

try:
    metadata_path.write_text(json.dumps(metadata, indent=2), encoding="utf-8")
except OSError as error:
    raise SystemExit(f"Could not save metadata to {metadata_path}: {error}") from error

print(f"Metadata saved to: {metadata_path}")
