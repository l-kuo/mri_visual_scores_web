#!/bin/bash

# Check if the input file and subject_id are provided
if [ "$#" -ne 1 ]; then
    echo "Usage: $0 <path_to_nifti_file>"
    exit 1
fi

# Assign input arguments to variables
INPUT_FILE="$1"
# SUBJECT_ID="$2"
SUBJECT_ID=$(basename $(dirname "$INPUT_FILE"))

# define scripts in pipeline
SCRIPTS=(
    "./src/freesurfer_preprocess.py"
    "./src/registered_transform.py"
    "./src/mta_erica_crops.py"
    "./src/manual_drawing.py"
    "./src/inference.py"
)

# Capture the start time
START_TIME=$(date +%s)

# Run freesurfer_preprocess.py script with the .nii.gz file as an argument
echo "Step 1: Running ${SCRIPTS[0]} with $INPUT_FILE"
python3 "${SCRIPTS[0]}" -i "$INPUT_FILE" || { echo "Failed to run ${SCRIPTS[0]}"; exit 1; }

# Run registered_transform.py script with norm.mgz and subject id inputs
TRANSFORM_INPUT="./temp/${SUBJECT_ID}/${SUBJECT_ID}_freesurfer/mri/norm.mgz"
echo "Step 2: Running ${SCRIPTS[1]} with $TRANSFORM_INPUT"
python3 "${SCRIPTS[1]}" -i "$TRANSFORM_INPUT" || { echo "Failed to run ${SCRIPTS[1]}"; exit 1; }

# Run mta_erica_crops.py script with subject_id inputs as an argument
echo "Step 3: Running ${SCRIPTS[2]} with $SUBJECT_ID"
python3 "${SCRIPTS[2]}" -s "$SUBJECT_ID" || { echo "Failed to run ${SCRIPTS[2]}"; exit 1; }

# Run manual_drawing.py script with subject_id inputs as an argument
echo "Step 4: Running ${SCRIPTS[3]} with $SUBJECT_ID"
python3 "${SCRIPTS[3]}" -s "$SUBJECT_ID" || { echo "Failed to run ${SCRIPTS[3]}"; exit 1; }

# Run inference.py script with subject_id inputs as an argument
echo "Step 5: Running ${SCRIPTS[4]} with $SUBJECT_ID"
python3 "${SCRIPTS[4]}" -s "$SUBJECT_ID" || { echo "Failed to run ${SCRIPTS[4]}"; exit 1; }

# Capture the end time
END_TIME=$(date +%s)

# Calculate the duration
DURATION=$((END_TIME - START_TIME))

# Output the process time
echo "Duration of the process: $DURATION seconds"

echo "All scripts executed successfully."
