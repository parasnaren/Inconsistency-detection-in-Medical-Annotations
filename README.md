# Inconsistency detection in Medical Annotations
Developed our own Phrase Embeddings of Medical data, using articles obtained from the PubMed FTP server. Medical terms that are semantically similar were clustered together, thereby helping to identify the inconsistencies.

*This project was developed as part of the onsite finals of the Smart India Hackathon, 2019. Due the an NDA, the dataset that we worked on to cluster entities could not be uploaded.*

## Creation of Embeddings

An *Ubuntu 16* server was used on **Google Cloud Platform** to train the embeddings, taking approximately 6 hours to developed the final embeddings.


## Phrasing of text

Phrasing of the text was done to obtain those medical terms that occurred frequently as phrases. Using the **Gensim** library module *Phrases*, we were successfully able to generate this set of phrases, occurring more than a threshold number of times.

<img src = "https://i.stack.imgur.com/KXD7F.png" height="60"/>

The above formula was used to generate a score for a pair of words occurring together. If this score exceeded a particular threshold, the two words are then paired as a phrase. This was continued until phrases of size 4 were created. (as very few phrases of size > 4 exist)


## Training

Word2Vec was used to train these embeddings using CBOW (Continous Bag of Words) approach.
The parameters for Word2Vec were:
