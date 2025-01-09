# Convert dicom files to nii.gz files
This repo contains python code for converting dicom files to nii.gz files.

### 0. Installation Anaconda and create a virtual environment 

#### 0.1. Please intall Anaconda firstly, you can find Installers [here](https://www.anaconda.com/download/success). 

#### 0.2. Verify Installation

1. Open a new terminal (or Anaconda Prompt for Windows).
2. Check the installation by typing:

```bash
conda --version
```
You should see the version number of Anaconda.

#### 0.3. Create a new environment (optional but highly recommended)

1. Create a new environment

```bash
conda create -n dicom python=3.9
```
Replace dicom with your desired environment name.

2. Activate the environment:

```bash
conda activate dicom
```
#### 0.4. Install required packages

install with pip:
```bash
pip install pydicom
pip install dicom2nifti
```

### 1. Set the path where dicom files are stored

```bash
base_dicom_dir=/path/to/your/dicom_files/folder
# Please modify this to actual path, e.g.,
```

### 2. Set the path to store the converted nifti files

```bash
base_output_dir=/path/to/store/nifti_files/folder
# Please modify this to actual path, e.g.,
```

### 3. Set the temp empty path 

```bash
temp_dir=/path/to/temp_empty/folder
# Please modify this to actual path, e.g.,
```

### 4. Start converting

```bash
python dicom_to_nii.py --base_dicom_dir $base_dicom_dir --base_output_dir $base_output_dir --temp_dir $temp_dir
```