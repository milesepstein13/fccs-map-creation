from cmath import nan
from netCDF4 import Dataset
import matplotlib.pyplot as plt
import numpy as np
import xarray as xr
import pandas as pd
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import scipy
import rasterio
from affine import Affine
import pyproj
import proj
import rioxarray as rxr

# determined manually with https://www.fs.usda.gov/pnw/tools/fuel-and-fire-tools-fft
# based on canadian fuel types: https://cwfis.cfs.nrcan.gc.ca/background/fueltypes/c1
# 
ca_to_us_fuelbeds = {
    # key values from metadata of Canadian fuel data
    0: 0, # Out of domain
    101: 85, # C1 - Spruce–Lichen Woodland -> 85 - black spruce/lichen forest
    102: 87, # C2 - Boreal Spruce -> 87 - Black spruce/feathermoss forest
    103: 22, # C3 - Mature Jack or Lodgepole Pine -> 22 - Mature lodgepole pine forest (146 for jack, but lodgepole is more common than jack in Western Canada)
    104: 21, # C4 - Immagture Jack or Lodgepole Pine -> 21 - Young lodgepole pine forest (148 for jack, but lodgepole is more common than jack in Western Canada)
    105: 138, # C5 - Red and White Pine -> 138 - Red pine-eastern white pine forest
    106: 24, # C6 - Conifer Plantation -> 24 - Pacific ponderosa pine-Douglas-fir forest (could be many things, chose this because it seems representative) TODO
    107: 67, # C7 - Ponderosa Pine-Douglas-Fir -> 67 - Interior ponderosa pine-Douglas-fir forest
    108: 224, # D1 - Leafless Aspen -> 224 - Quaking aspen forest
    109: 143, # M1 - Boreal Mixedwood-Leafless -> 143 -  Quaking aspen-paper birch-white spruce-balsam fir forest
    110: 143, # M2 - Boreal Mixedwood-Green -> 143 -  Quaking aspen-paper birch-white spruce-balsam fir forest
    111: 143, # M3 - Dead Balsam Fir Mixedwood-Leafless -> 143 -  Quaking aspen-paper birch-white spruce-balsam fir forest
    112: 143, # M4 - Dead Balsam Fir Mixedwood-Leafless -> 143 -  Quaking aspen-paper birch-white spruce-balsam fir forest
    113: 134, # S1 - Jack or Lodgepole Pine Slash -> 134 - White oak-northern red oak-hickory forest (chosen because it's the only fccs fuelbed with recent slash) TODO
    114: 134, # S2 - White Spruce-Balsam Slash -> 134 - White oak-northern red oak-hickory forest (chosen because it's the only fccs fuelbed with recent slash) TODO
    115: 134, # S3 - Coastal Cedar-Hemlock-Douglas-Fir Slash -> 134 - White oak-northern red oak-hickory forest (chosen because it's the only fccs fuelbed with recent slash) TODO
    116: 66, # O1a - Grass (spring) -> 66 - Bluebunch wheatgrass-bluegrass grassland (could be many things, chose this because it seems representative) TODO
    117: 66, # O2a - Grass (summer/fall) -> 66 - Bluebunch wheatgrass-bluegrass grassland (could be many things, chose this because it seems representative) TODO
    118: 0, # Water -> 0 - No fuel
    119: 0, # Non-fuel -> 0 - No fuel
    120: 0, # Wetland -> 0 - No fuel
    121: 0, # Urban area -> 0 - No fuel
    122: 0 # Vegetated non-fuel -> 0 - No fuel
}

def fuelbed_convert(canadian_fuelbed, x, y):
    #converts FBP fuel type to FCCS fueltype 
    if ((x % 100 == 0) & (y == 0)):
        print(x, y)
    return ca_to_us_fuelbeds[canadian_fuelbed]

# import Canadian fuel data
canadian_file_path = "data/nat_fbpfuels_2014b.tif"
cdata = xr.open_rasterio(canadian_file_path)
print("CANADA: ")

# plot piece of initial data for comparision
print("Plotting initial")
cdata[0, 13000:14000, 2000:2500].plot() # full size doesn't resolve, too big
plt.savefig("CApre.png")

# convert FBP fuel types to FCCS
for x in range(cdata.x.size):
    for y in range(cdata.y.size):
        data = cdata.data
        data[0, y, x] = fuelbed_convert(data[0, y, x], x, y)
        cdata.data = data
# smaller range for testing:
# print("Converting fuelbeds")
#or x in range(13000, 14000):
#    for y in range(2000, 2500):
#        cdata.data[0, x, y] = fuelbed_convert(cdata.data[0, x, y], x, y)
print("plotting final")
plt.clf()
cdata[0, 13000:14000, 2000:2500].plot() # full size doesn't resolve, too big
plt.savefig("CApost.png")
cdata.to_netcdf("data/fccs_canada.nc")


# import American fuel data
# american_file_path = "data/fccs_fuelload.nc"
# adata = xr.open_dataset(american_file_path)
# print("AMERICA: ", adata)

#import Alaskan fuel data
#alaskan_file_path = "data/FCCS_Alaska.nc"
#akdata = xr.open_dataset(alaskan_file_path)
#print("ALASKA: ", akdata)
#print(akdata.attrs)
#akdata.Band1.plot()
#plt.savefig('AKtestfig.png')