#
# Mean center each feature and divide it by the variance for normalization
#

import json
import numpy as np

in_folder = "./data/ws_unnormalized"
out_folder = "./data/ws_normalized"

# Reference for features and places
ref = None
with open("{}/month1.json".format(in_folder), encoding="utf8") as data_file:
    ref = json.load(data_file)
features = list(filter(lambda x: x != "times", ref.keys()))
places = list(ref["ws_10min"].keys())

# Aggregate months into year
year = { f : { p : [] for p in places } for f in features }
year["times"] = []
for m in range(1, 13):
    print(m)
    with open("{}/month{}.json".format(in_folder, m), encoding="utf8") as in_file:
        data = json.load(in_file)
        year["times"] += data["times"]
        for f in features:
            for p in places:
                year[f][p] = data[f][p]

# Normalize
for f in features:
    for p in places:
        year[f][p] = np.array(year[f][p])
        year[f][p] = (year[f][p] - np.mean(year[f][p])) / np.var(year[f][p])
        year[f][p] = year[f][p].tolist()

# Write data
with open("{}/year.json".format(out_folder), "w", encoding="utf8") as out_file:
    json.dump(year, out_file, ensure_ascii=False)

# data = None
# with open("./data/ws_unnormalized/month1.json", encoding="utf8") as in_file:
#     data = json.load(in_file)

# print(len(data["ws_10min"]["Asikkala Pulkkilanharju"]))
# print(len(data["times"]))
# for p in data["ws_10min"].keys():
#     print(p, len(data["ws_10min"][p]))