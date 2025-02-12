# import spacy
# import csv

# import pandas as pd 
# import geopandas as gpd 
# import geopy 
# import matplotlib.pyplot as plt
# from geopy.extra.rate_limiter import RateLimiter

# nlp = spacy.load('en_core_web_lg', disable=["parser"])
# nlpWK = spacy.load('xx_ent_wiki_sm')

# # Set up geolocator
# geolocator = geopy.geocoders.Nominatim(user_agent="HWdbScraper")

# file = pd.read_csv('HWdb1.csv')
# file['geocoded'] = ''
# file['coords'] = ''

# for (index, parsed_doc) in zip(file.iterrows(), nlp.pipe(iter(file['excerpt.rendered']))):
#     # Which field to use for NER
#     smallest_location = None
#     for ent in parsed_doc.ents:
#         # Spacy NER Named Entity Recognition tags

#         # rank NER tags, based on location
#         if (ent.label_ == 'LOC' or ent.label_ == 'GPE'):
#             location = geolocator.geocode(ent.text, timeout=4)
#             if location is not None:
#                 if smallest_location is None or (location.raw.get('importance', 0) < smallest_location.raw.get('importance', 0)):
#                     smallest_location = location
#     if smallest_location is not None:
#         file.at[index, 'geocoded'] = smallest_location
#         # Create point geometry
#         point = gpd.points_from_xy([smallest_location.longitude], [smallest_location.latitude])
#         file.at[index, 'coords'] = point
#         print(str(index) + " Smallest location named "+ smallest_location.address + " geocoded to " + str(smallest_location))
        
#     if (index>90):
#         break
                
# file.to_csv('HWdb1_geocoded.csv', index=False)

import spacy
from spacy import displac
import csv
import pandas as pd 
import geopandas as gpd 
import geopy 
import matplotlib.pyplot as plt
from geopy.extra.rate_limiter import RateLimiter
import concurrent.futures

nlp = spacy.load('en_core_web_lg')
nlpWK = spacy.load('xx_ent_wiki_sm')

# Set up geolocator
geolocator = geopy.geocoders.Nominatim(user_agent="HWdbScraper")

file = pd.read_csv('./Scraper/data/HWdb1.csv')
file['geocoded'] = ''
file['coords'] = ''

# Define a function to process each document
def process_doc(doc, index):
    smallest_location = None
    for ent in doc.ents:
        # Spacy NER Named Entity Recognition tags

        # rank NER tags, based on location
        if (ent.label_ == 'LOC' or ent.label_ == 'GPE'):
            displacy.serve(doc, style="ent")
            # location = geolocator.geocode(ent.text, timeout=4)
            # if location is not None:
            #     if smallest_location is None or (location.raw.get('importance', 0) < smallest_location.raw.get('importance', 0)):
            #         smallest_location = location
            # if smallest_location is not None:
            #     file.at[index, 'geocoded'] = smallest_location
            #     # Create point geometry
            #     point = gpd.points_from_xy([smallest_location.longitude], [smallest_location.latitude])
            #     file.at[index, 'coords'] = point
            #     print(str(index) + " Smallest location named "+ smallest_location.address + " geocoded to " + str(smallest_location))

# Use nlp.pipe to process the documents in parallel
docs = list(nlp.pipe(file['excerpt.rendered'].astype('str')))
with concurrent.futures.ThreadPoolExecutor(max_workers=8) as executor:
    futures = [executor.submit(process_doc, doc, index) for index, doc in enumerate(docs)]

# Write the updated DataFrame to a file
file.to_csv('./Scraper/data/HWdb2_geocoded.csv', index=False)
