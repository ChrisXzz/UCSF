# -*- coding: utf-8 -*-
import os
import argparse
import pydicom
import dicom2nifti
import shutil
import dicom2nifti.settings as settings

settings.disable_validate_slice_increment()

def clear_temp_dir(temp_dir):
    for file in os.listdir(temp_dir):
        file_path = os.path.join(temp_dir, file)
        if os.path.isfile(file_path) or os.path.islink(file_path):
            os.unlink(file_path)
        elif os.path.isdir(file_path):
            shutil.rmtree(file_path)

def main(base_dicom_dir, base_output_dir, temp_dir):
    if not os.path.exists(base_output_dir):
        os.makedirs(base_output_dir)
    if not os.path.exists(temp_dir):
        os.makedirs(temp_dir)

    for root, dirs, files in os.walk(base_dicom_dir):
        dicom_files = [f for f in files if os.path.isfile(os.path.join(root, f))]
        if not dicom_files:
            continue 

        try:
            series_files = {}

            for dicom_file in dicom_files:
                dicom_path = os.path.join(root, dicom_file)
                ds = pydicom.dcmread(dicom_path, force=True)

                if "SeriesInstanceUID" in ds:
                    uid = ds.SeriesInstanceUID
                    if uid not in series_files:
                        series_files[uid] = []
                    series_files[uid].append(dicom_path)

            for uid, files in series_files.items():
                clear_temp_dir(temp_dir)
                for file in files:
                    shutil.copy(file, temp_dir)

                dicom2nifti.convert_directory(temp_dir, temp_dir, compression=True, reorient=True)

                subfolder_names = root.replace(base_dicom_dir, '').strip(os.sep).replace(os.sep, '_')
                if not subfolder_names:
                    subfolder_names = os.path.basename(base_dicom_dir)  
                    
                for file_name in os.listdir(temp_dir):
                    if file_name.endswith('.nii.gz'):
                        new_name = f"{subfolder_names}_Depth_{len(files)}_{file_name}"
                        shutil.move(os.path.join(temp_dir, file_name), os.path.join(base_output_dir, new_name))

                print(f"Converted SeriesInstanceUID: {uid} with {len(files)} files. Output to {base_output_dir}")

        except Exception as e:
            print(f"Error processing folder '{root}': {e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Convert DICOM files to NIfTI format.")
    parser.add_argument("--base_dicom_dir", type=str, required=True, help="Path to the base DICOM directory.")
    parser.add_argument("--base_output_dir", type=str, required=True, help="Path to the output directory.")
    parser.add_argument("--temp_dir", type=str, required=True, help="Path to the temporary directory.")

    args = parser.parse_args()

    main(args.base_dicom_dir, args.base_output_dir, args.temp_dir)
