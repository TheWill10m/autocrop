#!/bin/bash

size=`sha256sum "$1"`
echo "$size" > "$2"size.txt