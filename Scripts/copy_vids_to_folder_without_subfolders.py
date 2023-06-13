#!/usr/bin/env python
import os
import json
import shutil

path_to_vars = "1-AnnChor1000_with_subfolders_24fps/"
save_path = "1-AnnChor1000_24fps_vids/"

def copyvids():

    for folder in os.listdir(path_to_vars):
        try:
            path_to_files = os.path.join(path_to_vars,folder)
            folder_total = 0
            for file in os.listdir(path_to_files):
                if file.endswith(".mp4"):
                    shutil.copy2(path_to_files+"/"+file,save_path+file) 
            print(f"{folder} successfully copied to {save_path}")
        except:
            print(f"{folder} is not a folder!")


if __name__ == "__main__":
    copyvids()