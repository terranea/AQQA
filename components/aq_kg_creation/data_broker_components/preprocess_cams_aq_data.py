import os
import xarray as xr
import zipfile
import glob
import argparse
from utils import clip_netcdf_to_bb
from zipfile import ZipFile

def preprocess_cams_aq_data(path_to_zip_folder: str, bounding_box: list, path_to_output: str):
    # Unzip CAMS AQ data
    with zipfile.ZipFile(path_to_zip_folder, 'r') as zip_ref:
        zip_ref.extractall(path_to_output)
    
    # Get paths to individual nc files
    search_string = os.path.join(path_to_output, "*.nc")
    path_to_files = glob.glob(search_string)

    for path_to_file in path_to_files:
        # Extract variable from path name
        var = path_to_file.split(".")[-4]

        # Open dataset
        ds = xr.open_dataset(path_to_file)

        # Clip data to bounding box
        ds_bb = clip_netcdf_to_bb(ds, bounding_box)

        # Period averaging
        if var == "O3":
            ds_bb_agg = ds_bb.resample(time="8H").mean()
        else:
            ds_bb_agg = ds_bb.resample(time="24H").mean()

        # Save netcdf
        year_month = ds_bb_agg.time.dt.strftime("%Y%m").values[0]
        path_output_variable = os.path.join(path_to_output, f"cams_aq_{var}_{year_month}.nc")
        ds_bb_agg.to_netcdf(path_output_variable)

        # delete extracted file
        os.remove(path_to_file)

        print(f"{var}-file processed!")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Preprocess CAMS air quality data (clip to bb and temporally aggregate).")
    
    # Specify CLI arguments
    parser.add_argument("--path-to-input", required=True, help="Path to zipped folder containing CAMS AQ data.")
    parser.add_argument("--bounding-box", required=True, nargs="+", type=float, help="Specify bounding box for your area of interest e.g. 45.82 50.65 8.95 17.22")
    parser.add_argument("--path-to-output", required=True, help="Path to location where unzipped preprocessed nc files should be stored.")
    
    args = parser.parse_args()
    preprocess_cams_aq_data(args.path_to_input, args.bounding_box, args.path_to_output)





