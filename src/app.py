import streamlit as st
import pandas as pd
from popular_rec_model import *
from ImplicitSec_rec_model import *

import torch

# Specify the path to your .pth file




def main():
    st.title('Movie Recommender')
    data = pd.read_csv('../Data/title_films.csv')
    movies=data['title'].values


    

    genres = ['','Action', 'Adventure', 'Animation', 'Children', 'Comedy', 'Crime', 'Documentary', 'Drama', 'Fantasy',
                  'Film-Noir', 'Horror', 'IMAX', 'Musical', 'Mystery', 'Romance', 'Sci-Fi', 'Thriller', 'War',
                  'Western']
    # Load the model from the saved file
    with open('../trained_models/popular_rec_model.pkl', 'rb') as file:
        popul_model = pd.read_pickle(file)
    # Load the model
 
    imp_sec_model = torch.load('../trained_models/ImplicitSec_rec_model.pth')

    
    with st.form("my_form"):
        st.write("Inside the form")
        selected_movies=st.multiselect("Choose Movies",movies)
        selected_genre=st.selectbox("Genre",genres)
        if selected_genre=='':
            selected_genre=None
        # Every form must have a submit button.
        submitted=st.form_submit_button("Submit")
        if submitted:
            if (len(selected_movies)==0):
                if selected_genre==None:
                    recommendations=movies[:5]
                else:
                    movie_id_recommendations = popul_model.predict(genre = selected_genre)
                    recommendations = from_id_to_title(movie_id_recommendations,data)
                st.table(recommendations)
            else: 
                input_movies_ids=data.loc[data['title'].isin(selected_movies),'item_ids'].values
                movie_id_recommendations=predict(model=imp_sec_model, input_movie_ids=input_movies_ids, genre = selected_genre) 
                recommendations = from_id_to_title(movie_id_recommendations,data)
                st.table(recommendations)

if __name__ == '__main__':
    main()
