from multiprocessing import Pool
import time
import subprocess
import os
import shutil
import argparse


def reconall(args):
    path, cores_per_process = args
    start = time.time()
    splitted = path.split('/')
    subjects_dir = os.path.dirname(path)
    subject_name = os.path.basename(subjects_dir)+"_freesurfer"
    print('subjects_dir: ', subjects_dir)
    print('subject_name: ', subject_name)
    os.environ["SUBJECTS_DIR"] = subjects_dir
    destination = os.path.join(subjects_dir, subject_name)
    print(destination)
    if os.path.isdir(destination):
        print("DIR Detected! Processing to Delete!!!")
        shutil.rmtree(destination)
        print(f"Directory '{destination}' removed successfully.")

    # Run for multiprocessing recon-all ###
    try:
        cmd = f'recon-all -autorecon1 -gcareg -canorm -i {path} -s {subject_name} -openmp {cores_per_process}'
        subprocess.run(cmd, shell=True, check=True)
        end = time.time()
        duration = end - start
    except Exception as e:
        print(f'Reconall Process Error {e}')
        end = time.time()
        duration = end - start
    return duration


if __name__ == '__main__':

    parser = argparse.ArgumentParser(description="Input nifti file for recon-all process.")
    parser.add_argument('-i', '--input', type=str, required=True, help='Input nifti file')
    parser.add_argument('-v', '--verbose', action='store_true', help='Enable verbose output')
    args = parser.parse_args()

    path = args.input
    cores_per_process = os.cpu_count()
    verbose = args.verbose

    if verbose:
        print(f"Processing input file: {path}")

    process_starts = time.time()
    duration = reconall([path, cores_per_process])
    print("Process Duration :", duration)

 
    process_ends = time.time()
    print("Total duration : ", process_ends - process_starts)