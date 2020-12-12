#!/bin/bash

echo "Welcome to autcrop"

for input in "Input"/*
do
    echo "$input"
    output=`basename $input`
    crop=`ffmpeg -ss 60 -i $input -vframes 10 -vf cropdetect -f null - 2>&1 | awk '/crop/ { print $NF }' | tail -1`
    echo "Detected crop format: $crop"
    ffmpeg -i $input -t 30 -vf $crop -map 0:v -map 0:a -map 0:s -c:s dvdsub \
    -c:v libx264 -preset fast -crf 22 -c:a \
    copy Output/$output
done