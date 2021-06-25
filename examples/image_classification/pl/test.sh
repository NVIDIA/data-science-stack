#!/bin/bash


if [ $# -lt 4 ]
then
  echo "use: test.sh <batch_size> <epochs> <gpus> <num_workers>"
  exit 1
fi

BATCH="$1"
EPOCHS="$2"
GPUS="$3"
WORKERS="$4"

echo "warmup run starting"
python /workspace/pytorch-lightning/pl_examples/domain_templates/computer_vision_fine_tuning.py --epochs 1 --batch-size ${BATCH} --gpus ${GPUS} --num_workers ${WORKERS} 

echo "running timed test"
time python /workspace/pytorch-lightning/pl_examples/domain_templates/computer_vision_fine_tuning.py --epochs ${EPOCHS} --batch-size ${BATCH} --gpus ${GPUS} --num_workers ${WORKERS}

