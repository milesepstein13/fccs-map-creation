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
#dataplot = data.where(data != -9999.)
#dataplot.plot()
#plt.savefig('UStestfig.png')

cdata = xr.open_rasterio("data/nat_fbpfuels_2014b.tif")
percent = np.count_nonzero(cdata)/np.size(cdata)
#print(percent)
print(cdata)
print("RESAMPLING")
cdata = cdata.reindex(y = cdata.y[::2], x = cdata.x[::2], method = 'nearest')
print(cdata)
#print("Point:")
#print(cdata[0, 1000, 10001].data)
cdata[0, 6500:7000, 1000:1250].plot() # full size doesn't resolve, too big
plt.savefig("CAtestfig.png")








