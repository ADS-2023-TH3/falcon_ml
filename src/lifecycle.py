from spotlight.cross_validation import user_based_train_test_split
from spotlight.datasets.movielens import get_movielens_dataset
from spotlight.sequence.implicit import ImplicitSequenceModel
from spotlight.interactions import Interactions
from spotlight.sequence.representations import CNNNet
from spotlight.evaluation import sequence_mrr_score
import numpy as np
import torch  # to save the model. Backbone done in torch.
import pandas as pd
import mlflow


def load_data_to_sequences(variant='20M',
                           max_sequence_length=200,
                           min_sequence_length=20,
                           step_size=200, df_split=False):
    """This functions loads the movielens dataset from the spotlight package

    Parameters:
        variant (str) : Parameter specifying the desired variant of the movielens
                        dataset. '20M' by default.
                        Possible variant inputs: '100K','1M','10M','20M'
        max_sequence_length (int) = 200 by default.
        min_sequence_length (int) = 20 by default.
        step_size (int) = 200 by default.
        df_split (boolean): False by default. Determines whether the train/test split is conducted
    Returns:
        train (sequence)
        test (sequence)

    """
    random_state = np.random.RandomState(100)
    dataset = get_movielens_dataset(variant=variant)
    if df_split:
        train, test = user_based_train_test_split(dataset,
                                                  random_state=random_state)
        train = train.to_sequence(max_sequence_length=max_sequence_length,
                                  min_sequence_length=min_sequence_length,
                                  step_size=step_size)
        test = test.to_sequence(max_sequence_length=max_sequence_length,
                                min_sequence_length=min_sequence_length,
                                step_size=step_size)

        return train, test

    else:
        dataset = dataset.to_sequence(max_sequence_length=max_sequence_length,
                                      min_sequence_length=min_sequence_length,
                                      step_size=step_size)
        return dataset


def train_ImplicitSec_model(train, model_type='cnn', save_model=True, n_iter=3, loss_type='bpr'):
    """Function that trains and saves the recommender model ImplicitSequenceModel()

    Args:
        train (sequence): sequence data ready to train using the ImplicitSequenceModel()
        model_type (str, optional): Sequence representation to use by the ImplicitSequenceModel.
                                    Default to 'cnn'.
                                    Possible inputs: 'cnn', 'pooling' or 'lstm'
        save_model (boolean): Default to 'True', determins whether or not to save the model.

    Returns:
        model (spotlight.sequence.implicit.ImplicitSequenceModel): trained model
    """
    model = ImplicitSequenceModel(n_iter=n_iter,
                                  representation=model_type,
                                  loss=loss_type)
    model.fit(train)

    return model, model_type, n_iter, loss_type


def evaluate_model(test, model):
    """evaluates the trained model by computing the mrr metrics

    Args:
        test (sequence): _description_
        model (spotlight.sequence.implicit.ImplicitSequenceModel): _description_

    Returns:
        mrr (np.array): mrr metrics
    """
    mrr = sequence_mrr_score(model, test)
    print('MRR: ', mrr)

    return mrr


# Mlflow run
with mlflow.start_run():
    # Load data
    train = load_data_to_sequences()

    # Train model
    model, model_type, n_iter, loss_type = train_ImplicitSec_model(train, model_type='cnn', save_model=True, n_iter=3, loss_type='bpr')

    # Evaluate model
    #mrr = evaluate_model(test, model)

    # Log parameters
    mlflow.log_param("model_type", model_type)
    mlflow.log_param("n_iter", n_iter)
    mlflow.log_param("loss_type", loss_type)

    # Log metrics
    #mlflow.log_metric("mrr", mrr)

    # Log artifacts (output files)
    #mlflow.pytorch.log_model(model, "models")