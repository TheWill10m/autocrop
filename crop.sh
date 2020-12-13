#!/bin/bash

echo "Welcome to autcrop"

set workingDir=""

for input in "$workingDir/Input"/*
do
    echo "$input"
    fileName=`basename $input`
    crop=`ffmpeg -ss 60 -i $input -vframes 24 -vf cropdetect -f null - 2>&1 | awk '/crop/ { print $NF }' | tail -1`
    echo "Detected crop format: $crop"
    ffmpeg -i $input -vf $crop -map 0:v -map 0:a -map 0:s -c:s dvdsub \
    -c:v libx265 -preset slow -crf 22 -c:a \
    copy $workingDir/Output/$fileName

    mv $input $workingDir/Processed
done