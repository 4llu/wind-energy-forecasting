import netCDF4 as nc

fn = 'data/ecmwf/output_1'
ds = nc.Dataset(fn)

print(ds)