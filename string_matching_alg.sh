#!/bin/bash
#$ -N AcquirerSubAlg_V5
#$ -j y    # join output and error
#$ -t 1-500
source /opt/rh/rh-python36/enable
cd ..
source env/bin/activate
cd AcquirerSubAlg_V5
DATADIR=data
DATAFILE=$DATADIR/$(ls $DATADIR | sed -n ${SGE_TASK_ID}p)
python AcquirerSubAlg.py $DATAFILE


