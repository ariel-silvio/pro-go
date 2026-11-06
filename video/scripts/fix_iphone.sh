#!/usr/bin/env bash
# Make an iPhone .MOV usable in Descript: HEVC/HDR video -> 1080p30 H.264 (BT.709, natural look, no tone-mapping),
# keep the stereo AAC track (drop Apple spatial audio "apac"), loudness to -16 LUFS.
# Usage: fix_iphone.sh IN.MOV OUT.mp4
set -euo pipefail
in="$1"; out="$2"; tmp="${out%.mp4}.part.mp4"
a=$(ffprobe -v error -select_streams a -show_entries stream=index,codec_name -of csv=p=0 "$in" | awk -F, '$2=="aac"{print $1; exit}')
[ -n "$a" ] || { echo "no stereo AAC track found in $in"; exit 1; }
ffmpeg -y -loglevel error -i "$in" -map 0:v:0 -map 0:"$a" \
  -vf "scale=-2:1080,format=yuv420p" -c:v libx264 -crf 18 -preset medium -r 30 \
  -color_primaries bt709 -color_trc bt709 -colorspace bt709 \
  -af "loudnorm=I=-16:TP=-1.5:LRA=11" -ar 48000 -c:a aac -b:a 192k -ac 2 -movflags +faststart "$tmp"
mv "$tmp" "$out"; echo "wrote $out"
