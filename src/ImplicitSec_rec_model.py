from spotlight.cross_validation import user_based_train_test_split
from spotlight.datasets.movielens import get_movielens_dataset
from spotlight.sequence.implicit import ImplicitSequenceModel
from spotlight.interactions import Interactions
from spotlight.sequence.representations import CNNNet
from spotlight.evaluation import sequence_mrr_score
import numpy as np

def load_data_to_sequences(variant = '20M', 
                            max_sequence_length = 200,
                            min_sequence_length = 20,
                            step_size = 200):
    random_state = np.random.RandomState(100)
    dataset = get_movielens_dataset(variant=variant)
    train, test = user_based_train_test_split(dataset,
                                              random_state=random_state)
    train = train.to_sequence(max_sequence_length=max_sequence_length,
                              min_sequence_length=min_sequence_length,
                              step_size=step_size)
    test = test.to_sequence(max_sequence_length=max_sequence_length,
                            min_sequence_length=min_sequence_length,
                            step_size=step_size)
    
    return train, test

def train_ImplicitSec_model(train, model_type = 'cnn'):
    model = ImplicitSequenceModel(n_iter=3,
                                  representation=model_type,
                                  loss='bpr')
    model.fit(train)
    
    return model 

def evaluate_model(test, model): 
    mrr = sequence_mrr_score(model, test)
    print('MRR: ', mrr)
    
    return mrr