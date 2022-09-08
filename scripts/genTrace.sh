#!/bin/bash

BASEDIR=$(pwd)
FILES="$BASEDIR/config/*"
COUNT=0
for f in $FILES
    do
        python tragen_cli.py -c $f &
        ((COUNT++))
        if [ $COUNT -eq 3 ]
            then
                wait
                COUNT=0
        fi
    done
