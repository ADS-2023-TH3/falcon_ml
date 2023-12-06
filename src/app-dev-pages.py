import streamlit as st
import pandas as pd
from popular_rec_model import *
from ImplicitSec_rec_model import *
import torch

from writing_functions import *


def display_movies(movies, ratings=None):
    # Display movies in a table with sliders for ratings using st.beta_columns
    for movie in movies:
        col1, col2 = st.columns(2)
        with col1:
            st.write(movie)
            if ratings is None:
                col11, col12 = st.columns(2)
                with col11:
                    replace = st.button("Replace suggestion", key=f"replace_{movie}")
                if replace:
                    if movie in st.session_state.recommendations:
                        st.session_state.to_remove = movie
                        #st.session_state.recommendations.remove(movie)
                    with col12:
                        confirm = st.button("Confirm", key=f"confirm_{movie}")
        with col2:
            if ratings is not None:
                rating = st.slider(f"Share your personal rating", 0, 5, int(ratings[movie]), key=f"rating_{movie}")
            else:
                rating = st.slider(f"Share your personal rating", 0, 5, 0, key=f"rating_{movie}")
            if rating > 0:
                st.session_state.ratings[movie] = rating

def user_ratings(username):
    feedback_worksheet = connect_to_sheet('feedback_sheet')
    feedback_users = feedback_worksheet.col_values(1)
    user_ratings_dict = {}
    if username in feedback_users:
        #index = feedback_users.index(username)
        indices = [i+1 for i, x in enumerate(feedback_users) if x == username]
        # Get the movies and ratings that the user has already rated
        movies = [feedback_worksheet.row_values(i)[1::2][0] for i in indices]
        ratings = [feedback_worksheet.row_values(i)[2::2][0] for i in indices]
        # Create a dictionary with the movies and ratings
        user_ratings_dict = dict(zip(movies, ratings))
        # Create a dictionary that keeps track of the indices of the movies
        user_ratings_dict_indices = dict(zip(movies, indices))

    return user_ratings_dict, user_ratings_dict_indices

import hashlib
def make_hashes(password):
	return hashlib.sha256(str.encode(password)).hexdigest()

def check_hashes(password,hashed_text):
	if make_hashes(password) == hashed_text:
		return True
	return False

def home():
    st.title("Home Page")
    st.title('Movie Recommender') 
        
    # Initialize session state
    if 'success' not in st.session_state:
        st.session_state.success = False

    # Login form
    # TODO: improve it with https://blog.jcharistech.com/2020/05/30/how-to-add-a-login-section-to-streamlit-blog-app/
    
    with st.form("login_form"):
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        submitted = st.form_submit_button("Login")

        if submitted:

            # Initialize session state
            st.session_state.requested_more_recommendations = 0
            st.session_state.recommendations = []
            st.session_state.more_recommendations = []
            st.session_state.ratings = {}
            st.session_state.to_remove = None

            # Connect to the users sheet
            users_worksheet = connect_to_sheet('users_sheet')
            users = users_worksheet.col_values(1)
            passwords = users_worksheet.col_values(2)

            if username in users:
                index = users.index(username)
                if check_hashes(password, passwords[index]):
                    # Check if the user has already rated some movies
                    st.session_state.user_ratings, st.session_state.user_ratings_indices = user_ratings(username)
                    st.session_state.username = username
                    # Display the welcome message
                    st.success("Logged in as {}".format(username))
                    st.session_state.success = True
                else: 
                    st.error("Incorrect username or password")
                    st.session_state.success = False
            else:
                st.error("Incorrect username or password")
                st.session_state.success = False

def about():
    st.title("About Page")
    # Your content for the about page

def contact():
    st.title("Contact Page")
    # Your content for the contact page

# Sidebar menu
menu_options = ["Home", "About", "Contact"]
selected_menu_option = st.sidebar.selectbox("Menu", menu_options)

# Display content based on the selected menu option
if selected_menu_option == "Home":
    home()
elif selected_menu_option == "About":
    about()
elif selected_menu_option == "Contact":
    contact()

