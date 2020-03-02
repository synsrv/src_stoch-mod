#!/bin/bash

echo ""
echo ""
echo "Running " $1
echo ""

if [ "$8" == "manual" ]; then
    echo "mode: test, manual"
    TESTFLAG='-t'
    DESTINATION='tests/man'
elif [ "$8" == "net-test" ]; then
    echo "mode: test, net-test"
    TESTFLAG='-t'
else
    echo "mode: result run"
    TESTFLAG=''
    DESTINATION='completed'
fi


if $6
then
   echo "doing local"
   python -m src.model.run -c $3 $TESTFLAG
else
   echo "doing nonlocal"
   srun -p $7 -c $4 --mem $5 --time 29-00 python \
	-m src.model.run -c $3 $TESTFLAG
fi

# # with multiprocessing. currently defunct because of a problem
# # with tex locking and memory consumption issues
# srun -p x-men -c $4 --mem $5 python default_analysis.py data/*.hdf5 $3

# final zero sys.argv sets mode to sequential
#cd ../
#echo "Running analysis..."
#mv src/run_analysis_fb.sh .
#./run_analysis_fb.sh


# --------------------------------------------------


if [ "$8" == "net-test" ];
then

    # 6 run python script to analyze expected
    # outputs if in automated testmode!

    python "./src/"$9"tests.py" 2> test.log

    ret=$?
    if [ $ret -ne 0 ]; then
	echo "Error"
    fi

    # # 7 copy log file produced by python

    #mv test.log $CODEDIR


    # # 8 (optional) self destruct


else


    cp src/run_analysis.sh .

    echo "Done."


    CRDIR=$(pwd);


    mkdir -p ../../$DESTINATION/
    mv $CRDIR ../../$DESTINATION/$1

    #echo "Not cleaning up, remove manually"

fi
