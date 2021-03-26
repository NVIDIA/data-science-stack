#!/bin/sh

# the name for the transient docker image
IMG=foo


# use 128 for 16G cards
# batch size 16 takes less than 5 GB of GPU mem
BATCH_SIZE=256
RUN_EPOCHS=15
# set to 0 for a CPU only test
# on a multi-gpu machine, setting to > 1 works
# but the test has overhead so the results are not representative
GPUS=1

# this setting should likely match the number of cores in the system
# this is the number of cores to use for the dataloader
WORKERS=16

echo `date` building docker image
docker build -t ${IMG} -f Dockerfile .

echo `date` launching...

# the idea is to do two runs and time the second
# because the first (shorter, 1 epoch) run will download and prepare / cache the data we don't care about timing that
docker run --rm --ipc=host ${IMG} /test.sh ${BATCH_SIZE} ${RUN_EPOCHS} ${GPUS} ${WORKERS}

# docker rmi ${IMG}
echo `date` all done
