
import os
import xarray as xr
import zipfile
import glob
import argparse
from utils import clip_netcdf_to_bb


def preprocess_cams_aq_data(path_to_zip_folder: str, bb: list, path_to_output: str):

    # unzip cams aq data
    print(path_to_zip_folder)
    path_to_zip_folder = "/mnt/data/raw/cams_euro_aq_reanalysis/2020/download_2020_01.zip"
    with zipfile.ZipFile(path_to_zip_folder, 'r') as zip_ref:
        zip_ref.extractall(path_to_unzip_folder)
    
    # get directories to individual nc files
    search_string = f"{path_to_unzip_folder}/*"
    path_to_files = glob.glob(search_string)

    ds_dict = {}

    for path_to_file in path_to_files:

        # extract variable from path name
        var = path_to_file.split(".")[-4]

        # open dataset
        ds = xr.open_dataset(path_to_file)

        # clip data to bounding box
        ds_bb = clip_netcdf_to_bb(ds, bounding_box)

        # period averaging
        if var == "O3":
            ds_bb_agg = ds_bb.resample(time="8H").mean()
        else:
            ds_bb_agg= ds_bb.resample(time="24H").mean()

        # save netcdf 
        path_output_variable = os.path.join(path_to_output, f"cams_aq_{var}_{year}{month}.nc")
        ds_bb_agg.to_netcdf(path_output_variable)


if __name__ == "__main__":
    
    parser = argparse.ArgumentParser(description="Preprocess CAMS air quality data (clip to bb and temporally aggregate).")
    
    # specify CLI arguments
    parser.add_argument("--path-to-input", required=True, help="Path to zipped folder where nc files with CAMS AQ data is stored")
    parser.add_argument("--bounding-box", required=True,  nargs="+", help="Specify bounding box for your area of interest e.g. [45.82, 50.65, 8.95, 17.22]")
    parser.add_argument("--path-to-output", required=True, help="Path to location where unzipped preprocessed nc files should be stored")
    
    args = parser.parse_args()
    
    preprocess_cams_aq_data(args.path_to_input, args.bounding_box, args.path_to_output)




