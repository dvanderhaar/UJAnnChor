#!/bin/bash

#This script is used as part of pre-processing the data for Coarse-Fine Networks which requires the data in RGB frames at 24FPS
#Run the "copy_vids_to_folder_without_subfolders.py" script to get all videos in the same directory.
#The script runs through the current directory's mp4s and extracts RGB frames.
#Creates a folder for each video which is used to store the resulting RGB frames in order.

MAXW=320
MAXH=320
SAVE_PATH="/path/to/saved_RGBS"

for f in ./*.mp4; do
	filename=$(basename $f)
    echo $filename
    foldername=${filename%.*}
    echo folder: $foldername

    if [ ! -d "$SAVE_PATH/$foldername" ] 
    then
        echo "$SAVE_PATH/$foldername DOES NOT exists, creating one ..." 
        mkdir -p $SAVE_PATH/$foldername
    fi   
    ffmpeg -i "$f" -qscale:v 3 -filter:v "scale='if(gt(a,$MAXW/$MAXH),$MAXW,-1)':'if(gt(a,$MAXW/$MAXH),-1,$MAXH)',fps=fps=24" "$SAVE_PATH/${foldername}/${filename%.*}_%0d.jpg";

done


