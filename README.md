# Prototyping a map interface for Hindutva Watch

- The HW database is a collection of news articles, tweets, and other sources of information about the activities of Hindutva groups in India.
- I believe it is pertinent to develop a easier way to understand relationships between these groups and their activities.

## Prototype
- The database is scraped from the Hindutva Watch website and stored in a CSV
- ```SpaCy``` is used to extract named locations (NER) from the text
- The lowest denominator location is selected and geocoded. This might be a cause for concern as the geocoding is not always accurate. Choices have to be weighted better
- It is then mapped using ```Leaflet```,
- ```Svelte``` and ```Svelvet``` are used to create interactions and a narrative maker.

## Roadmap
- [ ] Refine geocoding to be more accurate.
  - For example, when the SpaCy is fed 
    ```<p><iframe loading="lazy" title="Karnataka Dalit Woman Tied To Pole, Thrashed After Cows Strayed Into Field" width="696" height="392" src="https://www.youtube.com/embed/CEbl9JCoSyI?feature=oembed" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" allowfullscreen></iframe></p> <p><b class="place_cont">Bengaluru: </b></p> <p>A woman from the Dalit community was thrashed after her cow strayed into the field of an upper caste man in Karnataka&#8217;s Koppal district.</p> <p>A police case has been filed against the man, Amrish Kumbar, under the Scheduled Castes and Scheduled Tribes (Prevention of Atrocities) Act, which severely punishes ill-treatment to tribes. The man has been arrested, the police said.</p> <p>A video of the beating has been shared widely on social media.</p> <p>The woman, Shobhamma Harijan, is seen pleading with the man to stop thrashing her. But he continues to hurl expletives as he hits her.</p> <p>According to the police complaint, when Ms Harijan saw that her cow had strayed into Mr Kumbar&#8217;s fields, she quickly went there to bring it home.</p> <p><em>This story was originally published in ndtv.com . Read the full story <a href="https://www.ndtv.com/karnataka-news/on-camera-karnataka-dalit-woman-thrashed-after-cow-strays-into-field-3768434">here</a></em></p> ```

    It returns ```Castès, Sospel, Nice, Alpes-Maritimes, Provence-Alpes-Côte d'Azur, France métropolitaine, 06380, France``` as the location. This is not correct. The correct location is ```Koppal, Karnataka, India```. I believe it has taken "castes" as the Named Entity.
- [ ] Persistent state and sharing for narratives created on the narrative maker
- [ ] Research on event classification and other narrative building elements.    


### LLM models 
- Alpaca, AlpacaLora, LLaMa etc... (https://huggingface.co/Pi3141/alpaca-native-13B-ggml/tree/main)
  - Both the 7B and 13B are highly dependant on the prompts, they need to be explored
- Instructor Embedder (https://huggingface.co/hkunlp/instructor-large)
  - 
- Electra (https://huggingface.co/spaces/brijw/transformers_ner/blob/main/app.py)