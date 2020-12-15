#!/bin/bash

size=`ls -ls "$1"`
echo "$size" > "$2"size.txt