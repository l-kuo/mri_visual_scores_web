import nibabel as nib
import matplotlib
matplotlib.use('TKAgg')
import os
import argparse


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="Registered transform using the transformation matrix.")
    parser.add_argument('-s', '--subject_id', type=str, required=True, help='Subject ID')

    args = parser.parse_args()    

    subject_id = args.subject_id
    path = f'./results/{subject_id}/norm_to_mni305_1mm.nii.gz'
    img = nib.load(path)
    img = nib.as_closest_canonical(img)
    left_img = img.slicer[0:80, 46:142, 9:89]
    right_img = img.slicer[71:151, 46:142, 9:89]
    print(left_img.shape)
    print(right_img.shape)
    os.makedirs(os.path.dirname(path.replace('norm_to_mni305_1mm.nii.gz', 'cropped/norm_to_mni305_1mm.nii.gz')), exist_ok=True)
    nib.save(left_img, path.replace('norm_to_mni305_1mm.nii.gz', 'cropped/norm_to_mni305_1mm_left.nii.gz'))
    nib.save(right_img, path.replace('norm_to_mni305_1mm.nii.gz', 'cropped/norm_to_mni305_1mm_right.nii.gz'))
    print("New Image Saved!!!")