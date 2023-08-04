import cdsapi
import yaml

with open(".cdsapirc", 'r') as f:
        credentials = yaml.safe_load(f)

c = cdsapi.Client(url=credentials['url'], key=credentials['key'])


#for year in ["2019", "2020", "2021"]
#    for month in ["01", "02", "03", "04", "05", "06", "07", "08", "09", "10", "11", "12"]:

for year in ["2020"]:
    for month in ["01"]:
        
        c.retrieve(
            'cams-europe-air-quality-reanalyses',
            {
                'type': 'validated_reanalysis',
                'year': year,
                'format': 'zip',
                'variable': ['carbon_monoxide', 'nitrogen_dioxide', 'ozone',
                             'particulate_matter_10um', 'particulate_matter_2.5um', 'sulphur_dioxide'],
                'model': 'ensemble',
                'level': '0',
                'month': month,
            },
            f'/mnt/data/raw/cams_euro_aq_reanalysis/{year}/download_{year}_{month}.zip')


