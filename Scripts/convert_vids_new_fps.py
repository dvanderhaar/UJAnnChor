import os

source_dir = "./1-AnnChor1000/" # Replace with the source folder where the original videos can be found.
save_dir = "./1-AnnChor1000_with_subfolders_24fps/" # Replace with the folder to save the converted videos.
new_fps = 24 # Replace with the fps required

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
            #convert this video to 24fps and save it 
            #commend = "ffmpeg -i <input> -filter:v fps=30 <output>"
            command = "ffmpeg -i " + curr_src + "/" + file + " -filter:v fps="+new_fps+" " + curr_save + "/" + file # Specify the fps here
            os.system(command)
            print(f"{file} converted to {new_fps}fps")

def get_variations():
    return [folder for folder in os.listdir(source_dir)]


if __name__ == "__main__":
    for variation in get_variations():
        convertvids(variation)
    