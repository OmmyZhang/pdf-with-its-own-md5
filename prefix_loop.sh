#!/bin/sh

date

while ! timeout 1800 python ~/pdf-with-its-own-md5/prefix_loop.py >> ~/pdf-with-its-own-md5/prefix_loop.log
do
	killall md5_diffpathconnect
	echo "Killed.."
	sleep 60
	date
done

echo "Done!!!"
