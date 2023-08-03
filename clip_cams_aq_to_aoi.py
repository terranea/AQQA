import xarray as xr
import glob


year = "2020"
month = "01"
bounding_box = [45.82, 50.65, 8.95, 17.22]

# read in data 
search_string = f"../data/raw/cams_euro_aq_reanalysis/{year}/download_{year}_{month}/*"
path_to_file = glob.glob(search_string)[0]

ds = xr.open_dataset(path_to_file)

# extract long and lat from dataset
lat = ds['lat']
lon = ds['lon']

# Determine the indices of the bounding box in the spatial dimensions:
lat_min, lat_max = bounding_box[0], bounding_box[1]
lon_min, lon_max = bounding_box[2], bounding_box[3]

lat_indices = (lat >= lat_min) & (lat <= lat_max)
lon_indices = (lon >= lon_min) & (lon <= lon_max)

# Clip the dataset based on the calculated indices
clipped_ds = ds.sel(lat=lat_indices, lon=lon_indices)

# save clipped nc file
path_to_clipped_file = f"../data/processed/cams_aoi_aq_reanalysis/{year}/aq_aoi_{year}_{month}.nc"
clipped_ds.to_netcdf(path_to_clipped_file)