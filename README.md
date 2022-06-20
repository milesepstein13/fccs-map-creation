# fccs-map-creation


Run conversion.py to convert a tif with FBP fuels to a netCDF with fccs fuels. Change scale_factor to scale the data. Either store the input in `data/nat_fbpfuels_2014b.tif`, or change `canadian_file_path` to the path of your input. The result is saved as `data/fccs_canada`

`data/fccs_fuelload.nc` is also used to get metadata in the correct format. All other files are for testing or created by tests. In particular, readCAnc.py is used to test that the output is correct. 

# How to use the produced netCDF in playground
1. Upload to fccsmap repository
2. Ensure bluesky references the updated fccsmap
3. Upload this version of bluesky to dockerhub
4. Ensure bluesky-web's dockerfile is built from that image
