#!/bin/bash

# Check for Linux OS
if [[ "$(uname)" != "Linux" ]]; then
  echo "vLLM is only compatible with Linux."
  exit 1
fi

# Set the required compute capability
REQUIRED_COMPUTE_CAPABILITY="7.0"

# Extract the compute capability using nvidia-smi
GPU_CC=$(nvidia-smi --query-gpu=driver_version --format=csv,noheader | head -n 1)
if [[ $(echo "$GPU_CC < $REQUIRED_COMPUTE_CAPABILITY" | bc) -eq 1 ]]; then
  echo "GPU compute capability must be 7.0 or higher. Current compute capability: ${GPU_CC}"
  exit 1
fi

echo "CUDA requirements met: Compute Capability ${GPU_CC}"

# Correcting the VERSION variable assignment
VERSION="$1"

# Correcting the conda create command
conda create -n vllm python=${VERSION} -y
conda activate vllm

pip install vllm fschat accelerate gpustat ray
