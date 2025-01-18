import os
import re
import shutil
import nibabel as nib
from collections import defaultdict
from concurrent.futures import ProcessPoolExecutor, as_completed
from tqdm import tqdm

def process_case(case_name, files, input_dir, output_dir):

    unsatisfied = False
    valid_files = [file for file in files if file[3][0] == file[3][1]]

    if valid_files:
        max_file = max(valid_files, key=lambda x: x[2]) 
    else:
        max_file = max(files, key=lambda x: x[2])
        unsatisfied = True 

    filename, scan_sequence, _, _ = max_file

    case_folder = os.path.join(output_dir, f"{case_name}_{scan_sequence}")
    os.makedirs(case_folder, exist_ok=True)
    segmentations_folder = os.path.join(case_folder, "segmentations")
    os.makedirs(segmentations_folder, exist_ok=True)

    src_path = os.path.join(input_dir, filename)
    dest_path = os.path.join(case_folder, "ct.nii.gz")
    shutil.copy(src_path, dest_path)

    return unsatisfied, case_name

def parse_input_directory(input_dir):
    case_files = defaultdict(list)

    for filename in os.listdir(input_dir):
        if filename.endswith('.nii.gz'):
            match = re.match(r'(.*?)_(.*?)_Depth_(\d+)_.*\.nii\.gz', filename)
            if match:
                case_name = match.group(1)
                scan_sequence = match.group(2)
                depth_value = int(match.group(3))

                file_path = os.path.join(input_dir, filename)
                nii_data = nib.load(file_path)
                dimensions = nii_data.shape

                case_files[case_name].append((filename, scan_sequence, depth_value, dimensions))

    return case_files

def process_files(input_dir, output_dir):

    os.makedirs(output_dir, exist_ok=True)

    case_files = parse_input_directory(input_dir)

    unsatisfied_cases = []
    with ProcessPoolExecutor() as executor:
        futures = {executor.submit(process_case, case_name, files, input_dir, output_dir): case_name 
                   for case_name, files in case_files.items()}

        for future in tqdm(as_completed(futures), total=len(futures), desc="Processing cases"):
            case_name = futures[future]
            try:
                unsatisfied, case_name = future.result()
                if unsatisfied:
                    unsatisfied_cases.append(case_name)
            except Exception as e:
                print(f"Error processing {case_name}: {e}")

    unsatisfied_cases_path = os.path.join(output_dir, "xy_unsatisfied_cases.txt")
    with open(unsatisfied_cases_path, "w") as f:
        for case_name in unsatisfied_cases:
            f.write(case_name + "\n")

if __name__ == "__main__":
    input_directory = 'E:\\ucsf_post_5k\\out_new\\'  
    output_directory = 'E:\\ucsf_post_5k\\upload\\' 
    process_files(input_directory, output_directory)


