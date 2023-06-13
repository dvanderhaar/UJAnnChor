import os

source_dir = "./1-AnnChor1000/"
save_dir = "./1-AnnChor1000_25fps/"

def convertvids(folder):

    VAR = folder
    curr_src = source_dir + VAR
    curr_save = save_dir + VAR

    if not os.path.exists(curr_save):
        os.makedirs(curr_save)
        print("Save Directory created")
    else:
        print("Save directory already exists")

    for file in os.listdir(curr_src):
        if file.endswith('.mp4'):
            print(file)
            #convert this video to 25fps and save it 
            #commend = "ffmpeg -i <input> -filter:v fps=30 <output>"
            command = "ffmpeg -i " + curr_src + "/" + file + " -filter:v fps=25 " + curr_save + "/" + file
            os.system(command)
            print(f"{file} converted to 25fps")

def get_variations():
    #return [folder for folder in os.listdir(source_dir)]
    return ['SWA', 'TCF', 'TCM', 'TMF', 'TMM', 'WAL'] # remaining items

if __name__ == "__main__":
    print(get_variations())
    for variation in get_variations():
        convertvids(variation)
    