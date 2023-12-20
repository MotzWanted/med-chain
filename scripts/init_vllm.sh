#!/bin/bash

# Get available GPUs using gpustat
available_gpus=$(gpustat -p)

free_gpus_str=""
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
CUDA_VISIBLE_DEVICES=$free_gpus_str poetry run python -m vllm.entrypoints.api_server --model $1 --port $2 --tensor-parallel-size $3 --trust-remote-code --download-dir "/project/scratch/p200149/vllm"
