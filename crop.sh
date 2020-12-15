#!/bin/bash

tsp ffmpeg -i Input/"$1" -vf $2 -map 0:v -map 0:a -map 0:s -c:s dvdsub \
-c:v libx265 -preset slow -crf 22 -c:a \
copy Output/"$1"