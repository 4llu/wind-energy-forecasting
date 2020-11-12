#!/usr/bin/env python

# Download data from https://apps.ecmwf.int/datasets/data/interim-full-daily/levtype=sfc
from ecmwfapi import ECMWFDataServer
server = ECMWFDataServer()

server.retrieve({
    "class": "ei",
    "dataset": "interim",
    "date": "2018-01-01/to/2018-01-31",
    "expver": "1",
    "grid": "0.33/0.33",
    "area": "70/19/59/31",
    "levtype": "sfc",
    "param": "134.128/165.128/166.128/167.128",
    "step": "0",
    "stream": "oper",
    "time": "00:00:00/06:00:00/12:00:00/18:00:00",
    "type": "an",
    "format": "netcdf",
    "target": "data/ecmwf/output_1",
})