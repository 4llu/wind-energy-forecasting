import pandas as pd
import numpy as np
import netCDF4 as nc

# Definitions
#############

# Regions (17)
regions = [
    [19.0, 21.2, 60.6, 59.5], # Ahvenanmaa
    [21.2, 23.5, 61.0, 59.5], # Varsinais-Suomi
    [23.5, 26.2, 60.7, 59.5], # Uusimaa
    [26.2, 27.2, 61.3, 59.0], # Kymenlaakso
    [27.2, 30.0, 61.7, 59.0], # Etelä-Karjala
    [20.0, 22.7, 61.3, 60.0], # Satakunta
    [23.5, 25.0, 61.2, 60.7], # Kanta-Häme
    [25.0, 26.2, 61.6, 60.7], # Päijät-Häme
    [22.7, 25.0, 62.4, 61.0], # Pirkanmaa
    [26.2, 29.0, 62.4, 61.3], # Etelä-Savo
    [24.5, 26.5, 63.5, 61.6], # Keskisuomi
    [20.0, 24.5, 64.0, 61.0], # Etelä + Keski + Pohjanmaa
    [28.4, 32.0, 63.9, 61.7], # Pohjois-Karjala
    [26.5, 28.4, 64.0, 62.4], # Pohjois-Savo
    [27.2, 30.5, 65.3, 63.9], # Kainuu
    [23.4, 30.0, 66.0, 63.5], # Pohjois-Pohjanmaa
    [22.7, 30.5, 69.5, 66.0]  # Lappi
]

# Time series info
year = 2018
timestep = 6 # in hours
obs_per_day = int(24 / timestep) # 4


# Helpers
#########

def region_map(latitudes, longitudes, regions):
    re_map = np.zeros((len(latitudes), len(longitudes))) - 1

    for y, la in enumerate(latitudes):
        for x, lo in enumerate(longitudes):
            for i, r in enumerate(regions):
                # print(la, lo)
                if lo > r[0] and lo < r[1] and la < r[2] and la > r[3]:         
                    re_map[y, x] = i
                    break
            
    
    return re_map.astype(int)

def region_means(data, region_map, region_num):
    regions = [[] for i in range(region_num)]

    for y in range(len(region_map)):
        for x in range(len(region_map[0])):
            region = region_map[y][x]
            if region != -1:
                regions[region].append(data[y][x])

    means = []
    for r in regions:
        means.append(np.mean(np.abs(np.array(r))).tolist())
    return means

# Data selection
################

# Possible features: u10, v10, sp, t2m
features = ["u10", "v10"]
total_feature_num = len(features) * len(regions) # When using region means

# Possible months: 1-12
months = np.array([1, 2, 3, 4, 5, 6])
#months = np.array([1])
month_lengths = np.array([31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31])

# Data frame definitions
timesteps_months = month_lengths * obs_per_day # Timesteps for each month
timesteps = np.sum(month_lengths[months - 1]) * obs_per_day # Total number of timesteps to be included
datetimes = pd.date_range("{}-01-01".format(year), periods=timesteps, freq="{}H".format(timestep))
columns = []
for f in features + ["w10"]:
    for i in range(len(regions)):
        columns.append("{}_{}".format(f, i))

# Get data
##########

df_data = []
re_map = []
for m in months:
    print(m) # Progress tracker
    fn = 'data/ecmwf/output_{}'.format(m)
    ds = nc.Dataset(fn)
    # ds = nc.Dataset("./data/ecmfw/output_{}.nc4".format(m))

    # Compute region map
    if len(re_map) == 0:
        re_map = region_map(ds["latitude"][:], ds["longitude"][:], regions)

    # Create feature w10
    w10 = [0 for t in range(timesteps_months[m - 1])]
    for t in range(timesteps_months[m - 1]):
        w10[t] = np.sqrt(ds["u10"][t]**2 + ds["v10"][t]**2)

    # Calculate timestep values (In this case regional means)
    for t in range(timesteps_months[m - 1]):
        row = []
        for f in features:
            row += region_means(ds[f][t], re_map, len(regions))
        # And w10
        row += region_means(w10[t], re_map, len(regions))
        df_data.append(row)

# Output
########

# Create data frame
df = pd.DataFrame(np.array(df_data), columns=columns)
# Add datetimes as column because feather format only supports default indexing
df["datetime"] = datetimes

# For checking
print(df.tail(5))

# Write
df.to_feather('./data/predictors/wind_region_mean_2018-01to06.feather')