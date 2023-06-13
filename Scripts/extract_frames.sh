#!/bin/bash

#line=pathToVideo
MAXW=320
MAXH=320

for f in ./*.mp4; do
	filename=$(basename $f)
    echo $filename
    foldername=${filename%.*}
    echo folder: $foldername

    if [ ! -d "/media/margaux/0BF902C330829FBB/1-AnnChor1000_segmented_rgb/$foldername" ] 
    then
        echo "Directory /media/margaux/0BF902C330829FBB/1-AnnChor1000_segmented_rgb/$foldername DOES NOT exists, creating one ..." 
        mkdir -p /media/margaux/0BF902C330829FBB/1-AnnChor1000_segmented_rgb/$foldername
    fi   
    ffmpeg -i "$f" -qscale:v 3 -filter:v "scale='if(gt(a,$MAXW/$MAXH),$MAXW,-1)':'if(gt(a,$MAXW/$MAXH),-1,$MAXH)',fps=fps=24" "/media/margaux/0BF902C330829FBB/1-AnnChor1000_segmented_rgb/${foldername}/${filename%.*}_%0d.jpg";

done


