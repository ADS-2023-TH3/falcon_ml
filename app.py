import streamlit as st
from your_recommender_module import get_recommendations  # Import your recommender function

# Streamlit app code
st.title('Movie Recommender App')

# User input for movie title
user_movie_title = st.text_input('Enter a movie title:')

if user_movie_title:
    # Get recommendations based on user input
    recommendations = get_recommendations(user_movie_title)
    
    # Display recommendations to the user
    st.subheader('Top 5 Recommendations:')
    for idx, movie in enumerate(recommendations[:5]):
        st.write(f'{idx + 1}. {movie}')
