#!/bin/bash

BASEDIR=$(pwd)
FILES="$BASEDIR/config/*"
COUNT=0
for f in $FILES
    do
        python3 tragen_cli.py -c $f &
        ((COUNT++))
        if [ $COUNT -eq 3 ]
            then
                wait
                COUNT=0
                mv OUTPUT/* /mydata/traces/
        fi
    done
