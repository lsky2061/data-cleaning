#Pyton program to read JSON file containing DOE data catalogue

import json

f = open('doe-pdl-12-01-2020.json')

meta = json.load(f) #Dict with 5 items

catalogue = meta['dataset'] #This is a list of dictionaries; each dictionary describes a particular dataset

#Let's try to print just the titles of each dataset
for info in catalogue:
    #info is a dict
    title = info['title']
    if ('Electricity' in title): print(title)

f.close()
