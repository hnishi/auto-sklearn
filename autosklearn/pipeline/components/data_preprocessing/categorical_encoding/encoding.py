from typing import Dict, Optional, Tuple, Union

import numpy as np

from ConfigSpace.configuration_space import ConfigurationSpace

import scipy.sparse

from sklearn.preprocessing import OrdinalEncoder

from autosklearn.pipeline.base import DATASET_PROPERTIES_TYPE, PIPELINE_DATA_DTYPE
from autosklearn.pipeline.components.base import AutoSklearnPreprocessingAlgorithm
from autosklearn.pipeline.constants import DENSE, SPARSE, UNSIGNED_DATA, INPUT


class OrdinalEncoding(AutoSklearnPreprocessingAlgorithm):
    def __init__(self,
                 random_state: Optional[np.random.RandomState] = None,
                 ):
        self.random_state = random_state

    def fit(self, X: PIPELINE_DATA_DTYPE,
            y: Optional[PIPELINE_DATA_DTYPE] = None) -> 'OrdinalEncoding':
        if not scipy.sparse.issparse(X):
            self.preprocessor = OrdinalEncoder(
                categories='auto', handle_unknown='use_encoded_value', unknown_value=-1,
            )
            self.preprocessor.fit(X, y)
        return self

    def transform(self, X: PIPELINE_DATA_DTYPE) -> PIPELINE_DATA_DTYPE:
        if scipy.sparse.issparse(X):
            # Sparse data should be float dtype, which means we do not need
            # to further encode it.
            return X
        if self.preprocessor is None:
            raise NotImplementedError()
        # Notice we are shifting the unseen categories during fit to 1
        # from -1, 0, ... to 0,..., cat + 1
        # This is done because Category shift requires non negative integers
        # Consider removing this if that step is removed
        return self.preprocessor.transform(X) + 1

    @staticmethod
    def get_properties(dataset_properties: Optional[DATASET_PROPERTIES_TYPE] = None
                       ) -> Dict[str, Optional[Union[str, int, bool, Tuple]]]:
        return {'shortname': 'OrdinalEncoder',
                'name': 'Ordinal Encoder',
                'handles_regression': True,
                'handles_classification': True,
                'handles_multiclass': True,
                'handles_multilabel': True,
                'handles_multioutput': True,
                # TODO find out of this is right!
                'handles_sparse': True,
                'handles_dense': True,
                'input': (DENSE, SPARSE, UNSIGNED_DATA),
                'output': (INPUT,), }

    @staticmethod
    def get_hyperparameter_search_space(
        dataset_properties: Optional[DATASET_PROPERTIES_TYPE] = None,
    ) -> ConfigurationSpace:
        return ConfigurationSpace()
