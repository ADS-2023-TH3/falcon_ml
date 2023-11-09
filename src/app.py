import streamlit as st
import pandas as pd

def main():
    st.title('Movie Recommender')
    movies = [
        "The Shawshank Redemption",
        "The Godfather",
        "The Dark Knight",
        "Pulp Fiction",
        "Schindler's List",
        "The Lord of the Rings: The Return of the King",
        "Forrest Gump",
        "Inception",
        "Star Wars: Episode V - The Empire Strikes Back",
        "The Matrix",
        "The Silence of the Lambs",
        "Fight Club",
        "Gladiator",
        "The Avengers",
        "Titanic",
        "Jurassic Park",
        "Avatar",
        "The Lion King",
        "E.T. the Extra-Terrestrial",
        "The Terminator"
    ]

    genres = ['Action', 'Adventure', 'Animation', 'Children', 'Comedy', 'Crime', 'Documentary', 'Drama', 'Fantasy',
                  'Film-Noir', 'Horror', 'IMAX', 'Musical', 'Mystery', 'Romance', 'Sci-Fi', 'Thriller', 'War',
                  'Western']



    with st.form("my_form"):
        st.write("Inside the form")
        selected_movies=st.multiselect("Choose Movies",movies)
        selected_genre=st.selectbox("Genre",genres)
        # Every form must have a submit button.
        submitted=st.form_submit_button("Submit")
        if submitted:
            st.write("slider", selected_movies, "checkbox", selected_genre)
            df = pd.DataFrame(movies[:5], columns=["Movie Title"])
            st.dataframe(df)

    st.write('outside')

if __name__ == '__main__':
    main()





