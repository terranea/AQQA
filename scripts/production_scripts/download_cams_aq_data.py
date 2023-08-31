import cdsapi
import yaml
import argparse


def download_cams_aq_data(year: str, month: str, variables: list, _type: str, path_to_output: str, ):
    """
    downloads CAMS air quality data from Atmospheric data store 
    """
    
    c.retrieve(
        'cams-europe-air-quality-reanalyses',
        {
            'type': _type,
            'year': year,
            'format': 'zip',
            'variable': variables,
            'model': 'ensemble',
            'level': '0',
            'month': month,
        },
        path_to_output)


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="Download CAMS air quality data from Atmospheric data store.")
    
    # specify CLI arguments
    parser.add_argument("--year", required=True, help="Year for which to download the data")
    parser.add_argument("--month", required=True, help="Month for which to download the data")
    parser.add_argument("--variables", nargs="+", required=True, help="List of variables to download")
    parser.add_argument("--type", required=True, help="Type of data to download")
    parser.add_argument("--output-path", required=True, help="Path to save the downloaded data")
    
    args = parser.parse_args()

    # Open and load credentials from the .cdsapirc file
    with open("/workspaces/aqqa-kg-creation-dev/.cdsapirc", 'r') as f:
        credentials = yaml.safe_load(f)

    c = cdsapi.Client(url=credentials['url'], key=credentials['key'])
    
    download_cams_aq_data(args.year, args.month, args.variables, args.type, args.output_path)

