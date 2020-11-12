#
# Requires folder `data/months` with monthly data aggregates.
# Select wich features to include `important_f` and for those
# remove places with consistently missing data, and extrapolate short
# patches of missing data.
#

import json
import math

important_f = ["ws_10min"]

# For all months
for m in range(1, 13):
    # Load data
    clean_data = {f : {} for f in important_f}
    with open("./data/months/month{}.json".format(m), encoding="utf8") as in_file:
        data = json.load(in_file)

        # Extract selected features
        for f in important_f + ["times"]: # Include timestamps
            clean_data[f] = data[f]

    # Detect places missing values in important features
    remove_p = []
    for f in important_f:
        for p in clean_data[f].keys():
            if math.isnan(clean_data[f][p][0]):
                remove_p.append(p)

    # Remove those places from all features
    for f in important_f:
        for p in remove_p:
            clean_data[f].pop(p, None)
    
    # Find the longest ts and buff all to that length (copy last value)
    # This is dirty as fuck, but the worst places have already been removed and the rest only vary by max 5 places
    shortest = 10000
    for f in important_f:
        for p in clean_data[f].keys():
            if len(clean_data[f][p]) < shortest:
                shortest = len(clean_data[f][p])
    for f in important_f:
        for p in clean_data[f].keys():
            clean_data[f][p] = clean_data[f][p][:shortest]
    clean_data["times"] = clean_data["times"][:shortest]

    # Add missing values
    for f in important_f:
        for p in clean_data[f].keys():
            ts = clean_data[f][p]
            for i in range(len(ts)):
                # Missing value
                if math.isnan(ts[i]):
                    # Replace with average of previous value and next non-nan value
                    j = i + 1
                    while j < len(ts):
                        if not math.isnan(ts[j]):
                            ts[i] = round((ts[i - 1] + ts[j]) / 2, 1)
                            break
                        else:
                            j += 1
                        # In case of no non-nan values before end of ts, copy value from previous timestep
                        if not j < len(ts):
                            ts[i] = ts[i - 1]

    # Write data
    with open("./data/ws_unnormalized/month{}.json".format(m), "w", encoding="utf8") as out_file:
        json.dump(clean_data, out_file, ensure_ascii=False)

    print(m)


