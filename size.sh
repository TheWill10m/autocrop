#!/bin/bash

size=`stat "$1"`
echo "$size" > "$2"size.txt