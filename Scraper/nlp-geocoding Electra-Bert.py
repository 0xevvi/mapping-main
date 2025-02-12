from transformers import AutoTokenizer, AutoModelForTokenClassification, pipeline 
import pandas as pd

# HTML sanitization
from html_sanitizer import Sanitizer
sanitizer = Sanitizer({
    'tags': ('h1', 'h2', 'p'),
    'attributes': {},
    'empty': set(),
    'separate': set(),
})

# Electra from HuggingFace
tokenizer = AutoTokenizer.from_pretrained("dbmdz/electra-large-discriminator-finetuned-conll03-english")
model = AutoModelForTokenClassification.from_pretrained("dbmdz/electra-large-discriminator-finetuned-conll03-english")
ner_pipeline = pipeline("ner",model=model, 
                tokenizer=tokenizer)

# DF to process
## Source file
file = pd.read_csv('./Scraper/data/HWdb1.csv')
## DF to save to 
processed = pd.DataFrame(
    columns=['date', 'title.rendered', 'excerpt.rendered', 'link', 'geocoded'])

# Iterate through file and process the excerpt in each document
for index, row in file.iterrows():
    list = ner_pipeline(sanitizer.sanitize(file.at[index, 'excerpt.rendered']))

    for entity in list:
        if entity['entity'] == 'I-LOC':
            loc = entity['word']
    print(loc + '\n' + sanitizer.sanitize(file.at[index, 'excerpt.rendered']) + '\n')


