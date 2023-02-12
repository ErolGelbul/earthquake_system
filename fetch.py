import requests
import time

from bs4 import BeautifulSoup
import simpleaudio as sa
from distancefinder import haversine

from termcolor import colored

s_mainalarm = sa.WaveObject.from_wave_file("alarm.wav")
s_woopwoop = sa.WaveObject.from_wave_file("woopwoop.wav")
s_daa = sa.WaveObject.from_wave_file("daa.wav")
s_weewoo = sa.WaveObject.from_wave_file("weewoo.wav")

# setup dummy values

_onetab = "----------"
_is_Turkey = False
mv_list = [10, 10, 10]
distance = -1
d_list = [0, 0, 0]

while True:
    # fetch the data

    url = "http://www.koeri.boun.edu.tr/scripts/lst4.asp"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    pre_tag = soup.find("pre")

    # parse the data

    lines = pre_tag.text.strip().split("\n")
    mv = lines[6]
    place = lines[6]

    # grab the MV

    mv = mv[mv.index("-") + 4:]
    mv = mv[:4]
    mv = float(mv)
    print("Earthquake was: ", end="")
    print(colored(mv, "red", attrs=["bold"]))

    # grab the name and check if it is in Turkey

    if ")" in place:
        place = place[:place.index(")")]
        place = place[place.index("(") + 1:]
        print(f"Last earthquake location: {place}")
        _is_Turkey = True
    else:
        print("Not in Turkey")
        _is_Turkey = False

    # check if new earthquake is detected

    if mv not in mv_list:
        print(colored("New earthquake detected!", "blue", attrs=["bold"]))
        play_obj = s_woopwoop.play()
        play_obj.wait_done()
        mv_list.append(mv)
        # find the distance between the earthquake and me
        if _is_Turkey:
            distance = haversine(place)

    # get rid of the oldest MV if its filled
    if len(mv_list) > 4:
        mv_list.pop(0)

    # if mv increased alert me

    if mv_list[-1] > mv_list[-2]:
        diff = mv_list[-1] - mv_list[-2]
        print("MV increased by:", end=" ")
        print(colored("{:.1f}".format(diff), "yellow", attrs=["bold"]))
        play_obj = s_daa.play()
        play_obj.wait_done()
        mv_list[-1], mv_list[-2] = mv_list[-2], mv_list[-1]

    # print the distance

    print("Distance from me: ", end="")
    if distance > 100:
        print(colored("{:.1f}".format(distance),
                      "green", attrs=["bold"]), end="")
        print(" km")
    else:
        print(colored("{:.1f}".format(distance),
                      "red", attrs=["bold"]), end="")
        print(" km")

    # play alarm if earthquake is major

    if mv > 5 and _is_Turkey and distance < 100:
        print(colored("Major earthquake, we are in danger!", "red"))
        play_obj = s_weewoo.play()
        play_obj.wait_done()
    else:
        print(colored("No major earthquake, we are chilling.", "green"))

    if int(mv) > 0:
        print(colored((_onetab * int(mv)), "cyan", attrs=["bold"]))

    time.sleep(1)
