#!/bin/bash
#SBATCH --job-name=vllm-server
#SBATCH --output=../../../scratch/s183568/vllm_output/%x_%A_%a.out
#SBATCH --error=../../../scratch/s183568/vllm_output/%x_%A_%a.err
#SBATCH --time=24:00:00
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --nodelist=comp-gpu07
#SBATCH --gres=gpu:Turing:4
#SBATCH --cpus-per-task=2
#SBATCH --mem=32GB

echo Running on host $USER@$HOSTNAME
echo Node: $(hostname)
echo Start: $(date +%F-%R:%S)
echo -e Working dir: $(pwd)
echo Dynamic shared libraries: $LD_LIBRARY_PATH

# Load CUDA module
module load CUDA/11.7

# Source credentials
source credentials.txt

# Get available GPUs using gpustat
available_gpus=$(gpustat -p)

# Initialize a variable to store free GPU indices as a string
free_gpus_str=""

# Set a counter to track the line number
line_number=0

# Iterate through each line in gpustat
IFS=$'\n' # Set Internal Field Separator to newline to iterate over lines
for line in $available_gpus; do

  # Increment the line number
  ((line_number++))

  # Skip the first line
  if [ "$line_number" -eq 1 ]; then
    continue
  fi
  # Extract the fourth column (after the third "|")
  name_after_vram=$(echo "$line" | awk -F "|" '{gsub(/ /,"",$4); print $4}')

  # Check if there are characters after the third "|"
  if [ -z "$name_after_vram" ]; then
    # Add the GPU index to the array of free GPUs
    gpu_index=$(echo "$line" | cut -c2)
    # Add a comma and space if the string is not empty
    [ -n "$free_gpus_str" ] && free_gpus_str+=", "

    # Concatenate gpu_index to free_gpus_str
    free_gpus_str+="$gpu_index"
  fi
done

# Check if any free GPUs are available
if [ -z "$free_gpus_str" ]; then
  echo "No GPUs with an empty fourth column available. Exiting."
  exit 1
fi

# Display the concatenated GPU indices
echo "Free GPU indices: $free_gpus_str"

# Set CUDA_VISIBLE_DEVICES and run your Python script
CUDA_VISIBLE_DEVICES=$free_gpus_str poetry run python -m vllm.entrypoints.openai.api_server --model $1 --port $2 --tensor-parallel-size 4

