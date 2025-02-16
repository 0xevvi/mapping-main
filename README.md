# Prototyping a map interface for Tamil Watch Dog

- The TWD database is a collection of news articles, tweets, and other sources of information about the activities of Tamil Nationalism.

## Prototype
- The database is scrapes from websites and stored in a CSV
- ```SpaCy``` is used to extract named locations (NER) from the text
- The lowest denominator location is selected and geocoded. This might be a cause for concern as the geocoding is not always accurate. Choices have to be weighted better
- It is then mapped using ```Leaflet```,
- ```Svelte``` and ```Svelvet``` are used to create interactions and a narrative maker.

## Roadmap
- [ ] Refine geocoding to be more accurate.
- [ ] Persistent state and sharing for narratives created on the narrative maker
- [ ] Research on event classification and other narrative building elements.    


### LLM models 
- Alpaca, AlpacaLora, LLaMa etc... (https://huggingface.co/Pi3141/alpaca-native-13B-ggml/tree/main)
  - Both the 7B and 13B are highly dependant on the prompts, they need to be explored
- Instructor Embedder (https://huggingface.co/hkunlp/instructor-large)
  - 
- Electra (https://huggingface.co/spaces/brijw/transformers_ner/blob/main/app.py)