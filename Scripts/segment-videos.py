#!/usr/bin/env python
import os
import json
import shutil

#script to segment videos to ensure no video of the AnnChor dataset is longer than 1280 frames/ 53 seconds.
#To align more to the Charades dataset used with CF networks which has an average video length of 30s

videos_src_folder = "./ToSegmentLast/" # Update here
save_folder = "./ToSegmentLast_Done/" # Update here

ffmpeg_flags = "-y"

def segment_videos(VAR):
    save_path = save_folder + VAR + "/"
    if not os.path.exists(save_path):
        os.makedirs(save_path)
        print("Save Directory created")
    else:
        print("Save directory already exists")

    videos_src_path = videos_src_folder + VAR + "/"

    json_data = {}
    new_json_data = {}

    # Load the Json object for the varation that contains for each video:
    # 1. Duration of the video
    # 2. The annotations for each video
    try:
        with open(videos_src_path + VAR + "_json.json") as openfile:
            json_data = json.load(openfile)
    except Exception as e:
        print(e)
        return

    print("original json: ", json_data)

    #loop through each dictionary entry.
    for vid in json_data:
        #print(vid)
        #print(json_data[vid]["duration"]) # duration of the video
        vid_dur = round(json_data[vid]["duration"],3)
        # 1. Check the length of the video - must it be cut into two or three parts?
        # NO SPLIT NEEDED:
        if vid_dur <= 53:
             print(f"{vid} does not need to be segmented")
             # have to copy over the video as is and update the json accordingly
             shutil.copy2(videos_src_path+vid+".mp4",save_path+vid+".mp4") #copy the metadata as well.
             if new_json_data.get(vid) is None: # copy the original json as well
                 new_json_data[vid] = {}
                 new_json_data[vid]["subset"] = json_data[vid]["subset"]
                 new_json_data[vid]["duration"] = json_data[vid]["duration"]
                 new_json_data[vid]["onlyonedancer"] = json_data[vid]["onlyonedancer"]
                 new_json_data[vid]["actions"] = []
                 #loop through actions in original json_data:
                 for i in range(len(json_data[vid]["actions"])):
                    cl = json_data[vid]["actions"][i][0]
                    st_ann = json_data[vid]["actions"][i][1]
                    et_ann = json_data[vid]["actions"][i][2]
                    new_json_data[vid]["actions"].append([cl,st_ann,et_ann])
                 

        # SPLIT IN TWO:
        if vid_dur > 53 and vid_dur <=106:
            print(f"{vid} to be split into 2")
            #find halfway mark of the video in seconds
            halfway = round(vid_dur/2,3)
            print(f"{vid} to be cut into two at {halfway}")
            #First check if the halfway mark overlaps with any existing annotations, if so, update the halfway value
            hw_total_actions = 0
            for i in range(len(json_data[vid]["actions"])):
                hw_total_actions +=1
                st = json_data[vid]["actions"][i][1]
                et = json_data[vid]["actions"][i][2]
                if st < halfway < et: # marker lies between a start time and end time
                    print(f"Yes, for {vid}, {halfway} falls in the range between {st} and {et}")
                    if (halfway-st) < (et-halfway): # if it's closer to st:
                        halfway = st
                        print(halfway)
                    else: # otherwise update it to be the et
                        halfway = et
                        print(halfway)
            print(f"Total number of actions for {vid}: {hw_total_actions}")
            vid_id1 = vid+"_1"
            vid_id2 = vid+"_2"

            #clip from beginning to halfway time:
            command = "ffmpeg -ss 00:00:00 -accurate_seek -to " + str(halfway) + " -i " + videos_src_path + vid +".mp4 -c:v libx264 -c:a aac " + save_path + vid_id1+".mp4" + f" {ffmpeg_flags}"
            os.system(command)

            #update json
            if new_json_data.get(vid_id1) is None:
                new_json_data[vid_id1] = {}
                new_json_data[vid_id1]["subset"] = json_data[vid]["subset"]
                new_json_data[vid_id1]["duration"] = halfway
                new_json_data[vid_id1]["onlyonedancer"] = json_data[vid]["onlyonedancer"]
                new_json_data[vid_id1]["actions"] =[]
                #loop through actions in original json_data:
                
                hwtotal1 = 0
                for i in range(len(json_data[vid]["actions"])):
                    #check if the action falls within halfway mark by checing end time: et <= halfway
                    if json_data[vid]["actions"][i][2] <= halfway:
                        hwtotal1 +=1
                        cl = json_data[vid]["actions"][i][0]
                        st_ann = json_data[vid]["actions"][i][1]
                        et_ann = json_data[vid]["actions"][i][2]
                        new_json_data[vid_id1]["actions"].append([cl,st_ann, et_ann])
                print(f"Total num actions for {vid} clip 1: {hwtotal1}")

            #clip from halfway mark to the end:
            command = "ffmpeg -ss "+ str(halfway) + " -accurate_seek -i " + videos_src_path +vid +".mp4 -c:v libx264 -c:a aac " + save_path+vid_id2+".mp4" + f" {ffmpeg_flags}"
            os.system(command)

            #update json
            if new_json_data.get(vid_id2) is None:
                new_json_data[vid_id2] = {}
                new_json_data[vid_id2]["subset"] = json_data[vid]["subset"]
                new_json_data[vid_id2]["duration"] = round(vid_dur - halfway,3)# subtract from the end marker to get the new duration
                new_json_data[vid_id2]["onlyonedancer"] = json_data[vid]["onlyonedancer"]
                new_json_data[vid_id2]["actions"] = []
                #loop through actions in original json_data:
                hwtotal2 = 0
                for i in range(len(json_data[vid]["actions"])):
                    #check if the action falls between the halfway and end of video: st >= halfway
                    if json_data[vid]["actions"][i][1] >= halfway:
                        hwtotal2 +=1
                        cl2 = json_data[vid]["actions"][i][0]
                        st2_ann = json_data[vid]["actions"][i][1] - halfway #have to subtract the halfway marker for updated st timestamp
                        et2_ann = json_data[vid]["actions"][i][2] - halfway #have to subtract the halfway marker for updated et timestamp
                        new_json_data[vid_id2]["actions"].append([cl2, round(st2_ann,3), round(et2_ann,3)])
                        #new_json_data[vid_id2]["actions"].append([cl2, st3_ann, et3_ann]) #without rounding off
                print(f"Total num actions for {vid} clip 2: {hwtotal2}")


        # SPLIT IN THREE:
        if vid_dur > 106 and vid_dur <=159:
            onethird = round(vid_dur/3,3)
            twothirds = round(onethird*2,3)
            print(f" {vid} To be cut into 3 at {onethird} and at {twothirds}")

            ct_total_actions = 0
            #First check if the onethird mark or twothrids marks overlap with an existing annotations, if so, update the onthird/twothird values
            for i in range(len(json_data[vid]["actions"])):
                 ct_total_actions+=1
                 #print(json_data[vid]["actions"][i]) # inspect each annotation one at a time:
                 st = json_data[vid]["actions"][i][1]
                 et = json_data[vid]["actions"][i][2]
                 #if onethird > st and onethird < et:
                 if st < onethird < et:
                    print(f"Yes, for {vid}, {onethird} falls in the range between {st} and {et}")
                    #update the onethird value
                    #check if onethird is closer to st:
                    if (onethird-st) < (et-onethird):
                        onethird = round(st,3) #update the cut value to the st
                        print(onethird)
                    else: # if the distance is the same or its closer to the end cut at the end time (et) 
                        onethird = round(et,3) #update the cut value to et
                        print(onethird)
                 if st < twothirds < et:
                    print(f"Yes, for {vid}, {twothirds} falls in the range between {st} and {et}")
                    #update the twothirds value
                    if (twothirds-st) < (et-twothirds):
                        twothirds = round(st,3) #upate the cut value to st
                        print(twothirds)
                    else:
                        twothirds = round(et,3)
                        print(twothirds)
            print(f"Total num actions for {vid}: {ct_total_actions}")
            #create new vid_ids for output segments:
            vid_id1 = vid+"_1"
            vid_id2 = vid+"_2"
            vid_id3 = vid+"_3"

            #clip from beginning to onethird time:
            command = "ffmpeg -ss 00:00:00 -accurate_seek -to " + str(onethird) + " -i " + videos_src_path + vid +".mp4 -c:v libx264 -c:a aac " + save_path + vid_id1+".mp4" + f" {ffmpeg_flags}" 
            os.system(command)

            #update json:
            if new_json_data.get(vid_id1) is None:
                new_json_data[vid_id1] = {}
                new_json_data[vid_id1]["subset"] = json_data[vid]["subset"]
                new_json_data[vid_id1]["duration"] = onethird
                new_json_data[vid_id1]["onlyonedancer"] = json_data[vid]["onlyonedancer"]
                new_json_data[vid_id1]["actions"] =[]
                #loop through actions in original json_data:
                atotal1 = 0
                for i in range(len(json_data[vid]["actions"])):
                    #check if the action falls within onethird mark by checing end time: et <= onethird
                    if json_data[vid]["actions"][i][2] <= onethird:
                        atotal1 +=1
                        cl = json_data[vid]["actions"][i][0]
                        st_ann = json_data[vid]["actions"][i][1]
                        et_ann = json_data[vid]["actions"][i][2]
                        new_json_data[vid_id1]["actions"].append([cl,st_ann, et_ann])
                print(f"Total num actions for {vid} clip 1: {atotal1}")

            #clip from onethird time to twothirds time:
            command = "ffmpeg -ss " + str(onethird) + " -accurate_seek -to "+ str(twothirds) + " -i " + videos_src_path +vid + ".mp4 -c:v libx264 -c:a aac " + save_path+vid_id2+".mp4" + f" {ffmpeg_flags}"  
            os.system(command)

            #update json:
            if new_json_data.get(vid_id2) is None:
                new_json_data[vid_id2] = {}
                new_json_data[vid_id2]["subset"] = json_data[vid]["subset"]
                new_json_data[vid_id2]["duration"] = round(twothirds - onethird,3) # subtract from the twothirds marker to get the new duration
                new_json_data[vid_id2]["onlyonedancer"] = json_data[vid]["onlyonedancer"]
                new_json_data[vid_id2]["actions"] = []
                 #loop through actions in original json_data:
                atotal2 = 0
                for i in range(len(json_data[vid]["actions"])):
                    #check if the action falls between the onethird and twothird mark: st >= onethird and et <= twothirds
                    if json_data[vid]["actions"][i][1] >= onethird and json_data[vid]["actions"][i][2] <= twothirds:
                        atotal2 +=1
                        cl2 = json_data[vid]["actions"][i][0]
                        st2_ann = json_data[vid]["actions"][i][1] - onethird #have to subtract the onethird marker for updated st timestamp
                        et2_ann = json_data[vid]["actions"][i][2] - onethird #have to subtract the onethird marker for updated et timestamp
                        new_json_data[vid_id2]["actions"].append([cl2, round(st2_ann,3), round(et2_ann,3)])
                        #new_json_data[vid_id2]["actions"].append([cl2, st2_ann, et2_ann]) #without rounding off
                print(f"Total num actions for {vid} clip 2: {atotal2}")

            #clip from twothirds time to end:
            command = "ffmpeg -ss "+ str(twothirds) + " -accurate_seek -i " + videos_src_path +vid +".mp4 -c:v libx264 -c:a aac " + save_path+vid_id3+".mp4" + f" {ffmpeg_flags}"
            os.system(command)

            #update json:
            if new_json_data.get(vid_id3) is None:
                new_json_data[vid_id3] = {}
                new_json_data[vid_id3]["subset"] = json_data[vid]["subset"]
                new_json_data[vid_id3]["duration"] = round(vid_dur - twothirds,3)# subtract from the end marker to get the new duration
                new_json_data[vid_id3]["onlyonedancer"] = json_data[vid]["onlyonedancer"]
                new_json_data[vid_id3]["actions"] = []
                #loop through actions in original json_data:
                atotal3 = 0
                for i in range(len(json_data[vid]["actions"])):
                    #check if the action falls between the twothird and end of video: st >= twothirds
                    if json_data[vid]["actions"][i][1] >= twothirds:
                        atotal3 +=1
                        cl3 = json_data[vid]["actions"][i][0]
                        st3_ann = json_data[vid]["actions"][i][1] - twothirds #have to subtract the twothirds marker for updated st timestamp
                        et3_ann = json_data[vid]["actions"][i][2] - twothirds #have to subtract the twothirds marker for updated et timestamp
                        new_json_data[vid_id3]["actions"].append([cl3, round(st3_ann,3), round(et3_ann,3)])
                        #new_json_data[vid_id2]["actions"].append([cl2, st3_ann, et3_ann]) #without rounding off
                print(f"Total num actions for {vid} clip 3: {atotal3}")

    print(f"{VAR} done! ", end="")

    created_json = json.dumps(new_json_data) #creating an object of type json from the dictionary.
    with open(save_path + VAR + "annchor1000segmented.json", "w") as file:
        file.write(created_json)

    print("New segmented json written to file!")

            #clip from beginning to specified end-time:
            #command = "ffmpeg -ss 00:00:00 -accurate_seek -to "+ et +" -i "+vidkey+" -c:v libx264 -c:a aac "+save_dir+"/"+vidkey
            #os.system(command)

            #clip from specified st to specified et:
            # command = "ffmpeg -ss " + st + " -accurate_seek -to "+ et + " -i " + vidkey + " -c:v libx264 -c:a aac " + save_dir+"/"+vidkey
            # os.system(command)

            #clip from specified st to the end:
            # command = "ffmpeg -ss "+ st + " -accurate_seek -i " + vidkey +" -c:v libx264 -c:a aac " + save_dir+"/"+vidkey
            # os.system(command)


    
   
    # 2. If split in two find the halfway mark of the video in seconds
    # 3. Loop through each of the annotations and check if this halfway mark falls within an annotation
    # 4. If it doesn't, segment at the halfway mark
    # 5. If it does, check which annotation start or end is closest to the mark. Segment at that mark.

if __name__ == "__main__":
      for folder in os.listdir(videos_src_folder):
        segment_videos(folder)


#Overall logic:
# Get the sets' video durations from json file.

# If length <= 53 seconds:
# 	do nothing

# If length > 53 seconds and <= 106 seconds (53*2):
# 	Split the video into two parts _1 and _2 e.g. AUR0000_1.mp4 and AUR0000_2.mp4
# 	Put the correct annotations with the correct video

# If length > 106 but <= 159 (53*3)
# 	Split the video into three parts _1, _2 and _3

# Write a script to cut them so that they are max 53.3 ~ 53 seconds long (1280/24fps).

# Also be sure to cut around annotated parts.
