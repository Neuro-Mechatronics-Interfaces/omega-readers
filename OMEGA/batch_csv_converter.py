import sys
from pathlib import Path
from os.path import dirname, realpath
import csv
import tkinter as tk
from tkinter import filedialog

import numpy as np

Example_dir = dirname(realpath(__file__))
modules_dir = Path(Example_dir, "..").resolve()
sys.path.append(str(modules_dir))

from TMSiFileFormats.file_readers import Poly5Reader, Poly6Reader


def _choose_output_folder(source_folder):
	base = source_folder.parent / f"{source_folder.name}_csv"
	output_folder = base
	suffix = 2
	while output_folder.exists():
		output_folder = base.with_name(f"{base.name}_{suffix}")
		suffix += 1
	output_folder.mkdir()
	return output_folder


def _poly5_blocks(reader, block_samples=8192):
	for start in range(0, reader.samples.shape[1], block_samples):
		yield reader.samples[:, start:start + block_samples].T


def _write_csv(reader, sample_blocks, output_path):
	headers = [
		f"{name} ({unit})"
		for name, unit in zip(reader.ch_names, reader.ch_unit_names)
	]
	headers.append("Fs (Hz)")

	with output_path.open("w", newline="", encoding="utf-8-sig") as csv_file:
		csv.writer(csv_file).writerow(headers)
		for samples in sample_blocks:
			rows = np.empty((samples.shape[0], len(headers)), dtype=np.float64)
			with np.errstate(invalid="ignore"):
				rows[:, :-1] = samples
			rows[:, -1] = reader.sample_rate
			np.savetxt(csv_file, rows, delimiter=",", fmt="%.9g")


def _convert_file(source_path, output_path):
	if source_path.suffix.lower() == ".poly5":
		reader = Poly5Reader(str(source_path))
		sample_blocks = _poly5_blocks(reader)
	else:
		reader = Poly6Reader(str(source_path))
		sample_blocks = reader.iter_sample_blocks()

	_write_csv(reader, sample_blocks, output_path)


def main():
	root = tk.Tk()
	root.withdraw()
	selected_folder = filedialog.askdirectory(title="Select folder containing Poly5/Poly6 files")
	root.destroy()

	if not selected_folder:
		raise SystemExit("No folder selected.")

	source_folder = Path(selected_folder)
	source_files = sorted(
		path for path in source_folder.iterdir()
		if path.is_file() and path.suffix.lower() in {".poly5", ".poly6"}
	)
	if not source_files:
		raise SystemExit("The selected folder contains no Poly5 or Poly6 files.")

	output_folder = _choose_output_folder(source_folder)
	print(f"Converting {len(source_files)} file(s) to: {output_folder}")

	stem_counts = {}
	for path in source_files:
		stem_counts[path.stem.lower()] = stem_counts.get(path.stem.lower(), 0) + 1

	failures = []
	for source_path in source_files:
		output_name = f"{source_path.stem}.csv"
		if stem_counts[source_path.stem.lower()] > 1:
			output_name = f"{source_path.stem}_{source_path.suffix[1:].lower()}.csv"
		output_path = output_folder / output_name
		try:
			_convert_file(source_path, output_path)
			print(f"Converted: {source_path.name} -> {output_path.name}")
		except Exception as error:
			output_path.unlink(missing_ok=True)
			failures.append((source_path.name, str(error)))
			print(f"Failed: {source_path.name}: {error}")

	print(f"\nFinished. CSV files are in: {output_folder}")
	if failures:
		print(f"{len(failures)} file(s) could not be converted.")


if __name__ == "__main__":
	main()
