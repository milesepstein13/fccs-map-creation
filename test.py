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

nc = Dataset('data/fccs_fuelload.nc')
#print("netCDF4: ")
#print(nc)
data = xr.open_dataset("data/fccs_fuelload.nc")
print("XARRAY: ")
print(data)
print(data.FCCS_FuelLoading)
dataplot = data.FCCS_FuelLoading.where(data.FCCS_FuelLoading != -9999.)
#dataplot.plot()
#plt.savefig('UStestfig.png')

cdata = xr.open_rasterio("data/nat_fbpfuels_2014b.tif")
percent = np.count_nonzero(cdata)/np.size(cdata)
#print(percent)
print(cdata)
#print("Point:")
#print(cdata[0, 1000, 10001].data)
#cdata[0, 13000:14000, 2000:2500].plot() # full size doesn't resolve, too big
#plt.savefig("CAtestfig.png")








