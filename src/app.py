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

    selected_items=st.multiselect("Choose Movies",movies)
    if st.button("Recommend movies"):
        df = pd.DataFrame(movies[:5], columns=["Movie Title"])
        st.dataframe(df)

if __name__ == '__main__':
    main()





