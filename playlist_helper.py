#!/usr/bin/python

# Reid's Spotify Playlist Helper!
# The purpose of this program is to help you organise your Spotify playlists by
# allowing you to set a time of day that you want to start your playlist, and
# using that data to tell you at what time each song will start and finish
# it will also take into account the length of your crossfade
# I haven't decided on a license yet, so this code is copyright Reid Wicks
# until I can decide on an appropriate license.

import json
import spotipy
import spotipy.util as util
import time

#Assigning variables.
MS = 1000
CROSSFADE_LENGTH = 7    # Consider re-writing the program so that CROSSFADE_LENGTH
START_TIME = 61200      #and START_TIME are defined outside of the program
START_TIME_FORM = time.strftime('%H:%M:%S', time.gmtime(START_TIME))
current_time = START_TIME
current_time_form = time.strftime('%H:%M:%S', time.gmtime(current_time))
playlist_tracks = []
track_total = 0         # Not strictly necessary, but useful for assignining positions to each track.

with open("user_data.txt", "r") as user_data:
    username = user_data.readline().rstrip()        # The user's username should be the first line of the user_data file
    playlist_id = user_data.readline().rstrip()     # Playlist ID is the second line in the user_data file
    scope = user_data.readline().rstrip()           # Scopes are the third line of the file
with open("app_data.txt", "r") as app_data:
    client_id = app_data.readline().rstrip()        # Client ID is the first line of the app_data file
    client_secret = app_data.readline().rstrip()    # Client secret is the second line of the app_data file
    redirect_uri = app_data.readline().rstrip()     # Don't know what to do with this, tbh. But it's in there. It's the third line of the app_data file

token = util.prompt_for_user_token(username,scope,client_id,client_secret,redirect_uri)
sp = spotipy.Spotify(auth=token)

part1 = sp.user_playlist_tracks(username,
                                playlist_id,
                                fields='items(track(name,duration_ms,uri))',
                                limit=100,
                                offset=0,
                                market=None,
                                )
part2 = sp.user_playlist_tracks(username,
                                playlist_id,
                                fields='items(track(name,duration_ms,uri))',
                                limit=100,
                                offset=100,
                                market=None,
                                )

for x in part1:
    for y in part1[x]:
        for z in y:
            name = y[z]['name']
            duration_ms = y[z]['duration_ms']
            song_uri = y[z]['uri']
            length = time.strftime('%M:%S', time.gmtime(duration_ms/MS))
            position = track_total
            playlist_tracks.append({'name': name,
                                    'duration_ms': duration_ms,
                                    'uri': song_uri,
                                    'length': length,
                                    'position': position,
                                    })
            track_total += 1
for x in part2:
    for y in part2[x]:
        for z in y:
            name = y[z]['name']
            duration_ms = y[z]['duration_ms']
            song_uri = y[z]['uri']
            length = time.strftime('%M:%S', time.gmtime(duration_ms/MS))
            position = track_total
            playlist_tracks.append({'name': name,
                                    'duration_ms': duration_ms,
                                    'uri': song_uri,
                                    'length': length,
                                    'position': position,
                                    })
            track_total += 1
def print_tracks():
    global current_time_form  # Yeah, yeah, I know. "Don't use global variables".
    global current_time       # I'm using them here to avoid constantly passing variables
    for item in playlist_tracks:
        print("Song pos:    {}".format(item['position']))
        print("Name:        {}".format(item['name']))
        #print("Length:      {}".format(item['length']))
        print("Song starts: {}".format(current_time_form))
        end_time = current_time + (item['duration_ms']/MS)
        end_time_form = time.strftime('%H:%M:%S', time.gmtime(end_time))
        print("Song ends:   {}".format(end_time_form))
        current_time += (item['duration_ms']/MS) - CROSSFADE_LENGTH
        current_time_form = time.strftime('%H:%M:%S', time.gmtime(current_time))
    print("Playlist ends:   {}".format(current_time_form))
    print("Total tracks:    {}".format(track_total))

def move_track():
    #Use this guide: https://beta.developer.spotify.com/console/put-playlist-tracks/
    track_to_move = input("Type the name of the track you want to move: ")
    new_location = int(input("Please enter the position you wish to move the track to: "))
    for item in playlist_tracks:
        if item['name'] == track_to_move:
            sp.user_playlist_reorder_tracks(username, playlist_id, item['position'], new_location)
    print("Moving track {} to position {}".format(track_to_move, new_location))
def find_uri():
    track_pos = int(input("Please enter the position of the track you want the URI for: "))
    for item in playlist_tracks:
        if item['position'] == track_pos:
            track_uri = item['uri']
            break
    print(track_uri)

print_tracks()
move_track()
