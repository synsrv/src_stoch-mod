#!/bin/bash


# 1 read out folder

LOCAL_COMPUTE=false
DEBUG=false
CLUSTER='x-men'
TESTRUN='net-test'

TESTDIR_FULL=$1
TESTDIR=$(basename $TESTDIR_FULL)

CODEDIR=$(pwd);

# use timestamp + TESTDIR as working dir name
WDIR=$(date +"%y%m%d_%H%M%S")"_"$TESTDIR;



# 2 copy to location with appropriate file name

mkdir -p ../tests/testing/$WDIR

#rsync -a --exclude='*~' --exclude='.git' \
rsync -a --exclude='*~' --exclude='analysis/' \
      $CODEDIR/ ../tests/testing/$WDIR/src/

rsync -a --delete --exclude='*~' --exclude='__pycache__' \
      $CODEDIR/../analysis-dev/ ../tests/testing/$WDIR/src/analysis



cd ../tests/testing/$WDIR



# 3 read out simulation set up (cores, memory etc...)

source "./src/"$TESTDIR_FULL"simulation.config"

# echo $NPARSIM
# echo $NCORES
# echo $MEMGB


# 4 replace explored_params

cp "./src/"$TESTDIR_FULL"explored_params.py" ./src/model/


# 5 start simulation through run_local with settings from 3)

rm -f nohup.out

nohup ./src/run_local.sh $WDIR $CODEDIR $NPARSIM \
                          $NCORES $MEMGB $LOCAL_COMPUTE \
                          $CLUSTER $TESTRUN $TESTDIR_FULL &





