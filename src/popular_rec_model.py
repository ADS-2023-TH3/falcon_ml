# Requiered imports

from spotlight.datasets.movielens import get_movielens_dataset
import pandas as pd

def get_merge_data():
    # Download the dataset movielens from spotlight
    dataset = get_movielens_dataset(variant='20M')
    item_ids = dataset.item_ids
    ratings = dataset.ratings
    df = pd.DataFrame({'item_ids':item_ids,'ratings':ratings})

    # Download movielens dataset to add genres
    genres_df = pd.read_csv('../Data/movies.csv')
    genres_df = genres_df.rename(columns={'movieId': 'item_ids'})

    # Merge dataframes by item_ids
    df = pd.merge(df,genres_df,on='item_ids')
    return df


class TopPopRecommender:

    def fit(self, train):
        item_popularity = train[['item_ids', 'ratings']].groupby(by='item_ids').count()
        self.train = train
        self.popular_items = item_popularity.sort_values(by='ratings', ascending=False).index

    def recommend(self, at=5, genre=None):
        if genre is not None:
            # Filter the train dataset by the specified genre
            genre_items = self.train[self.train['genres'].str.contains(genre)]
            # Group by 'item_ids' and count ratings
            genre_item_popularity = genre_items[['item_ids', 'ratings']].groupby(by='item_ids').count()
            # Sort by popularity
            genre_popular_items = genre_item_popularity.sort_values(by='ratings', ascending=False).index
            # Take the top 'at' items
            recommended_items = genre_popular_items[0:at]
        else:
            # If no genre is specified, return the top 'at' popular items across all genres
            recommended_items = self.popular_items[0:at]

        return recommended_items
