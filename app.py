import sys
sys.path.append('/falcon_ml/src')

import streamlit as st
import pandas as pd
from popular_rec_model import *
from ImplicitSec_rec_model import *
import torch

def main():
    st.title('Movie Recommender')

    data = pd.read_csv('/falcon_ml/Data/movies.csv')
    movies = data['title'].values
    genres = ['', 'Action', 'Adventure', 'Animation', 'Children', 'Comedy', 'Crime', 'Documentary', 'Drama', 'Fantasy',
              'Film-Noir', 'Horror', 'IMAX', 'Musical', 'Mystery', 'Romance', 'Sci-Fi', 'Thriller', 'War',
              'Western']

    with open('/falcon_ml/trained_models/popular_rec_model.pkl', 'rb') as file:
        popul_model = pd.read_pickle(file)

    imp_sec_model = torch.load('/falcon_ml/trained_models/ImplicitSec_rec_model.pth')

    with st.form("my_form"):
        selected_movies = st.multiselect("Choose Movies", movies)
        selected_genre = st.selectbox("Genre", genres)

        if selected_genre == '':
            selected_genre = None
        submitted = st.form_submit_button("Submit")

        if submitted:
            if (len(selected_movies) == 0):
                if selected_genre == None:
                    # If no movie and no genre selected. We give the 5 films that falcons team like the most
                    st.text("No movies and no genre selected. Here are our 5 favorite movies")
                    recommendations = ['Pulp Fiction (1994)', 'Green Book (2018)',
                                       'Inception (2010)', 'The Godfather (1972)', 'Kill Bill: Vol. 1 (2003)']
                else:
                    # Popular recommender
                    movie_id_recommendations = popul_model.predict(genre=selected_genre, at=5)
                    recommendations = from_id_to_title(movie_id_recommendations, data)
                st.table(recommendations)
            else:
                # Spotlight recommender
                # Convert title to item_id
                titles_df = pd.DataFrame({'title': selected_movies})
                result_df = pd.merge(titles_df, data, on='title', how='left')
                input_movies_ids = result_df['item_ids'].values
                movie_id_recommendations = predict(model=imp_sec_model, input_movie_ids=input_movies_ids,
                                                   genres_df=data, genre=selected_genre, at=5)
                recommendations = from_id_to_title(movie_id_recommendations, data)
                st.table(recommendations)

if __name__ == '__main__':
    main()