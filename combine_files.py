
import ffmpeg
import os
import glob
import subprocess,shlex
import pathlib

def get_files():
    cwd = os.getcwdb().decode("UTF-8")
    print (cwd)
    files = glob.glob(os.path.join(cwd,"*.mp4"))
    print (files)
    input_file=open("mylist.txt","w+")
    for file in files:
        input_file.write("file '{}'\n".format(os.path.normpath(file)))
    input_file.flush
    input_file.close

def encode():
    folder=str(os.getcwdb().decode("UTF-8"))
    print("Folder=", str(folder) )
    name = os.path.join(str(folder), str(os.path.basename(folder)).replace(" ","_")) + ".mp4"
    print (name)
    cmd = "ffmpeg -f concat -safe 0 -i mylist.txt -metadata title='{}' -c copy '{}'".format(name,name)
    out = subprocess.check_output(shlex.split(cmd))
    print (out)




get_files()
encode()