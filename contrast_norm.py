import os
import nibabel as nib
import numpy as np
import argparse
from concurrent.futures import ProcessPoolExecutor, as_completed
from multiprocessing import cpu_count
from tqdm import tqdm

def normalize_image(image, min_val=-1000, max_val=1000):
    image[image > max_val] = max_val
    image[image < min_val] = min_val
    normalized_image = image
    
    return normalized_image

def process_file(file_path):

    img = nib.load(file_path)
    img_data = np.array(img.dataobj)
    '''
    ### Lock this part when hanle non-GPPH style data
    slope = 1
    intercept = -1024
    img_data = img_data * slope + intercept
    ###
    '''
    normalized_data = normalize_image(img_data)

    normalized_img = nib.Nifti1Image(normalized_data, img.affine, img.header)

    normalized_img.set_data_dtype(np.int16)
    normalized_img.get_data_dtype(finalize=True)
    
    nib.save(normalized_img, file_path)
    return file_path



def normalize_ct_images(directory):
    tasks = []
    for root, _, files in os.walk(directory):
        for file in files:
            if file == 'ct.nii.gz':
                file_path = os.path.join(root, file)
                tasks.append(file_path)
    return tasks

def main():
    parser = argparse.ArgumentParser(description="Normalize CT images")
    parser.add_argument('--directory', default = 'E:\\ucsf_post_5k\\upload\\', help='The directory containing the ct.nii.gz files.')
    args = parser.parse_args()

    tasks = normalize_ct_images(args.directory)
    
    print('>> {} CPU cores are secured.'.format(cpu_count()))
    with ProcessPoolExecutor(max_workers=cpu_count()) as executor:
        futures = {executor.submit(process_file, task): task for task in tasks}

        for future in tqdm(as_completed(futures), total=len(futures), desc='Normalizing and converting CT images'):
            task = futures[future]
            try:
                future.result()
            except Exception as e:
                print(f"Error processing {task}: {e}")

if __name__ == '__main__':
    main()


