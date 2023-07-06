import cdsapi
import yaml

with open("../plattforms/ads/.cdsapirc", 'r') as f:
        credentials = yaml.safe_load(f)

c = cdsapi.Client(url=credentials['url'], key=credentials['key'])

c.retrieve(
    'cams-europe-air-quality-reanalyses',
    {
        'type': 'validated_reanalysis',
        'year': '2020',
        'format': 'zip',
        'month': '08',
        'level': '0',
        'model': 'ensemble',
        'variable': 'particulate_matter_2.5um',
    },
    '../data/download.zip')

