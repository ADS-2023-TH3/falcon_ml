import pickle
from popular_rec_model import *

# Train the model and store it
# Get data
df = get_merge_data()
# Train the model
model = TopPopRecommender()
model.fit(df)
# Store it
with open('../trained_models/popular_rec_model.pkl', 'wb') as file:
    pickle.dump(model, file)