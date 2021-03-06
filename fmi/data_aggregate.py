#
# Requires folder `data/raw` with data for single days
# and folder `data/months` where the monthly aggregates
# will be created to.
#

import json

# Days to aggregate to a month
month_lengths = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
cur_day = 0

# Places to remove for a reason or another (Timesteps wrong, completely missing times, etc.)
unfit_places = ["Enontekiö Kilpisjärvi Saana",
                "Espoo Tapiola",
                "Hailuoto Marjaniemi",
                "Halsua Purola",
                "Hanko Tulliniemi",
                "Helsinki Harmaja",
                "Helsinki Vuosaari Käärmeniementie",
                "Helsinki Vuosaari satama",
                "Hämeenlinna Lammi Evo",
                "Ilomantsi Mekrijärvi",
                "Inari Ivalo lentoasema",
                "Inari Saariselkä Kaunispää",
                "Inari Seitalaassa",
                "Jomala Jomalaby",
                "Jomala Maarianhamina lentoasema",
                "Jyväskylä lentoasema",
                "Jämsä Halli lentoasema",
                "Järvenpää Sorto",
                "Kajaani lentoasema",
                "Kankaanpää Niinisalo lentokenttä",
                "Kauhava lentokenttä",
                "Kaskinen Sälgrund",
                "Kemi I majakka",
                "Kemi Kemi-Tornio lentoasema",
                "Kauhajoki Kuja-Kokko",
                "Kittilä lentoasema",
                "Korsnäs Bredskäret",
                "Kotka Haapasaari",
                "Kouvola Utti lentoasema",
                "Kruunupyy Kokkola-Pietarsaari lentoasema",
                "Kumlinge kirkonkylä",
                "Kuopio Savilahti",
                "Kustavi Isokari",
                "Kuusamo lentoasema",
                "Kristiinankaupunki Majakka",
                "Lahti Sopenkorpi",
                "Lappeenranta Hiekkapakka",
                "Lappeenranta Konnunsuo",
                "Lappeenranta lentoasema",
                "Lappeenranta Lepola",
                "Lemland Nyhamn",
                "Liperi Joensuu lentoasema",
                "Liperi Tuiskavanluoto",
                "Lumparland Långnäs satama",
                "Maarianhamina Länsisatama",
                "Muonio Sammaltunturi",
                "Mustasaari Valassaaret",
                "Oulu lentoasema",
                "Parikkala Koitsanlahti",
                "Pello kirkonkylä",
                "Pirkkala Tampere-Pirkkala lentoasema",
                "Pori lentoasema",
                "Pori Tahkoluoto satama",
                "Porvoo Emäsalo",
                "Puolanka Paljakka",
                "Raasepori Jussarö",
                "Rauma Kylmäpihlaja",
                "Rautavaara Ylä-Luosta",
                "Rovaniemi rautatieasema",
                "Salo Kiikala lentokenttä",
                "Savonlinna lentoasema",
                "Sotkamo Kuolaniemi",
                "Siilinjärvi Kuopio lentoasema",
                "Sipoo Itätoukki",
                "Sodankylä Tähtelä",
                "Turku lentoasema",
                "Turku Rajakari",
                "Vaasa lentoasema",
                "Vantaa Helsinki-Vantaan lentoasema",
                "Vieremä Kaarakkala",
                "Ähtäri Inha"
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
    base = { f : { p : [] for p in places } for f in features }

    # For all days in month
    for i in range(cur_day, cur_day + ml):
        with open("./data/raw/data{}.json".format(i), encoding="utf8") as data_file:
            day = json.load(data_file)
            for f in features:
                for p in places:
                    base[f][p] += day[f][p][:-1] # Drop last value because it is the duplicate of the first value of the next day

    # Move timestamps into their own feature
    base["times"] = list(map(lambda x: x[0], base["t2m"]["Espoo Nuuksio"])) # Extract times
    for f in features:
        for p in places:
            # print(f, p, i)
            base[f][p] = list(map(lambda x: x[1], base[f][p]))

    # Write
    with open("./data/months/month{}.json".format(m), "w", encoding="utf8") as out_file:
        json.dump(base, out_file, ensure_ascii=False)

    # Move on to next
    cur_day += ml
    print(m)  # Display progression
    m += 1

