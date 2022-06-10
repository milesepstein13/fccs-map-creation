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

# import Canadian fuel data
canadian_file_path = "data/nat_fbpfuels_2014b.tif"
cdata = xr.open_rasterio(canadian_file_path)

# transform to match US
print(cdata)
p1 = pyproj.Proj(cdata.crs)
#todo: automate parameters below from adata
p2 = pyproj.Proj("+proj=lcc +lat_0=40 +lon_0=-100 +lat_1=33 +lat_2=45")
(newx, newy) = pyproj.transform(p1, p2, cdata.x[0:np.size(cdata.y)], cdata.y) #wrong but for proof of concept
print(newx)
print(newy)

# convert Canadian fuel types to American


print("A")
# import American fuel data
adata = xr.open_dataset("data/fccs_fuelload.nc")
#print(adata.attrs)

# add coordinates from metadata
xcoords = np.linspace(adata.XORIG, adata.XORIG + adata.XCELL*adata.NCOLS, num=adata.NCOLS)
ycoords = np.linspace(adata.YORIG, adata.YORIG + adata.YCELL*adata.NROWS, num=adata.NROWS)

adata = adata.FCCS_FuelLoading
#print(adata)
adata = adata.assign_coords(COL=xcoords)
adata = adata.assign_coords(ROW=ycoords)
#print(adata)

print("FUELLOADING: ")
#print(adata)
adata.plot()
plt.savefig('UStestfig.png')

# combine datasets




# export to netCDF