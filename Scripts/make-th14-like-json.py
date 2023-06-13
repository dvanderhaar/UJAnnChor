#!/usr/bin/env python
import os
import json

dsname = "AnnChor260-TD" # Update here

base_path = "/media/" # Update here
durationfile_path = base_path+"AnnChor1000_25fps_durations.json" # Update here
tt_splitfile_path = base_path+"overall_tt_split.json" # Update here
save_th_AnnChor_path = base_path + dsname+".json"

#videos_with_subfolders_path = "./1-AnnChor1000_25fps"
csv_annotations_path = "/media/path_to_csv_annotation_files" # Update here

orig_class_names = [ 'ExtDerriereOnRight','ExtDerriereOnLeft','Courus','EchappeSecond','CabrioleDevantRight',\
                    'CabrioleDevantLeft','GrandJeteRight','GrandJeteLeft','PirouetteRight','PirouetteLeft',\
                    'SissonneFRight','SissonneFLeft','ExtensionSecondRight','ExtensionSecondLeft','TourEnLair',\
                        'CabrioleDerriereRight','CabrioleDerriereLeft','WaltzRight','WaltzLeft']

new_class_names = ['ExtDerriere','Courus','EchappeSecond','CabrioleDevant','GrandJete','Pirouette','SissonneF','ExtensionSecond','TourEnLair','CabrioleDerriere','WaltzStep']



def create_JSON():
    count = 0
    #Load the train-test json into memory:
    with open(tt_splitfile_path) as ttf:
        tt_split_json = json.load(ttf)

    #Load the vid-duration json into memory:
    with open(durationfile_path) as df:
            duration_json = json.load(df)

    json_dict = {}
    json_dict["version"] = "AnnChor1000-25fps"
    json_dict["database"] = {}
    #print(json_dict)
    map_dict = create_map_dict()
    #print(sorted(os.listdir(videos_with_subfolders_path)))
    for csvFile in os.listdir(csv_annotations_path):
        path_to_csv = os.path.join(csv_annotations_path,csvFile)
        if csvFile.endswith(".csv"):
            try:
                lines = open(path_to_csv,'r').readlines()[2:] # read from line 2 onwards...
            except Exception as e:
                print("Error: ",e)
            
            for line in lines:
                try:
                    l = line.split(",")
                    vid_ID = l[1].split('\\\\')[3].replace('"','')[:-5]

                    # determine the kind of label:
                    j = l[4].replace('"','')
                    j = j.strip("{}\n").split(":") # j[0] is 'OnlyOneDancer?' or "BalletSteps", j[1] is the value
                    #print(j[0])

                    cl = 0
                    onlyOne = 0
                    if j[0].lower() != 'BalletSteps'.lower(): #if it's not a balletstep label
                        if j[0].lower() == 'OnlyOneDancer?'.lower(): # check if it's a flag for only one dancer
                            onlyOne = int(j[1])
                    elif int(j[1])==19: # Skip if the annotation is for backwards for now
                        continue
                    else:
                        cl =int(j[1]) # otherwise it is a ballet step  class label
                    # map the class to its model class number 0-10:
                    mc = map_dict[cl]
                    class_name = new_class_names[mc]

                    if json_dict["database"].get(vid_ID) is None: #if there is no entry for this vid id:
                        json_dict["database"][vid_ID] = {}
                        json_dict["database"][vid_ID]["subset"] = tt_split_json[vid_ID]
                        json_dict["database"][vid_ID]["duration"] = duration_json[vid_ID]
                        json_dict["database"][vid_ID]["fps"] = 25.0
                        json_dict["database"][vid_ID]["annotations"] = []

                    if not (l[2] =='' or l[3]==''): #if there are temporal annotations
                        count += 1
                        start = float(l[2])
                        end = float(l[3])
                        startframe = round(start*25,2)
                        endframe = round(end*25,2)
                        #format the annotation to alingn with thumos14:
                        ann_obj = {"label":class_name,"segment":[start, end], "segment(frames)":[startframe,endframe],"label_id":mc}
                        json_dict["database"][vid_ID]["annotations"].append(ann_obj)
                    else:
                        continue
                except Exception as e:
                    print(f"Issue here {csvFile}:", e)
                    #print(csvFile,e)
    #print("Dictionary: ",json_dict)
    made_json = json.dumps(json_dict)
    with open(save_th_AnnChor_path, "w") as file:
         file.write(made_json)
    print("No. Annotations: ", count)

def create_map_dict():
    map_dict = {0:0, 1:0, 2:1, 3:2, 4:3, 5:3, 6:4, 7:4, 8:5, 9:5, 10:6, 11:6, 12:7, 13:7, 14:8, 15:9, 16:9, 17:10, 18:10}
    return map_dict

if __name__ == "__main__":
    print("Creating Thumos-like Annotation json for AnnChor...")
    create_JSON()
    print("DONE :)")
    
