#!/bin/bash
set -e
for i in {1..5}
do
  echo "grabbing $i/5"
  raspistill -n -t 1 -o $i.jpg
  feh --slideshow-delay 0.2 --cycle-once $i.jpg
done
