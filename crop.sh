#!/bin/bash

echo "Cropping"
echo "True" > transcoding.txt

ffmpeg -t 10 -i Input/"$1" -vf $2 -map 0:v -map 0:a -map 0:s -c:s dvdsub \
-c:v libx265 -preset ultrafast -crf 28 -c:a \
copy Output/"$1"

echo "False" > transcoding.txt

#echo "Welcome to autcrop"
#
#for input in "Input"/*
#do
#    echo "$input"
#    fileName=`basename "$input"`
#    crop=`ffmpeg -ss 60 -i "$input" -vframes 24 -vf cropdetect -f null - 2>&1 | awk '/crop/ { print $NF }' | tail -1`
#    echo "Detected crop format: $crop"
#    ffmpeg -i "$input" -vf $crop -map 0:v -map 0:a -map 0:s -c:s dvdsub \
#    -c:v libx265 -preset slow -crf 22 -c:a \
#    copy ./Output/"$fileName"
#
#    #mv "$input" ./Processed/"$fileName"
#done