#!/bin/sh

if [ -z $2 ]
then
	exit 1
fi

while true
do
	./main $1 $2
	if [ $? == 127 ]
	then
		exit 1
	fi
done
