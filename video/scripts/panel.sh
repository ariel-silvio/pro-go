#!/usr/bin/env bash
# Turns a folder of phone frames (780x1688 JPEGs from film_prototype.cjs) into a 960x1080
# left-half panel: phone on ivory with a hairline border. Usage: panel.sh <framesDir> <out.mp4>
set -euo pipefail
in="$1"; out="$2"; tmp="${out%.mp4}.part.mp4"
ffmpeg -y -loglevel error -framerate 30 -i "$in/%04d.jpg" \
  -vf "scale=-2:900:flags=lanczos,pad=iw+4:ih+4:2:2:color=0xE3DDD3,pad=960:1080:(ow-iw)/2:(oh-ih)/2:color=0xF7F3EC,format=yuv420p" \
  -c:v libx264 -crf 18 -preset veryfast -r 30 -movflags +faststart "$tmp" && mv "$tmp" "$out"
