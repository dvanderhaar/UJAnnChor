#!/usr/bin/env python

import cv2
import datetime
import os
import json

dataset_name = "AnnChor1000_24fps" # Update here
path_to_vids = "/media/1-AnnChor1000_24fps_vids" # Update here
save_json_path = "./"+dataset_name+"_durations.json"
save_stats_path = "./"+dataset_name+"_vid_stats.txt"

def create_overall_vid_duration_json():
    vid_dur_dict = {}
    print("Creating overall vid duration json...")
    total_vids = 0
    total_seconds = 0
    average_length = 0
    max_seconds = 0
    max_frames = 0 

    for f in os.listdir(path_to_vids):
        if f.endswith(".mp4"):
            vid_ID = f[:-4]
            #print(vid_ID)
            total_vids +=1
            try:
                vid_path = os.path.join(path_to_vids,f)
                data = cv2.VideoCapture(vid_path)
                #count number of frames:
                frames = data.get(cv2.CAP_PROP_FRAME_COUNT)
                if frames > max_frames:
                    max_frames = frames
                fps = data.get(cv2.CAP_PROP_FPS)
                print(f"Frame count: {f}: {frames}, FPS: {fps}")
                #calculate video duration:
                vid_dur_seconds = round(frames/fps,2)
                if vid_dur_seconds > max_seconds:
                    max_seconds = vid_dur_seconds
                total_seconds += vid_dur_seconds
                print(f"Duration in seconds: {vid_dur_seconds}")
                vid_dur_dict[vid_ID] = vid_dur_seconds
            except Exception as e:
                print(f,e)
    print("DICT:", vid_dur_dict)
    print("Total number of videos: ", total_vids)
    average_length = total_seconds/total_vids
    print("Average length of videos in seconds:", average_length)
    print("Length of the longest video in seconds:", max_seconds)
    print(f"Length of the longest video in frames: {max_frames} \n")


    vid_dur_json = json.dumps(vid_dur_dict)
    with open(save_json_path,'w') as file:
        file.write(vid_dur_json)
    
    with open(save_stats_path, 'w') as f:
        f.write(f"{dataset_name} stats: \n")
        f.write(f"Total number of videos: {total_vids} \n")
        f.write(f"Average length of videos in seconds: {average_length} \n")
        f.write(f"Length of the longest video in seconds: {max_seconds} \n")
        f.write(f"Length of the longest video in frames: {max_frames} \n")

if __name__ == "__main__":
    create_overall_vid_duration_json()
    print("DONE :)")
