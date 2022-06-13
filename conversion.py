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

def fuelbed_convert(canadian_fuelbed, x, y):
    if ((x % 100 == 0) & (y % 100 == 0)):
        print(x, y)
    return canadian_fuelbed + 50

# import Canadian fuel data
canadian_file_path = "data/nat_fbpfuels_2014b.tif"
cdata = xr.open_rasterio(canadian_file_path)
print("CANADA: ", cdata)
cdata[0, 13000:14000, 2000:2500].plot() # full size doesn't resolve, too big
plt.savefig("CApre.png")
#for x in range(cdata.x.size):
#    for y in range(cdata.y.size):
#        cdata.data[0, x, y] = fuelbed_convert(cdata.data[0, x, y], x, y)
# smaller range for testing:
for x in range(13000, 14000):
    for y in range(2000, 2500):
        cdata.data[0, x, y] = fuelbed_convert(cdata.data[0, x, y], x, y)
plt.clf()
cdata[0, 13000:14000, 2000:2500].plot() # full size doesn't resolve, too big
plt.savefig("CApost.png")


# import American fuel data
american_file_path = "data/fccs_fuelload.nc"
adata = xr.open_dataset(american_file_path)
print("AMERICA: ", adata)

#import Alaskan fuel data
alaskan_file_path = "data/FCCS_Alaska.nc"
akdata = xr.open_dataset(alaskan_file_path)
print("ALASKA: ", akdata)
print(akdata.attrs)
akdata.Band1.plot()
plt.savefig('AKtestfig.png')