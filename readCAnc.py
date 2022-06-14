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
print(data)
data.__xarray_dataarray_variable__[0, 9000:14000, 1000:4500].plot()
plt.savefig('CAnc.png')