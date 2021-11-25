import os
import subprocess

root_dir = input(
    "Please type the path to your directory OR leave empty for current path:"
    )
if root_dir is "":
    root_dir = os.getcwd()

ignore = [
    ".git"
]

def general(move_trailers, remove_nfo, print_mov, delete_mov):
    for current_dir_name in os.listdir(root_dir):
        current_dir_path = root_dir + '\\' + current_dir_name
        if os.path.isdir(current_dir_path) and current_dir_name not in ignore:
            print("\n" + current_dir_name + ":\n")
            #move
            if move_trailers or remove_nfo:
                if "1080p" in os.listdir(current_dir_path):
                    fhd_path = current_dir_path + '\\1080p'
                    for file in os.listdir(fhd_path):
                        if ('-trailer.' in file and move_trailers) or (file[-4:] == ".nfo" and remove_nfo):
                            os.remove(fhd_path + "\\" + file)
            trailer_path = current_dir_path + '\\Trailers'
            if move_trailers or print_mov or delete_mov:
                if 'Trailers' not in os.listdir(current_dir_path):
                    os.mkdir(trailer_path)
                if move_trailers:
                    for file in os.listdir(current_dir_path):
                        current_file_path = current_dir_path + '\\' + file
                        if not os.path.isdir(current_file_path):
                            if '-trailer.' in file:
                                if file not in os.listdir(trailer_path):
                                    print("\t"+current_file_path + '--->' + trailer_path + '\\' + file)
                                    os.rename(current_file_path, trailer_path + '\\' + file)
                                else:
                                    os.remove(current_file_path)
                                    print('\tDeleting ' + current_file_path)
                            elif file[-4:] == ".nfo":
                                os.remove(current_file_path)
                for trailerFile in os.listdir(trailer_path):
                    if ".mov" in trailerFile:
                        if print_mov:
                            print("\t"+trailer_path + '\\' + trailerFile)
                        if delete_mov:
                            if len(os.listdir(trailer_path)) > 1:
                                os.remove(trailer_path + '\\' + trailerFile)
                            else:
                                print("\t"+"No other trailer in "+current_dir_name)


def no_trailer():
    have_trailers = []
    no_trailers = []
    for movie_folder in os.listdir(root_dir):
        cur_folder = root_dir+"\\"+movie_folder
        if os.path.isdir(cur_folder):
            if "Trailers" not in os.listdir(cur_folder):
                no_trailers.append(movie_folder)
            else:
                files = cur_folder+"\\Trailers"
                if not os.listdir(files):
                    no_trailers.append(movie_folder)
                else:
                    have_trailers.append(movie_folder)

    print("Have trailers: "+str(len(have_trailers))+"\n\t"+"\n\t".join(have_trailers))
    print("\n\n")
    print("lacking trailers: "+str(len(no_trailers))+"\n\t"+"\n\t".join(no_trailers))


def remove_dots():
    for movie_folder in os.listdir(root_dir):
        cur_folder = root_dir+"\\"+movie_folder
        if os.path.isdir(cur_folder):
            os.rename(cur_folder, root_dir+"\\"+movie_folder.replace(".", " "))


def convert_trailers():
    for movie_folder in os.listdir(root_dir):
        cur_folder = root_dir+"\\"+movie_folder
        if os.path.isdir(cur_folder):
            if "Trailers" in os.listdir(cur_folder) and os.path.isdir(cur_folder+"\\Trailers"):

                src = cur_folder+"\\Trailers"
                dst = cur_folder+"\\Trailers"

                for root, dirs, filenames in os.walk(src, topdown=False):
                    print(filenames)
                    for filename in filenames:
                        if filename[:-3]+"mp4" not in filenames:
                            print('[INFO] 1', filename)
                            try:
                                _format = ''
                                if ".flv" in filename.lower():
                                    _format = ".flv"
                                if ".mp4" in filename.lower():
                                    _format = ".mp4"
                                if ".avi" in filename.lower():
                                    _format = ".avi"
                                if ".mov" in filename.lower():
                                    _format = ".mov"

                                input_file = os.path.join(root, filename)
                                print('[INFO] 1', input_file)
                                output_file = os.path.join(dst, filename.replace(_format, ".mp4"))
                                subprocess.call(['ffmpeg', '-i', input_file, output_file])
                            except:
                                print("A conversion exception occurred")


move_trailers = remove_nfo = print_mov = delete_mov = False

inpt = input("""
1) Move Trailers
2) Remove .nfo
3) Print .mov
4) Delete .mov
5) Convert Trailers to .mp4
6) No Trailers
7) Remove dots
""")
print("\n")
if "1" in inpt:
    move_trailers = True
if "2" in inpt:
    remove_nfo = True
if "3" in inpt:
    print_mov = True
if "4" in inpt:
    delete_mov = True

if move_trailers or remove_nfo or print_mov or delete_mov:
    general(move_trailers, remove_nfo, print_mov, delete_mov)

if "5" in inpt:
    convert_trailers()

if "7" in inpt:
    remove_dots()

if "6" in inpt:
    no_trailer()

print("\n\nFinished")
input()