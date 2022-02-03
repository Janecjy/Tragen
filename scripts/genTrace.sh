#!/bin/bash

BASEDIR=$(pwd)
FILES="$BASEDIR/config/*"
COUNT=0
for f in $FILES
    do
        python tragen_cli.py -c $f > $COUNT.out &
        ((COUNT++))
        if [ $COUNT -eq 5 ]
            then
                wait
                COUNT=0
        fi
    done
