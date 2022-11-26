#!/bin/bash
#SBATCH --verbose
#SBATCH -p aquila,parallel
#SBATCH --time=168:00:00
#SBATCH --nodes=1
#SBATCH --mem=12GB
#SBATCH --mail-type=ALL # select which email types will be sent
#SBATCH --mail-user=NETID@nyu.edu # NOTE: put your netid here if you want emails

#SBATCH --array=0-11 # here the number depends on number of tasks in the array, e.g. 0-11 will create 12 tasks
#SBATCH --output=logs/%A_%a.out # %A is SLURM_ARRAY_JOB_ID, %a is SLURM_ARRAY_TASK_ID
#SBATCH --error=logs/%A_%a.err

# #####################################################
# #SBATCH --gres=gpu:1 # uncomment this line to request a gpu
#SBATCH --constraint=cpu # specify constraint features ('cpu' means only use nodes that have the 'cpu' feature) check features with the showcluster command

sleep $(( (RANDOM%10) + 1 )) # to avoid issues when submitting large amounts of jobs

echo "SLURM_JOBID: " $SLURM_JOBID
echo "SLURM_ARRAY_JOB_ID: " $SLURM_ARRAY_JOB_ID
echo "SLURM_ARRAY_TASK_ID: " $SLURM_ARRAY_TASK_ID

#module load anaconda3 cuda/9.0 glfw/3.3 gcc/7.3 mesa/19.0.5 llvm/7.0.1 # load modules that we might use
module load singularity

echo "Job ID: ${SLURM_ARRAY_TASK_ID}"


singularity exec -B /scratch/$USER/sing/REDQ-fall22-student:/workspace/REDQ -B /scratch/$USER/sing/mujoco-sandbox/opt/conda/lib/python3.8/site-packages/mujoco_py/:/opt/conda/lib/python3.8/site-packages/mujoco_py/ /scratch/$USER/sing/mujoco-sandbox bash -c "
export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/workspace/.mujoco/mujoco210/bin
export MUJOCO_PY_MUJOCO_PATH=/workspace/.mujoco/mujoco210/
export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/usr/local/nvidia/lib
export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/workspace/.mujoco/mujoco210/bin
export MUJOCO_GL=egl
cd /workspace/REDQ/experiments/
python proj1.py --setting ${SLURM_ARRAY_TASK_ID}
"