import streamlit as st
import pandas as pd
from popular_rec_model import *
from ImplicitSec_rec_model import *
import torch

def main():
    st.title('Movie Recommender') 

    data = pd.read_csv('../Data/movies.csv')
    movies = data['title'].values
    genres = ['', 'Action', 'Adventure', 'Animation', 'Children', 'Comedy', 'Crime', 'Documentary', 'Drama', 'Fantasy',
              'Film-Noir', 'Horror', 'IMAX', 'Musical', 'Mystery', 'Romance', 'Sci-Fi', 'Thriller', 'War',
              'Western']

    with open('../trained_models/popular_rec_model.pkl', 'rb') as file:
        popul_model = pd.read_pickle(file)

    imp_sec_model = torch.load('../trained_models/ImplicitSec_rec_model.pth')      

    # Initialize session state
    if 'times_visualized' not in st.session_state:
        st.session_state.times_visualized = 0
    if 'recommendations' not in st.session_state:
        st.session_state.recommendations = []
    if 'more_recommendations' not in st.session_state:
        st.session_state.more_recommendations = []
    if 'ratings' not in st.session_state:
        st.session_state.ratings = {}

    with st.form("my_form"):
        selected_movies = st.multiselect("Choose Movies", movies)
        selected_genre = st.selectbox("Genre", genres)

        if selected_genre == '':
            selected_genre = None
        submitted = st.form_submit_button("Submit")

        if submitted:
            st.session_state.times_visualized = 1   # Reset times_visualized
            st.session_state.recommendations = []   # Reset recommendations
            st.session_state.more_recommendations = []   # Reset more_recommendations

            if (len(selected_movies) == 0):
                if selected_genre == None:
                    # If no movie and no genre selected. We give the 5 films that falcons team like the most
                    st.text("No movies and no genre selected. Here are our 5 favorite movies")
                    st.session_state.recommendations = ['Pulp Fiction (1994)','Green Book (2018)',
                                                        'Inception (2010)', 'The Godfather (1972)', 'Kill Bill: Vol. 1 (2003)']
                else:
                    # Popular recommender
                    movie_id_recommendations = popul_model.predict(genre=selected_genre, at=100)
                    st.session_state.recommendations = from_id_to_title(movie_id_recommendations, data)
            else:
                # Spotlight recommender
                # Convert title to item_id
                titles_df = pd.DataFrame({'title': selected_movies})
                result_df = pd.merge(titles_df, data, on='title', how='left')
                input_movies_ids = result_df['item_ids'].values
                # Give the prediction
                movie_id_recommendations = predict(model=imp_sec_model, input_movie_ids=input_movies_ids,
                                                   genres_df = data,genre=selected_genre,at=100)
                
                st.session_state.recommendations = from_id_to_title(movie_id_recommendations, data)

    if len(st.session_state.recommendations) > 0:   # Display recommendations obtained from the form
        st.subheader("Top 5 movies for your preferences")
        display_movies_with_sliders(st.session_state.recommendations[0:5])

    if len(st.session_state.recommendations)-5 > 0:   # The recommendations are more than 5
        with st.form("more_recommendations_form"):
            st.subheader('More recommendations for the same preferences')
            
            submitted_2 = st.form_submit_button("More recommendations")
                
            if submitted_2:
                if (st.session_state.times_visualized) * 5 < len(st.session_state.recommendations):   # If there are some recommendations left
                    if (st.session_state.times_visualized + 1) * 5 < len(st.session_state.recommendations):
                        st.session_state.more_recommendations = st.session_state.recommendations[st.session_state.times_visualized * 5:(st.session_state.times_visualized + 1) * 5]
                    else:   # If there are less than 5 recommendations left
                        st.session_state.more_recommendations = st.session_state.recommendations[st.session_state.times_visualized * 5:]
                    
                    st.session_state.times_visualized += 1
                else:
                    st.session_state.more_recommendations = []
                    st.text("There are no more recommendations. Please select new movies or a new genre")

    if len(st.session_state.more_recommendations) > 0:   # Display more recommendations obtained from the form
        display_movies_with_sliders(st.session_state.more_recommendations)

    print(st.session_state.ratings)
    

def display_movies_with_sliders(movies):
    # Display movies in a table with sliders for ratings using st.beta_columns
    for movie in movies:
        col1, col2 = st.columns(2)
        with col1:
            st.write(movie)
        with col2:
            rating = st.slider(f"Share your personal rating", 0, 5, 0, key=f"rating_{movie}")
            if rating > 0:
                st.session_state.ratings[movie] = rating

if __name__ == '__main__':
    main()