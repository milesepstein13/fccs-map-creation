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
from pyproj import CRS
import proj
import rioxarray as rxr
import gdal 

# determined manually with https://www.fs.usda.gov/pnw/tools/fuel-and-fire-tools-fft
# based on canadian fuel types: https://cwfis.cfs.nrcan.gc.ca/background/fueltypes/c1
# 
ca_to_us_fuelbeds = {
    # key values from metadata of Canadian fuel data
    0: nan, # Out of domain
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
    if ((x % 100 == 0) & (y == 2000)):
        print(x, y)
        print("canadian fuelbed", canadian_fuelbed)
        print("american fuelbed", ca_to_us_fuelbeds[canadian_fuelbed])
    return ca_to_us_fuelbeds[canadian_fuelbed]

# import Canadian fuel data
canadian_file_path = "data/nat_fbpfuels_2014b.tif"
cdata = xr.open_rasterio(canadian_file_path, decode_coords="all")
print("CANADA: ")
print(cdata)
cdata = cdata.astype(np.float32)

# plot piece of initial data for comparision
print("Plotting initial")
cdata[0, 13000:14000, 2000:2500].plot() # full size doesn't resolve, too big
plt.savefig("CApre.png")

# resample
cdata = cdata.reindex(y = cdata.y[::4], x = cdata.x[::4], method = 'nearest')

# convert FBP fuel types to FCCS
for x in range(cdata.x.size):
    for y in range(cdata.y.size):
        data = cdata.data
        data[0, y, x] = fuelbed_convert(data[0, y, x], x, y)
        cdata.data = data
# smaller range for testing:
print("Converting fuelbeds")
#for x in range(3250, 3500):
#    for y in range(500, 625):
#        cdata.data[0, x, y]  = fuelbed_convert(cdata.data[0, x, y], x, y)        
print("new data")
print(cdata)
print("plotting final converted")
plt.clf()
cdata[0, 3250:3500, 500:625].plot() # full size doesn't resolve, too big
plt.savefig("CApost.png")

print("CONVERTING array to dataset")
# convert from dataarray to dataset (so it's like american data)
cdataset = cdata[0, :, :].to_dataset(name = "Band1")

# import American fuel data to use as reference
american_file_path = "data/fccs_fuelload.nc"
adataset = xr.open_dataset(american_file_path, decode_coords="all")


cdataset.attrs['Conventions'] = adataset.attrs['Conventions']

print("Converting metadata")
lcc = adataset.lambert_conformal_conic 
lcc.attrs['Northernmost_Northing'] = cdata.y.values[0]
lcc.attrs['Southernmost_Northing'] = cdata.y.values[-1]
lcc.attrs['Easternmost_Easting'] = cdata.x.values[-1]
lcc.attrs['Westernmost_Easting'] = cdata.x.values[0]
lcc.attrs['spatial_ref'] = CRS.from_proj4(cdata.attrs['crs']).to_wkt()
g = gdal.Open(canadian_file_path)
geotransform = ([g.GetGeoTransform()[0], g.GetGeoTransform()[1] * 4, g.GetGeoTransform()[2], g.GetGeoTransform()[3], g.GetGeoTransform()[4], g.GetGeoTransform()[5]*4])
lcc.attrs['GeoTransform'] = geotransform
lcc.attrs['central_meridian'] = -95
lcc.attrs['standard_parallel_1'] = 49
lcc.attrs['standard_parallel_2'] = 77
lcc.attrs['latitude_of_projection_origin'] = 49
cdataset = cdataset.assign_coords(lambert_conformal_conic = lcc)
cdataset = cdataset.drop_vars('band')
cdataset = cdataset.drop_vars('x')
cdataset = cdataset.drop_vars('y')
print("spatial_ref", lcc.attrs['spatial_ref'])
print("geotransform", lcc.attrs['GeoTransform'])


print("savings as netcdf")
# save as netcdf
cdataset.to_netcdf('data/fccs_canada.nc')

# to see that dataset works
plt.clf()
cdataset.Band1[3250:3500, 500:625].plot() 
plt.savefig("CAdataset.png")

