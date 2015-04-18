__author__ = 'TwelveNights'

import json
import requests
import time
import ast

data = ""
interval = 1428613200
time_pull = 12

# Riot API Key
key = open("key.txt").read()

try:
    f = open('data.json')
    data = json.loads(f.read())
    f.close()

except FileNotFoundError:
    print("File is not there, it will be made after the first run.")

except ValueError:
    f.close()

if data != "":
    ward_spots = data["data"]
    match_count = data["match_count"]
else:
    ward_spots = []
    match_count = 0

for a in range(time_pull):
    interval += 60*5*a
    url = "https://na.api.pvp.net/api/lol/na/v4.1/game/ids?beginDate={0}&api_key={1}".format(interval, key)
    response = requests.get(url)
    match_list = ast.literal_eval(response.text)

    for match in match_list:
        print(match)
        match_url = "https://na.api.pvp.net/api/lol/na/v2.2/match/{0}?includeTimeline=true&api_key={1}".format(match, key)
        match_response = requests.get(match_url)
        if match_response.status_code == 200:
            json_object = match_response.json()
            frames = json_object["timeline"]["frames"]
            match_count += 1

            for frame in range(len(frames)):
                if frames[frame]["timestamp"] == 0:
                    pass
                else:
                    for event in frames[frame]["events"]:
                        if event["eventType"] == "WARD_PLACED" and event["wardType"] != "TEEMO_MUSHROOM" and event["wardType"] != "UNDEFINED":
                            if frame * 60000 - 1000 <= event["timestamp"] <= frame * 60000 + 1000:
                                creatorId = event["creatorId"]
                                timestamp = event["timestamp"]
                                wardType = event["wardType"]
                                x = frames[frame]["participantFrames"]["{}".format(creatorId)]["position"]["x"]
                                y = frames[frame]["participantFrames"]["{}".format(creatorId)]["position"]["y"]

                                team = json_object["participants"][creatorId - 1]["teamId"]
                                info = {"team": team, "type": wardType, "position": {"x": x, "y": y}, "time": timestamp}
                                ward_spots.append(info)
        else:
            time.sleep(300)
            break
        time.sleep(1)


with open('data.json', 'w') as outfile:
    data = {"match_count": match_count,
            "data": ward_spots}
    json.dump(data, outfile)
