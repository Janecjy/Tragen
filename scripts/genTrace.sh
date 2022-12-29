#!/bin/bash

BASEDIR=$(pwd)
FILES="$BASEDIR/config/*"
COUNT=0
mkdir -p /mydata/traces/
for f in $FILES
    do
        # for ((i=0; i<3; i++))
        # do
        #     cp $f ${f::-7}-$i".config"
        #     echo ${f::-7}-$i".config"
        python3 tragen_cli.py -c ${f::-7}".config" &
        ((COUNT++))
        if [ $COUNT -eq 4 ]
            then
                wait
                COUNT=0
                mv OUTPUT/* /mydata/traces/
        fi
        # done
    done
wait
mv OUTPUT/* /mydata/traces/
rm -rf /mydata/traces/debug.txt
rm -rf /mydata/traces/logfile.txt
