import pandas as pd
from spotlight.datasets.movielens import get_movielens_dataset
def add_feedback_to_retrain(username):
    """
    Adds user feedback to the MovieLens dataset for retraining purposes.

    Parameters:
    - username (str): The username for which feedback should be added.

    Returns:
    - final_df (pd.DataFrame): The updated DataFrame containing MovieLens dataset
      with additional feedback from the specified user. Ready to re-training.
    """

    # read movie lens dataset
    dataset = get_movielens_dataset(variant='20M')
    item_ids = dataset.item_ids
    ratings = dataset.ratings
    df = pd.DataFrame({'item_ids':item_ids,'ratings':ratings})

    # read feedback dataset
    feedback = pd.read_csv('../Data/fake_feedback.csv')

    # read dataset with title, item_ids and genre
    complete_df = pd.read_csv('../Data/movies.csv')

    # Select title of username (e.g. username= 'admin1')
    filtered_df = feedback[feedback['Users'] == username]
    titles_list = filtered_df['title'].tolist()

    # Select item_ids and include ratings of the selected username
    titles_df = pd.DataFrame({'title': titles_list})
    result_df = pd.merge(titles_df, complete_df, on='title', how='left')
    input_movies_ids = result_df['item_ids'].values
    input_movies_ids = pd.DataFrame(input_movies_ids, columns=['item_ids'])
    input_movies_ids['ratings'] = filtered_df['ratings'].tolist()

    # Concatenate feedback to dataframe
    final_df = pd.concat([df, input_movies_ids], ignore_index=True)

    return final_df

