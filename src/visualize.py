import nibabel as nib
import matplotlib
matplotlib.use("Qt5Agg")
from nibabel.viewers import OrthoSlicer3D
import os
import glob
import numpy as np


path = '/home/multi-cam17/Documents/mri/clone_repo/ad_classification/temp/sub-OAS30090/sub-OAS30090_ses-M090_run-01_T1w.nii.gz'
paths = glob.glob(path, recursive=True)

for path in paths:

    img = nib.load(path)
    img = nib.as_closest_canonical(img)
    print(img)
    data = img.get_fdata()
    data = data.astype(int)
    print((np.unique(data)))
    print(len(np.unique(data)))
    print(path)
    # data[data!=3.] = 0.0
    # data[data==3.] = 255.


    print(img.shape)
    OrthoSlicer3D(data).show()
