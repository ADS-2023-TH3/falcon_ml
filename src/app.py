import streamlit as st
import pandas as pd
from popular_rec_model import *
from ImplicitSec_rec_model import *
import torch


def main():
    st.title('Movie Recommender')

    # First we read the data and get the list of movies, we will need it to desplay in the select box
    # We also define the list of Genres
    data = pd.read_csv('../Data/title_films.csv')
    movies = data['title'].values
    genres = ['', 'Action', 'Adventure', 'Animation', 'Children', 'Comedy', 'Crime', 'Documentary', 'Drama', 'Fantasy',
              'Film-Noir', 'Horror', 'IMAX', 'Musical', 'Mystery', 'Romance', 'Sci-Fi', 'Thriller', 'War',
              'Western']

    # load the models
    # popular recommender
    with open('../trained_models/popular_rec_model.pkl', 'rb') as file:
        popul_model = pd.read_pickle(file)

    # General model
    imp_sec_model = torch.load('../trained_models/ImplicitSec_rec_model.pth')

    # What comes next is a form. A form is a set of input elements and a submit button.
    # When you click submit the form will return selected movies and genre and will run the code
    # to give a recommendation according to the input data.
    with st.form("my_form"):
        selected_movies = st.multiselect("Choose Movies", movies)
        selected_genre = st.selectbox("Genre", genres)

        # We have to change the blank space for None for the models to work correctly
        if selected_genre == '':
            selected_genre = None
        # submit button.
        submitted = st.form_submit_button("Submit")

        # The following logic structure selects the model to use.
        # 1. The user selcts movies --> General model
        # 2. No movies:
        # 2.1 Genre selected --> popular recomender
        # 2.2 No Genre --> Our recommendations
        # There are a series of transformations from movie to movie id and viceversa for the
        # inputs/outputs to work correctly
        if submitted:
            if (len(selected_movies) == 0):
                if selected_genre == None:
                    recommendations = movies[:5]
                else:
                    movie_id_recommendations = popul_model.predict(genre=selected_genre)
                    recommendations = from_id_to_title(movie_id_recommendations, data)
                st.table(recommendations)
            else:
                input_movies_ids = data.loc[data['title'].isin(selected_movies), 'item_ids'].values
                movie_id_recommendations = predict(model=imp_sec_model, input_movie_ids=input_movies_ids,
                                                   genre=selected_genre)
                recommendations = from_id_to_title(movie_id_recommendations, data)
                st.table(recommendations)


if __name__ == '__main__':
    main()