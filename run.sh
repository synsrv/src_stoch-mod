#!/bin/bash

NPARSIM=1
NCORES=1
MEMGB=2
LOCAL_COMPUTE=false
POSTFIX=""
TESTRUN='manual'
TESTDIR_FULL=''
DEBUG=false
CLUSTER='x-men'
DESCRIPTION=''

while getopts "hln:c:m:P:Eds" opt; do
    case $opt in
    h) echo "usage: $0 [-h] [-a] [-l] ..."; exit ;;
    l) LOCAL_COMPUTE=true ;;
    n) NPARSIM=$OPTARG ;;
    c) NCORES=$OPTARG ;;
    m) MEMGB=$OPTARG ;;
    E) TESTRUN="false" ;;
    d) DEBUG=true ;;
    s) CLUSTER='sleuths' ;;
    P) POSTFIX=$OPTARG ;;
    \?) echo "error: option -$OPTARG is not implemented"; exit ;;
    esac
done

if [ "$POSTFIX" == "" ];
then
    read -p "Postfix: " POSTFIX
fi

if [ "$TESTRUN" == "false" ]; 
then
    read -p "Description: " DESCRIPTION
fi    

# echo $NPARSIM
# echo $NCORES
# echo $MEMGB
# echo $POSTFIX
# echo $LOCAL_COMPUTE
# echo $DESCRIPTION


CODEDIR=$(pwd);

# use timestamp + POSTFIX as temporary folder name
TIMESTAMP=$(date +"%y%m%d_%H%M%S")$POSTFIX;


mkdir -p ../running/$TIMESTAMP

#rsync -a --exclude='*~' --exclude='.git' \
rsync -a --exclude='*~' --exclude='analysis/' \
      $CODEDIR/ ../running/$TIMESTAMP/code/

rsync -a --delete --exclude='*~' --exclude='__pycache__' \
      $CODEDIR/../analysis-dev/ ../running/$TIMESTAMP/code/analysis

cd ../running/$TIMESTAMP

# make sure nohup.out doesn't exist
rm -f nohup.out

if [[ ! -z $DESCRIPTION ]];
then
   echo $DESCRIPTION > ./description
fi

if $DEBUG
then
   echo "debug mode" 
   ./code/run_local.sh $TIMESTAMP $CODEDIR $NPARSIM \
                          $NCORES $MEMGB $LOCAL_COMPUTE \
                          $CLUSTER $TESTRUN $TESTDIR_FULL
else
    echo "normal mode"
    nohup ./code/run_local.sh $TIMESTAMP $CODEDIR $NPARSIM \
                          $NCORES $MEMGB $LOCAL_COMPUTE \
                          $CLUSTER $TESTRUN $TESTDIR_FULL &
fi

# # touch $CODEDIR/../$TIMESTAMP


# # run via sbatch -p x-men -c <ncores> --mem 32GB run.sh <ncores>

# # echo "START"
# # running -p x-men -c $1 --mem 32GB python stdp_scl_it_strct_run.py -c $1
# # echo "END"
# # touch end.org
