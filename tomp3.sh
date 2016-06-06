#!/bin/bash
for a in ./*.flac; do
    ffmpeg -i "$a" -qscale:a 2 "${a[@]/%flac/mp3}"
done
