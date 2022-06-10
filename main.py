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

# import Canadian fuel data
canadian_file_path = "data/nat_fbpfuels_2014b.tif"
cdata = xr.open_rasterio(canadian_file_path)

# convert Canadian fuel types to American

# import American fuel data
adata = xr.open_dataset("data/fccs_fuelload.nc")

# get both datasets in a form that can be combined
#transform = Affine.from_gdal(*cdata.attrs['transform'])
#nx, ny = cdata.sizes['x'], cdata.sizes['y']
#x, y = np.meshgrid(np.arange(nx)+0.5, np.arange(ny)+0.5) * transform
#print(x)
# combine datasets

print(adata.ROW)


# export to netCDF