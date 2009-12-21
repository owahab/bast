#!/bin/sh

# get the app dir if not already defined 		

if [ -z "$PROGRAM_DIR" ]; then
   PROGRAM_DIR=`dirname "$0"`
fi

exec python -O ${PROGRAM_DIR}/bast.py $@