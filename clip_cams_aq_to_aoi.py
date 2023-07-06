import xarray as xr


year = "2019"
month = "01"
bounding_box = [45.82, 50.65, 8.95, 17.22]

# read in data 
path_to_cams_aq_nc_file = f"../data/raw/cams_euro_aq_reanalysis/{year}/download_{year}_{month}.nc"
ds = xr.open_dataset(path_to_cams_aq_nc_file)

# extract long and lat from dataset
lat = ds['latitude']
lon = ds['longitude']

# Determine the indices of the bounding box in the spatial dimensions:
lat_min, lat_max = bounding_box[0], bounding_box[1]
lon_min, lon_max = bounding_box[2], bounding_box[3]

lat_indices = (lat >= lat_min) & (lat <= lat_max)
lon_indices = (lon >= lon_min) & (lon <= lon_max)

# Clip the dataset based on the calculated indices
clipped_ds = ds.sel(latitude=lat_indices, longitude=lon_indices)

# save clipped nc file
path_to_clipped_file = "../data/processed/cams_aoi_aq_reanalysis/{year}/aq_aoi_{year}_{month}.nc"
clipped_ds.to_netcdf(path_to_clipped_file)