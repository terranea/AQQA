import xarray as xr
import datetime
import json
from shapely.geometry import Point


def load_json_file(file_path):
    "load json file from path"
    with open(file_path) as json_file:
        return json.load(json_file)


def coordinates_to_wkt(x, y):
    "convert point coordinates to wkt literal"
    point = Point(x, y)
    wkt = point.wkt
    return wkt


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


def unix_ts_to_date_str(ts: int):
    """Function converts unix timestamp to date string"""

    unix_timestamp = ts / 1_000_000_000  # Convert nanoseconds to seconds
    date_obj = datetime.date.fromtimestamp(unix_timestamp)
    formatted_date = date_obj.strftime("%Y-%m-%d")
    return formatted_date