if you are using the sample hpc scripts to run jobs, by default the out and err logs will be generated here.
if you want logs to be generated elsewhere, simply change following lines in your job script files.
note that if you generate the logs into a folder (for example "logs") you can get an error if the folder is not there.
#SBATCH --output=logs/%A_%a.out # %A is SLURM_ARRAY_JOB_ID, %a is SLURM_ARRAY_TASK_ID
#SBATCH --error=logs/%A_%a.err