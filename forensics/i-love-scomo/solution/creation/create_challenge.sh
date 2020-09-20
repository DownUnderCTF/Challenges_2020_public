#!/bin/bash

if [ -z "$1" ]
then
	echo "Need to give a flag";
	exit 1;
fi

FLAG=$1
PASSWORD="iloveyou"

python3 clean_file.py national_anthem.txt &&
python3 WSencoder.py "out.txt" "secret_message.txt" "$FLAG" &&
steghide embed -cf "ilovescomo.jpg" -ef "secret_message.txt" -p "$PASSWORD";
