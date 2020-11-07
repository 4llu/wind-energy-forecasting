#
# Requires folder `data/raw` with data for single days
# and folder `data/months` where the monthly aggregates
# will be created to.
#

import json

# Days to aggregate to a month
month_lengths = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
cur_day = 0

# Places to remove for a reason or another (Mostly timesteps wrong)
unfit_places = ["Helsinki Vuosaari Käärmeniementie",
                "Helsinki Vuosaari satama",
                "Inari Ivalo lentoasema",
                "Jyväskylä lentoasema",
                "Järvenpää Sorto",
                "Kajaani lentoasema",
                "Kemi I majakka",
                "Kemi Kemi-Tornio lentoasema",
                "Kittilä lentoasema",
                "Korsnäs Bredskäret",
                "Kouvola Utti lentoasema",
                "Kruunupyy Kokkola-Pietarsaari lentoasema",
                "Kuopio Savilahti",
                "Kuusamo lentoasema",
                "Lahti Sopenkorpi",
                "Lappeenranta Hiekkapakka",
                "Lumparland Långnäs satama",
                "Maarianhamina Länsisatama",
                "Oulu lentoasema",
                "Pori lentoasema",
                "Sipoo Itätoukki",
                "Sodankylä Tähtelä",
                "Turku lentoasema",
                "Vaasa lentoasema",
                ]

# Reference for features and places
ref = None
with open("./data/raw/data0.json", encoding="utf8") as data_file:
    ref = json.load(data_file)
features = ref.keys()  # ['t2m', 'ws_10min', 'wd_10min', 'rh', 'p_sea']
places = list(filter(lambda x: x not in unfit_places, ref["t2m"].keys())) # With unfit places removed

# Aggregate months
m = 1
for ml in month_lengths:
    first = None

    # For all days in month
    for i in range(cur_day, cur_day + ml):
        day = None
        with open("./data/raw/data{}.json".format(i), encoding="utf8") as data_file:
            day = json.load(data_file)

        # Use first day as base    
        if i == cur_day:
            first = day
            # Remove unfit places
            for f in features:
                for p in unfit_places:
                    first[f].pop(p, None)
        # Add others
        else:
            for f in features:
                for p in places:
                    first[f][p] += day[f][p]

    # Move timestamps into their own feature
    first["times"] = list(map(lambda x: x[0], first["t2m"][list(first["t2m"].keys())[0]])) # Extract times
    for f in features:
        for p in places:
            # print(f, p, i)
            first[f][p] = list(map(lambda x: x[1], first[f][p][:-1])) # Drop last value because it is the duplicate of the first value of the next day

    # Write
    with open("./data/months/month{}.json".format(m), "w", encoding="utf8") as out_file:
        json.dump(first, out_file, ensure_ascii=False)

    # Move on to next
    cur_day += ml
    print(m)  # Display progression
    m += 1

