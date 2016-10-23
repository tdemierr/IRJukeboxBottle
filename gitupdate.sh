#!/bin/bash
#Test
echo "Test"
while ! ping -W bitbucket.org; do
	echo "waiting network"
	sleep 1
done
cd /home/pi/IRJukeboxBottle && git pull origin master
echo "pull success"
