#!/bin/bash
#SBATCH --nodes=1                          # number of nodes
#SBATCH --ntasks=4                        # number of tasks (2 tasks for 2 datasets)
#SBATCH --gpus-per-task=2                  # number of gpu per task (2 GPUs per task)
#SBATCH --cpus-per-task=1                  # number of cores per task
#SBATCH --time=3:00:00                    # time (HH:MM:SS)
#SBATCH --partition=gpu                    # partition
#SBATCH --account=p200149                  # project account
#SBATCH --qos=default                      # SLURM qos
#SBATCH --error=job/%J.err
#SBATCH --output=job/%J.out

# display args
echo "===================================="
echo "ARGS       = $@"
echo "===================================="

echo "====== starting experiment ========="
poetry run ray start --head

# Run the experiment with the appropriate dataset and prompt using srun
srun --exclusive -n 1 -o job/%J-medqa.out -e job/%J-medqa.err \
 poetry run python run.py builder="medqa" \
 prompt="falcon-zeroshot" exp_name="direct-zeroshot" \
 $@ &

srun --exclusive -n 1 -o job/%J-medmcqa.out -e job/%J-medmcqa.err \
 poetry run python run.py builder="medmcqa" \
 prompt="falcon-zeroshot" exp_name="direct-zeroshot" \
 $@ &

# Run the experiment with the appropriate dataset and prompt using srun
srun --exclusive -n 1 -o job/%J-medqa.out -e job/%J-medqa.err \
 poetry run python run.py builder="medqa" \
 prompt="falcon-fewshot" exp_name="5-shot-cot" \
 $@ &

srun --exclusive -n 1 -o job/%J-medmcqa.out -e job/%J-medmcqa.err \
 poetry run python run.py builder="medmcqa" \
 prompt="falcon-fewshot" exp_name="5-shot-cot" \
 $@ &

wait