# Spotlight Package

The aim of the documentation is to provide a brief overview of the existing model and how we can use it.

## Data used

- MovieLens: public dataset. Data is organised according to 'Id', 'Ratings'
- We need to add the Genre and the Title of each movie, so we download the file directly from Movilens and we merge both datasets.


## Recommender from Spotlight

1. **Implicit Sequence Model**: model for recommending items given a sequence of previous items. This is the one firstly implemented in our app, as the idea is to get recommendations based on a previous selection of some films.

Other models available in Spotlight:

- *Sequence representations*: submodule available where we can model the users relating to the items they have interacted.

- *Implicit Factorization Model*: model used for making a prediction based on a user's behaviour. As we don't have users for now, this is not valid for us (it is based in user-item)

- *Explicit Factorization Model*: model used for making a prediction based on the inputs the user has made himself. Similar casuistic as the previous one

- *Latent Representation*: also based in users.

## Popular Recommender

  **Top Popular Recommender model**: This model will be used in the case that the user only takes as input genre, without any film suggestion. In that case, a popular recommender is implemented, which will recommend the most popular films (based on the ratings) on that genre.



