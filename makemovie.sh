#!/usr/bin/sh

# make movie from bestoverdistance graphs

ffmpeg -i %04d.png -r 10 -pix_fmt yuv420p -profile:v baseline -vcodec libx264 -b:v 500000 year.mp4
