import os, sys
import subprocess
import audio_codecs


ignore = [
    ".git",
    "mgmt.py"
]

endpoint_folders = [
    "1080p",
    "Trailers",
    "Subs",
    "Extras"
]

global_state = {
    "removed_dots": [],
    "deleted_nfos": [],
    "moved_trailers": [],
    "no_trailers": [],
    "all_movs": [],
    "to_convert": [],
    "converted_trailers": [],
    "deleted_movs": [],
    "all_dts": [],
    "log": []
    }

def log(section: str, values: list):
    global global_state
    if section == "removed_dots":
        global_state["log"].append("dots removed from '"+values[0]+"'")
        global_state["removed_dots"].append(values[0])
    elif section == "deleted_nfos":
        global_state["log"].append("'"+values[0]+"' Deleted")
        global_state["deleted_nfos"].append(values[0])
    elif section == "move_trailers":
        line = "'"+values[0] + "' moved to '" + values[1]+"'"
        global_state["log"].append(line)
        global_state["moved_trailers"].append(values[1])
    elif section == "no_trailers":
        global_state["log"].append("'"+values[0] + "' lacks trailers")
        global_state["no_trailers"].append(values[0])
    elif section == "convertion_succeed":
        global_state["log"].append("'"+values[0] + "' converted to '" + values[1]+"'")
        global_state["converted_trailers"].append(values[1])
    elif section == "convertion_failed":
        global_state["log"].append("converting '" + values[0] + "' Failed")
    elif section == "mov_deleted":
        global_state["log"].append("'"+values[0] + "' deleted")
        global_state["deleted_movs"].append(values[0])
    elif section == "mov_printed":
        global_state["all_movs"].append(values[0])
    elif section == "dts_found":
        global_state["all_dts"].append(values[0])


def remove_dots(path: str):
    folders = path.split("\\")
    if "." in folders[-1]:
        folders[-1] = folders[-1].replace(".", " ")
        new_path = "\\".join(folders)
        os.rename(path, new_path)
        log("removed_dots", [new_path])
        return new_path
    else:
        return path


def delete_nfo(path: str):
    if os.path.isfile(path) and path[-4:] == ".nfo":
        os.remove(path)
        log("deleted_nfos", [path])


def move_trailers(file_path: str):
    if '-trailer.' in file_path:
        folders = file_path.split("\\")
        root_path = "\\".join(folders[:-1])
        file_name = folders[-1]
        trailer_path = root_path + "\\Trailers"
        final_file_path = trailer_path+"\\"+file_name
        if not "Trailers" in os.listdir(root_path):
            os.mkdir(trailer_path)
        else:
            if file_name in os.listdir(trailer_path):
                os.remove(file_path)
                log("move_trailers", [file_path, final_file_path])
                return True
        os.rename(file_path, final_file_path)
        log("move_trailers", [file_path, final_file_path])
        return True


def no_trailer(path: str):
    if path.split("\\")[-1] not in endpoint_folders:
        def check_further(path: str):
            no_trailer_files = True
            for file in os.listdir(path):
                if os.path.isfile and "-trailer" in file:
                    no_trailer_files = False
                    break
            if no_trailer_files:
                log("no_trailers", [path])
        if "Trailers" not in os.listdir(path):
            check_further(path)
        elif not os.listdir(path+"\\Trailers"):
            check_further(path)


def convert_trailers(dir_path: str, filename: str):
    if filename[-3:] != "mp4":
        try:
            format = ''
            if ".flv" in filename.lower():
                _format = ".flv"
            if ".mp4" in filename.lower():
                _format = ".mp4"
            if ".avi" in filename.lower():
                _format = ".avi"
            if ".mov" in filename.lower():
                _format = ".mov"
                
            input_file = os.path.join(dir_path, filename)
            output_file = os.path.join(dir_path, filename.replace(_format, ".mp4"))
            subprocess.call(['ffmpeg', '-i', input_file, output_file])
            log("convertion_succeed", [input_file, output_file])
        except:
            log("convertion_failed", [input_file])


def manage_movs(path:str, delete_mov: bool, print_mov: bool):
    if path[-3:] == "mov":
        if delete_mov:
            os.remove(path)
            log("mov_deleted", [path])
        else:
            log("mov_printed", [path])


def main_loop(root: str, flags: dict):
    if "remove_dots" in flags:
        root = remove_dots(root)
    dir_name = root.split("\\")[-1]
    dir_has_files = False
    for item_name in os.listdir(root):
        item_path = root + "\\" + item_name
        if os.path.isdir(item_path):
            if os.listdir(item_path):
                main_loop(item_path, flags)
            else:
                pass
            continue
        else:
            if item_name not in ignore:
                dir_has_files = True  
            if flags["delete_nfos"]:
                delete_nfo(item_path)

            # different functionality for different folder names
            if dir_name == "1080p":
                if flags["move_trailers"] and '-trailer.' in item_name:
                    os.remove(item_path)
                    continue
            elif dir_name == "Trailers":
                if flags["convert_trailers"]:
                    convert_trailers(root, item_name)
                if flags["delete_movs"] or flags["print_movs"]:
                    manage_movs(item_path, flags["delete_movs"], flags["print_movs"])
            else:
                if flags["move_trailers"]:
                    if move_trailers(item_path):
                        continue

            if flags["print_dts"]:
                if audio_codecs.is_dts(item_path):
                    log("dts_found", [item_path])

    if dir_has_files and flags["no_trailer"]:
        no_trailer(root)


def main():
    global global_state
    root_dir = None
    if len(sys.argv)>1:
        root_dir = sys.argv[1]
    else:
        root_dir = input(
        "Please type the path to your directory OR leave empty for current path:\n"
        )
        if root_dir == "" or root_dir is None:
            root_dir = os.getcwd()
            print("no path was entered. starting at "+root_dir)

    print(root_dir)

    flags = {
        "remove_dots": False,
        "delete_nfos": False,
        "move_trailers": False,
        "no_trailer": False,
        "convert_trailers": False,
        "delete_movs": False,
        "print_movs": False,
        "print_dts": False
    }

    inpt = input("""
    1) Remove dots
    2) Delete .nfo Files
    3) Move Trailers
    4) No Trailers
    5) Convert Trailers to .mp4
    6) Delete .mov Files
    7) Print .mov Files
    8) Print DTS Files

    """)
    print("\n")
    if "1" in inpt:
        flags["remove_dots"] = True
    if "2" in inpt:
        flags["delete_nfos"] = True
    if "3" in inpt:
        flags["move_trailers"] = True
    if "4" in inpt:
        flags["no_trailer"] = True
    if "5" in inpt:
        flags["convert_trailers"] = True
    if "6" in inpt:
        flags["delete_movs"] = True
    if "7" in inpt:
        flags["print_movs"] = True
    if "8" in inpt:
        flags["print_dts"] = True

    main_loop(root_dir, flags)

    if flags["print_movs"]:
        for item in global_state["all_movs"]:
            print(item)
        print("")
    if flags["no_trailer"]:
        for item in global_state["no_trailers"]:
            print(item)
        print("")
    if flags["print_dts"]:
        for item in global_state["all_dts"]:
            print(item)
        print("")

    print("\n\nFinished")

    print(global_state)

    input()


if __name__ == "__main__":
    main()