import streamlit as st
import pandas as pd
from popular_rec_model import *
import pickle


def main():
    st.title('Movie Recommender')
    data = pd.read_csv('../Data/title_films.csv')
    movies = data['Title'].values

    genres = ['', 'Action', 'Adventure', 'Animation', 'Children', 'Comedy', 'Crime', 'Documentary', 'Drama', 'Fantasy',
              'Film-Noir', 'Horror', 'IMAX', 'Musical', 'Mystery', 'Romance', 'Sci-Fi', 'Thriller', 'War',
              'Western']

    # Load the model from the saved file
    with open('../trained_models/popular_rec_model.pkl', 'rb') as file:
        popul_model = pickle.load(file)
    with st.form("my_form"):
        st.write("Inside the form")
        selected_movies = st.multiselect("Choose Movies", movies)
        selected_genre = st.selectbox("Genre", genres)
        # Every form must have a submit button.
        submitted = st.form_submit_button("Submit")
        if submitted:
            if (len(selected_movies) == 0):
                movie_id_recommendations = popul_model.predict(genre=selected_genre)
                recommendations = from_id_to_title(movie_id_recommendations, data)
                st.table(recommendations)
            else:
                df = pd.DataFrame(movies[-5:], columns=["Movie Title"])
                st.dataframe(df)


if __name__ == '__main__':
    main()





