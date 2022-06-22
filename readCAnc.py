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

data = xr.open_dataset("data/fccs_canada.nc")
print("FROM NC:")
print(data)
data.Band1.plot()
plt.savefig('CAnc.png')
#print("FROM TIF")
#canadian_file_path = "data/nat_fbpfuels_2014b.tif"
#cdata = xr.open_rasterio(canadian_file_path)
#print(cdata)

# import American fuel data
american_file_path = "data/fccs_fuelload.nc"
adata = xr.open_dataset(american_file_path)
print("AMERICA: ", adata)
#print(adata.lambert_conformal_conic)

# import Alaskan fuel data
alaskan_file_path = "data/FCCS_Alaska.nc"
akdata = xr.open_dataset(alaskan_file_path)
print("ALASKA: ", akdata)
#plt.clf()
#akdata.Band1.plot()
#plt.savefig('AKnc.png')
