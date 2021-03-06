#!/bin/bash
#SBATCH --job-name=test_array
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=18
#SBATCH --partition=dept_gpu
#SBATCH --gres=gpu:1
#SBATCH --mem=32gb
#SBATCH --time=2:00:00
#SBATCH --qos=normal
#SBATCH --output=slurm-%A_%a.out
#SBATCH --error=slurm-%A_%a.err
#SBATCH --dependency=singleton

source ~/.bashrc
cd $SLURM_SUBMIT_DIR

JOB_SCRIPTS_FILE=../new_job_scripts_after_debug
if [ ! -f "${JOB_SCRIPTS_FILE}" ];
then
	echo error: file ${JOB_SCRIPTS_FILE} does not exist >&2
	exit
fi

N_JOB_SCRIPTS=$(cat ${JOB_SCRIPTS_FILE} | wc -l)
N_EXAMPLES=10

JOB_SCRIPT_INDEX=$(( (${SLURM_ARRAY_TASK_ID} - 1) / N_EXAMPLES + 1 ))
EXAMPLE_INDEX=$(( (${SLURM_ARRAY_TASK_ID} - 1) % N_EXAMPLES + 1 ))

JOB_SCRIPT=../$(head -n"${JOB_SCRIPT_INDEX}" ${JOB_SCRIPTS_FILE} | tail -n1)
WORK_DIR=$(dirname $JOB_SCRIPT)

echo $SLURM_ARRAY_TASK_ID $JOB_SCRIPT_INDEX $EXAMPLE_INDEX

cd $WORK_DIR
eval $JOB_SCRIPT $WORK_DIR $EXAMPLE_INDEX $SLURM_ARRAY_JOB_ID

exit
