import os
import shutil
import nibabel as nib
import numpy as np
from concurrent.futures import ProcessPoolExecutor, as_completed
from tqdm import tqdm

def process_file(file_path, target_path):
    try:
        nii_data = nib.load(file_path).get_fdata()
        min_hu = np.min(nii_data)
        if min_hu > -100:
            file_name = os.path.basename(file_path)
            shutil.move(file_path, os.path.join(target_path, file_name))
    except Exception as e:
        print(f"Error processing {file_path}: {e}")

def gather_tasks(source_path, target_path):
    tasks = []
    for file_name in os.listdir(source_path):
        file_path = os.path.join(source_path, file_name)
        if file_name.endswith(".nii.gz") and os.path.isfile(file_path):
            tasks.append((file_path, target_path))
    return tasks

def move_files(source_path, target_path):
    os.makedirs(target_path, exist_ok=True)

    tasks = gather_tasks(source_path, target_path)

    print(f"Found {len(tasks)} files to process.")
    with ProcessPoolExecutor() as executor:
        futures = {executor.submit(process_file, task[0], task[1]): task for task in tasks}

        for future in tqdm(as_completed(futures), total=len(futures), desc="Processing files"):
            task = futures[future]  
            try:
                future.result()  
            except Exception as e:
                print(f"Error during task execution for {task}: {e}")

if __name__ == "__main__":
    source_path = "E:\\ucsf_post_5k\\out_new\\"  
    target_path = "E:\\ucsf_post_5k\\error\\"  
    
    if not os.path.exists(target_path):
        os.makedirs(target_path)
        
    move_files(source_path, target_path)


