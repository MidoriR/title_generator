import requests
from bs4 import BeautifulSoup
import time
import re
import json

#Get all links for talks in each year and store it in a dictionary

available_years = range(2009,2019)

urls = {}

for year in available_years:
    root_git = f'https://github.com/pyvideo/data/blob/41fdb50427599f1a0e780e8ebe98f2c7ed04420e/pycon-us-{year}/videos/'
    try:
        req = requests.get(root_git)
        soup = BeautifulSoup(req.content, 'html.parser')
        all_talks = soup.find_all('a', { 'id':re.compile('.')})
        titles = []
        for talk in all_talks:
            titles.append(talk.get('title'))
        urls[f'{year}'] = titles
    except Exception:
        print('There was a problem with your https {year} request. Try later')
    time.sleep(5)

# get all the json files

all_info = []
only_titles = []

for key in urls:
    for name in urls[key]:
        root_json = f'https://raw.githubusercontent.com/pyvideo/data/41fdb50427599f1a0e780e8ebe98f2c7ed04420e/pycon-us-{key}/videos/{name}'
        try:
            req = requests.get(root_json)
            filtered = {'title': req.json()['title'],
                        'description': req.json()['description']}
            all_info.append(filtered)
            only_titles.append(req.json()['title'])
            time.sleep(1.5)
        except Exception:
            print(f'there was a problem processing {key}, {name}')

# Save files

with open('all_info.json', 'w') as json_file:
    json.dump(all_info, json_file)

with open('titles.txt', 'w') as txt_file:
    for item in only_titles:
        txt_file.write('%s\n' % item)


