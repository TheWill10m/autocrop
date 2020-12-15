#!/bin/bash

crop=`ffmpeg -ss 60 -i "$1" -vframes 24 -vf cropdetect -f null - 2>&1 | awk '/crop/ { print $NF }' | tail -1`
echo "$crop" > "$2"crop.txt