import os
import matplotlib
matplotlib.use("Qt5Agg")
from subprocess import call
import argparse


def mri_convert(path):
    src_dir = os.path.dirname(path)
    des_dir = './results'
    des = os.path.join(des_dir, path.split('/')[-4])
    des_file1 = os.path.join(des, 'norm_to_mni305_1mm.nii.gz')
    des_file2 = os.path.join(des, 'norm_to_mni305_2mm.nii.gz')

    ref1 = '/usr/local/freesurfer/7.4.1/average/mni305.cor.subfov1.mgz' # '/usr/local/freesurfer/7.4.1/average/mni305.cor.nii.gz'
    ref2 = '/usr/local/freesurfer/7.4.1/average/mni305.cor.subfov2.mgz' # '/usr/local/freesurfer/7.4.1/average/mni305.cor.nii.gz'
    os.makedirs(des, exist_ok=True)
    # cmd = f"mri_convert --out_orientation RAS {path} {des_file}"
    # cmd = f"flirt -in {path} -ref {ref} -out {des_file} -omat {des_file.replace('.nii.gz', '.mat')}"
    cmd1 = f'mri_vol2vol --mov {path} --targ {ref1} --lta {src_dir}/transforms/talairach.lta --o {des_file1}'
    cmd2 = f'mri_vol2vol --mov {path} --targ {ref2} --lta {src_dir}/transforms/talairach.lta --o {des_file2}'
    call(cmd1, shell=True)
    call(cmd2, shell=True)

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="Registered transform using the transformation matrix.")
    parser.add_argument('-i', '--input', type=str, required=True, help='Input transformed norm.mgz file path')

    args = parser.parse_args()    
    path = args.input

    mri_convert(path)
