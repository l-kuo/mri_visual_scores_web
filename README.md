# Alzheimer's Disease and Visual Score Predictions with Brain MRI Scans

The repository is designed to classify Alzheimer's Disease and to predict the visual scores using 3D brain MRI scans in a single pipeline. The detail classes are the following:  

### Alzheimer's Classification
- 0: Normal
- 1: Mild Cognitive Impairment
- 2: Alzheimer's Disease

### Global Cortical Atrophy Score (GCA)
- 0 ~ 3 (4 scores)  

### Left and Right Medial Temporal Lobe Atrophy Score (MTA)
- 0 ~ 4 (5 scores)  

### Left and Right Entorhinal Cortical Atrophy Score (ERICA)
- 0 ~ 3 (4 scores)  

## Instructions
1. To run the pipeline, **FreeSurfer** version 7.X and above is required. Please refer to `https://surfer.nmr.mgh.harvard.edu/fswiki/rel7downloads` for the installation.
1. The working directory is `./ad_classification`.
2. Install the necessary libraries from `requirements.txt`.
3. Put the classification model, GCA model, MTA model and ERICA model weight files into `./models` directory.
4. The input 3D MRI image can be either in .nii or .nii.gz format and placed in `./temp/subject_id/` (Notice that subject_id is unique).

To run the pipeline:  
`./scripts/run_pipeline.sh ./temp/subject_id/T1_mri_filename.nii.gz`

The intermediate processed files are saved in the `./results` directory. The final prediction results are saved in the `predictions.json`.

## Downloads
The weight files can be download from [mri_visual_scores_weights](https://192.168.5.144/share.cgi?ssid=2382304aeaae4e60b8411d6844abdf17)