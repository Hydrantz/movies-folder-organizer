import subprocess

PROBLEMATIC = ["dts", 'truehd']

def get_codecs(path: str):
    command = ['ffprobe', '-v', '0', '-select_streams', 'a', '-show_entries', 'stream', path]
    metadata = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out, err = metadata.communicate()
    fin = [adv.split("ncodec_name=")[1].split("\\")[0] for adv in str(out).split('nindex=')[1:]]
    return fin

def is_dts(path: str):
    ans = False
    list = get_codecs(path)
    for prb in PROBLEMATIC:
        if prb in list:
            ans = True
            break
    return ans