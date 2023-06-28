#!/bin/bash

BASE_DIR="/scratch1/09498/janechen/"
FILES=$BASE_DIR"Tragen/config/*"
for f in $FILES
    do
        for ((i=0; i<10; i++))
        do
            cp $f ${f::-7}-$i".config"
            echo "python3 tragen_cli.py -c "${f::-7}"-"$i".config"
        # done
    done
done
