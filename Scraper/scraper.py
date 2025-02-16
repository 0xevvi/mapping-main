import requests
import fitz  # PyMuPDF
import spacy
from geopy.geocoders import Nominatim
import folium

# Step 1: Download the PDF
pdf_url = "https://tamilgenocidememorial.org/wp-content/uploads/2022/09/Massacres-of-Tamils-1956-2008.pdf"
response = requests.get(pdf_url)

# Save the PDF to a local file
with open("Massacres_of_Tamils_1956_2008.pdf", "wb") as f:
    f.write(response.content)

# Step 2: Extract Text from the PDF
doc = fitz.open("Massacres_of_Tamils_1956_2008.pdf")

# Extract text from each page
text = ""
for page_num in range(doc.page_count):
    page = doc.load_page(page_num)
    text += page.get_text()

# Step 3: Load SpaCy Model for Named Entity Recognition (NER)
nlp = spacy.load("en_core_web_sm")

# Process the extracted text
doc = nlp(text)

# Extract the named locations (GPE: Geopolitical Entity)
locations = [ent.text for ent in doc.ents if ent.label_ == "GPE"]

# Step 4: Geocode the Locations to Get Latitude and Longitude
geolocator = Nominatim(user_agent="TamilWatchDog")

def geocode_location(location):
    location_obj = geolocator.geocode(location)
    if location_obj:
        return location_obj.latitude, location_obj.longitude
    else:
        return None

# Geocode the extracted locations
geocoded_locations = []
for location in locations:
    geocoded_location = geocode_location(location)
    if geocoded_location:
        geocoded_locations.append(geocoded_location)

# Step 5: Create a Map Using Folium and Plot the Locations
# Initialize the map (centered around a default location)
m = folium.Map(location=[8.0, 81.0], zoom_start=6)

# Add markers for each geocoded location
for lat, lon in geocoded_locations:
    folium.Marker([lat, lon]).add_to(m)

# Save the map as an HTML file
m.save("tamil_watchdog_map.html")

print("Map saved as 'tamil_watchdog_map.html'")


# import requests
# import pandas as pd

# i = 1
# while True:
#     # Make a GET request to the website that returns a JSON response
#     url = "https://hindutvawatch.org/wp-json/wp/v2/posts?_embed&per_page=100&page=" + str(i)
#     response = requests.get(url)

#     if response.status_code == 200:
#         # Convert the JSON response into a Pandas dataframe
#         data = response.json()
#         df = pd.json_normalize(data)

#         # printing all columns of the dataframe
#         # print(df.columns)
#         dfSelected = df.loc[:, ['id', 'date', 'title.rendered', 'excerpt.rendered', 'link', 'content.rendered', 'featured_media']]

#         # Save the dataframe as a CSV file
#         dfSelected.to_csv("data/HWdb1.csv", mode='a',  index=False)

#         print("Data of page" + str(i) + "saved to output.csv")
#         i += 1
    
#     else:
#         print("No more pages to scrape after page " + str(i-1))
#         break
    