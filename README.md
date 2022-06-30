# fccs-map-creation


Run conversion.py to convert a tif with FBP fuels to a netCDF with fccs fuels. Change scale_factor to scale the data. Either store the input in `data/nat_fbpfuels_2014b.tif`, or change `canadian_file_path` to the path of your input. The result is saved as `data/fccs_canada`

`data/fccs_fuelload.nc` is also used to get metadata in the correct format. All other files are for testing or created by tests. In particular, readCAnc.py is used to test that the output is correct. 


# How to test the produced netCDF in playground
1. Upload fccs_canada.nc to fccsmap/fccsmap/data (mine is forked from pnwairfire/fccsmap)
2. In fuelbeds.py of bluesky, ensure imports of fccsmap/FccsLookUp are from an updated version of fccsmap (for testing, I just used a relative import)
3. Follow "Building Docker Image" instructions [here](https://gl.tawhiri.eos.ubc.ca/bluesky/bluesky/-/blob/master/docs/installation.md) to build an image of bluesky
4. change the dockerfile of bluesky-web to be `FROM bluesky` to use that image

# Changes I made to accomadate this new file (if things aren't working, check that this are all done)
1. In fccsmap/fccsmap/lookup:
    1. added a Canadian option to `FUEL_LOAD_NCS` following existing formatting
    2. added `is_canada` (like `is_alaska`) in OPTIONS_STRING
    3. `fuel_load_key` assignment logic handles `is_canada`
2. In bluesky/modules/fuelbeds, add `FccsLookUp(is_canada=True, **Config().get('fuelbeds')) # Canada` to `FCCS_LOOKUPS`
