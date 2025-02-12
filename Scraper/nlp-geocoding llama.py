from llama_cpp import Llama
from bs4 import BeautifulSoup
import pandas as pd

# HTML sanitization
from html_sanitizer import Sanitizer
sanitizer = Sanitizer({
    'tags': ('h1', 'h2', 'p'),
    'attributes': {},
    'empty': set(),
    'separate': set(),
})

# Source file
file = pd.read_csv('./Scraper/data/HWdb1.csv')

# DF to save to 
processed = pd.DataFrame(
    columns=['date', 'title.rendered', 'excerpt.rendered', 'link', 'geocoded'])

llm = Llama(model_path="C:/Users/adhav/Downloads/llama.cpp/models/ggml-vic7b-q4_0.bin",
            n_ctx=8192,
            use_mlock=False,  # Keeps the model in RAM
            )

# Iterate through file and process the excerpt in each document
for index, row in file.iterrows():

    loc = llm("""
       You are an excellent linguist. The task is to label location entities in the given sentence down to a village or a city or a state. Below are some examples. 

        Respond with a accurate location. The location must be geocodeable and in English.

        Example 1:
        Input: <p>On February 9, at Baramati, in rural Pune, Hindu Jangarjana Morcha organized by Sakal Hindu Samaj was successfully held where hate offender Kalicharan Maharaj freely delivered his hate speech rife with blatant lies and hysteria. This, despite urgent appeals being made by Citizens for Justice and Peace (CJP) to the DGP, Maharashtra as well as SP of  [&hellip;]</p>

        Output: Baramati, Pune,

        Example 2:
        Input: <p>A 400-year-old chapel in western India faces the threat of demolition as local politicians aim to acquire the land and use it for a football pitch, local Catholics have claimed. They are protesting that the chapel of Our Lady Of Remedies in Daman, built during the Portuguese colonial era in 1607, is threatened by a [&hellip;]</p>

        Output: Daman


        Example 3:
        Input: <p>KOPPAL: A 30-year-old woman was allegedly beaten up with a slipper by a man belonging to an upper caste after her cattle strayed into his agriculture field. The incident took place at Rampur village in Koppal district on February 3. The victim, who is from the Dalit community, said the accused, Amaresh Kumbar, beat her up [&hellip;]</p>

        Output: Rampur, Koppal

      
        Input:
        """ +

        sanitizer.sanitize(file.at[index, 'excerpt.rendered']) +

        "Output: ",
        stop=["\n"],

        max_tokens=2048,
        echo=True)
    print(loc['choices'][0]['text'])

    # Save data to dataframe
    processed.at[index] = [file.at[index, 'date'], file.at[index, 'title.rendered'],
                           file.at[index, 'excerpt.rendered'], file.at[index, 'link'], loc['choices'][0]['text']]
    
    # Save to csv every 10 loop
    if index % 10 == 0:
        processed.to_csv('./Scraper/data/HWdb_LLAMA_geocoded.csv', index=False, mode='a', header=False)

processed.to_csv('./Scraper/data/HWdb_LLAMA_geocoded.csv', index=False)
