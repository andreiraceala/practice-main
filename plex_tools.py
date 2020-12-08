import plexapi
import os
import re
import subprocess,shlex
from tinytag import TinyTag
from plexapi.myplex import MyPlexAccount

account = MyPlexAccount('', '')
plex = account.resource('DESKTOP-1').connect()  # returns a PlexServer instance
movies = plex.library.section('Porn')
for video in movies.search():
    #print(video.title, video.locations)
    extension = "." + video.locations[0][-3:]
    final_name = re.sub('[^\w\-_\. ]', '', video.title) + extension
    final_path = os.path.dirname(video.locations[0])
    #print("Mutam aici: ", os.path.join(final_path, final_name))
    if extension == ".mp4" and video.contentRating == "XXX":
        print("Processing file {}".format(video.locations[0]))
        tag = TinyTag.get(video.locations[0])
        #print(video.title, tag.title)
        if str(tag.title).strip("\n") != str(video.title).strip("\n"):
            os.rename(video.locations[0], os.path.join(final_path, final_name))
            output_file = os.path.join(final_path, final_name)
            input_file =video.locations[0] + "_temp"
            os.rename(output_file, input_file)
            summary = re.sub(r'[^\w]', ' ', video.summary)
            print("Writing: Title:{} ,Content {}, Genres {} Output {} ".format(video.title, video.contentRating, video.genres, output_file))
            #print("Summary: {}".format(video.summary))
            cmd ='ffmpeg -hide_banner -nostats -loglevel 1 -i "{}" -codec copy -metadata title="{}" -metadata genre="{}" -metadata synopsis="{}" "{}"'.format(input_file, video.title, video.contentRating, summary, output_file )
            print(cmd)
            subprocess.check_output(shlex.split(cmd))
            if os.path.isfile(output_file):
                os.remove(input_file)
            else:
                continue
        else:
            continue

