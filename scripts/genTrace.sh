#!/bin/bash

BASEDIR=$(pwd)
FILES="$BASEDIR/config/*"
COUNT=0
for f in $FILES
    do
        for ((i=0; i<10; i++))
        do
            cp $f ${f::-7}-$i".config"
            echo ${f::-7}-$i".config"
            python3 tragen_cli.py -c ${f::-7}-$i".config" &
            ((COUNT++))
            if [ $COUNT -eq 4 ]
                then
                    wait
                    COUNT=0
                    mv OUTPUT/* /mydata/traces/
            fi
        done
    done
