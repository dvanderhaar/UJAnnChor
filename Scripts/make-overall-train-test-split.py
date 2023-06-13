#!/usr/bin/env python
import os
import json

ratio = 0.8

tf_fps_folder = "1-AnnChor1000_25fps/" #25 frames per second folder with subfolders for each Variation # Update here

orig_class_names = [ 'ExtDerriereOnRight','ExtDerriereOnLeft','Courus','EchappeSecond','CabrioleDevantRight',\
                    'CabrioleDevantLeft','GrandJeteRight','GrandJeteLeft','PirouetteRight','PirouetteLeft',\
                    'SissonneFRight','SissonneFLeft','ExtensionSecondRight','ExtensionSecondLeft','TourEnLair',\
                        'CabrioleDerriereRight','CabrioleDerriereLeft','WaltzRight','WaltzLeft']

new_class_names = ['ExtDerriere','Courus','EchappeSecond','CabrioleDevant','GrandJete','Pirouette','SissonneF','ExtensionSecond','TourEnLair','CabrioleDerriere','WaltzStep']

def create_tt_split(VAR):
    path_to_varvids = tf_fps_folder + VAR
    vid_list =[]
    tt_list =[]
    tt_dict = {}
    total_var_vids = 0 # to count the number of videos in the folder
    try:
        vid_files = sorted([file for file in os.listdir(path_to_varvids)])
        for file in vid_files:
            if file.endswith(".mp4"):
                #print(file)
                vid_ID = file[:-4]
                #print(vid_ID)
                if tt_dict.get(vid_ID) is None: #mechanism to count number of vids
                    tt_dict[vid_ID] = ''
                    vid_list.append(vid_ID)
                    total_var_vids += 1

        num_train = round(ratio * total_var_vids)
        num_test = total_var_vids - num_train
        print(f"Num train: {num_train} Num test: {num_test}")
        tt_list = ["training"]*num_train + ["testing"]*num_test
        print(tt_list)
        result_dict = dict(zip(vid_list,tt_list)) #merge lists to make dictionary
        print(result_dict)
        return result_dict
    except Exception as e:
        print("LOL not a folder.", e)
        return None
    
if __name__ == "__main__":
    overall_tt_dict ={}
    for folder in os.listdir(tf_fps_folder):
        train_test_split_dict = create_tt_split(folder)
        if train_test_split_dict is None:
            continue
        overall_tt_dict.update(train_test_split_dict)
    print("Overall Train_Test_Dictionary: ",overall_tt_dict)
    save_tt_json = json.dumps(overall_tt_dict)
    save_tt_json_path = "./overall_tt_split.json"
    with open(save_tt_json_path,'w') as f:
        f.write(save_tt_json)