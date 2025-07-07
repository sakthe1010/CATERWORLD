#!/bin/bash

set -e

# Ensure folders exist
mkdir -p output temp audio input subtitles

python tts_edge.py

# STEP 1: Create animated video clips from images (5s each)

# 1. Zoom-in effect for image 1
ffmpeg -y -loop 1 -i input/image_1.jpeg -filter_complex \
"[0:v]scale=1400:788,zoompan=z='zoom+0.0005':d=125:s=1280x720:fps=25,format=yuv420p" \
-t 5 temp/slide1.mp4

# 2. Pan right effect for image 2
ffmpeg -y -loop 1 -i input/image_2.jpeg -filter_complex \
"[0:v]scale=1440:720,trim=duration=5,setsar=1,format=yuv420p,crop=1280:720:x='(in_w-1280)*t/5':y=0" \
-r 25 temp/slide2.mp4

# 3. Vertical pan with fade-in for image 3
ffmpeg -y -loop 1 -i input/image_3.jpeg -filter_complex \
"[0:v]scale=1280:1440,trim=duration=5,setsar=1,crop=1280:720:y='(in_h-720)*t/5':x=0,fade=t=in:st=0:d=1,format=yuv420p" \
-r 25 -t 5 temp/slide3.mp4

# STEP 2: Concatenate slides into one video
ffmpeg -y -f concat -safe 0 -i <(printf "file '$PWD/temp/slide1.mp4'\nfile '$PWD/temp/slide2.mp4'\nfile '$PWD/temp/slide3.mp4'") -c:v libx264 -pix_fmt yuv420p temp/temp_video.mp4

# STEP 3: Mix narration and background music (adjust bgm volume down)
ffmpeg -y -i audio/voiceover.wav -i audio/bgm.wav -filter_complex "[1:a]volume=0.2[a1];[0:a][a1]amix=inputs=2:duration=first:dropout_transition=2[aout]" -map "[aout]" -c:a aac -b:a 128k temp/temp_audio.m4a

# STEP 4: Combine final video and mixed audio
ffmpeg -y -i temp/temp_video.mp4 -i temp/temp_audio.m4a -c:v copy -c:a aac -shortest temp/temp_av.mp4

# STEP 5: Generate subtitles using Whisper
whisper audio/voiceover.wav --language English --task transcribe --output_format srt --output_dir subtitles

# STEP 6: Burn subtitles into the final video
ffmpeg -y -i temp/temp_av.mp4 -vf subtitles=subtitles/voiceover.srt -c:a copy output/final_promo.mp4

echo "✅ Final promo video saved to: output/final_promo.mp4"
