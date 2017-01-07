#!/usr/bin/env bash

#curl http://raspberrypi:8000 > /dev/null; WEB=$?
netstat -ntlp |grep :::8000 > /dev/null; WEB=$? 

if [ $WEB -ne 0 ]
then
	echo "Webserver seems down... $WEB"
	exit
fi

ping -c 1 -w 30 iPhonevonDorian &> /dev/null
UTE=$?

ping -c 1 -w 30 androidfab &> /dev/null
FAB=$?

UTELOCK=/tmp/uteda.lock
FABLOCK=/tmp/fabda.lock

function get_status()
{
if [[ ($FAB -ne 0) && ($UTE -ne 0) ]]
then
	echo "None of us is online"
	if [[ -f $UTELOCK || -f $FABLOCK ]]
	then
		echo "Nobody here till recently -- switch off"
		rm -f $UTELOCK $FABLOCK
		return 255
	fi
fi

if [[ ($FAB -eq 0) && ($UTE -eq 0) ]]
then
	echo "BOTH are online"
	if [[ -f $UTELOCK && -f $FABLOCK ]]
	then
		echo "Both already been here before"
		return 31
	fi
	touch $UTELOCK
	touch $FABLOCK
	return 30
else
	if [[ -f $UTELOCK && -f $FABLOCK ]]
	then
		echo "Last time both've been here but not anymore.. cleaning up locks after em"
		rm -f $UTELOCK $FABLOCK
	fi
fi

if [ $UTE -eq 0 ]
then
	echo "UTE is online $UTE"
	if [ -f $UTELOCK ]
	then
		echo "Ute seems to be here already"
		return 11
	fi
	touch $UTELOCK
	return 10
else
	echo "UTE is offline $UTE"
	if [ -f $UTELOCK ]
	then
		echo "Ute just left"
	fi
	rm -f $UTELOCK
fi

if [ $FAB -eq 0 ]
then
	echo "FAB is online $FAB"
	if [[ -f $FABLOCK ]]
	then
		echo "Fab seems to be here already"
		return 21
	fi
	touch $FABLOCK
	return 20
else
	echo "FAB is offline $FAB"
	if [ -f $FABLOCK ]
	then
		echo "Fab just left"
	fi
	rm -f $FABLOCK
fi

return 0
}

echo "FAB $FAB & UTE $UTE"

get_status; STATUS=$?

echo "Program Status: $STATUS"

case $STATUS in
255)
	curl http://raspberrypi:8000/208/128/56/0 > /dev/null
  ;;
10)
	echo "UTE is online $UTE"
	curl http://raspberrypi:8000/208/128/56/255 > /dev/null
  ;;
20)
	echo "FAB is online $FAB"
	curl http://raspberrypi:8000/255/200/64/200 > /dev/null
  ;;
30)
	echo "BOTH are online"
	curl http://raspberrypi:8000/224/182/42/255 > /dev/null
  ;;
*)
  # Default ?
  ;;
esac
