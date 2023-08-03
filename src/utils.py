import xarray as xr


def clip_netcdf_to_bb(ds: xr.core.dataset.Dataset, bounding_box: list):
    """Function clips netcdf file (loaded by xarray) to bounding box stored in list"""
    
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

    return clipped_ds