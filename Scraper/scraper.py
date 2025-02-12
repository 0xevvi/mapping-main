import requests
import pandas as pd

i = 1
while True:
    # Make a GET request to the website that returns a JSON response
    url = "https://hindutvawatch.org/wp-json/wp/v2/posts?_embed&per_page=100&page=" + str(i)
    response = requests.get(url)

    if response.status_code == 200:
        # Convert the JSON response into a Pandas dataframe
        data = response.json()
        df = pd.json_normalize(data)

        # printing all columns of the dataframe
        # print(df.columns)
        dfSelected = df.loc[:, ['id', 'date', 'title.rendered', 'excerpt.rendered', 'link', 'content.rendered', 'featured_media']]

        # Save the dataframe as a CSV file
        dfSelected.to_csv("data/HWdb1.csv", mode='a',  index=False)

        print("Data of page" + str(i) + "saved to output.csv")
        i += 1
    
    else:
        print("No more pages to scrape after page " + str(i-1))
        break
    