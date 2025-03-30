import typing
from collections import OrderedDict
from typing import Callable, Type, Union

import numpy as np
import pandas as pd
import torch
from river import base
from river.base.typing import FeatureName, RegTarget
from sortedcontainers import SortedSet

from deep_river.base import DeepEstimator, DeepEstimatorInitialized
from deep_river.utils import dict2tensor, float2tensor


class _TestModule(torch.nn.Module):
    def __init__(self, n_features, n_outputs):
        super().__init__()
        self.n_features = n_features
        self.n_outputs = n_outputs
        self.dense0 = torch.nn.Linear(n_features, n_outputs)

    def forward(self, X, **kwargs):
        return self.dense0(X)


class MultiTargetRegressor(base.MultiTargetRegressor, DeepEstimator):
    """A Regressor that supports multiple targets.

    Parameters
    ----------
    module
        Torch Module that builds the autoencoder to be wrapped.
        The Module should accept parameter `n_features` so that the
        returned model's input shape can be determined based on the number
        of features in the initial training example.
    loss_fn
        Loss function to be used for training the wrapped model.
        Can be a loss function provided by `torch.nn.functional` or one of
        the following: 'mse', 'l1', 'cross_entropy', 'binary_crossentropy',
        'smooth_l1', 'kl_div'.
    optimizer_fn
        Optimizer to be used for training the wrapped model.
        Can be an optimizer class provided by `torch.optim` or one of the
        following: "adam", "adam_w", "sgd", "rmsprop", "lbfgs".
    lr
        Learning rate of the optimizer.
    device
        Device to run the wrapped model on. Can be "cpu" or "gpu".
    seed
        Random seed for the wrapped model.
    **kwargs
        Parameters to be passed to the `Module` or the `optimizer`.

    Examples
    --------
    >>> from river import evaluate, compose
    >>> from river import metrics
    >>> from river import preprocessing
    >>> from river import stream
    >>> from sklearn import datasets
    >>> from torch import nn
    >>> from deep_river.regression.multioutput import MultiTargetRegressor

    >>> class MyModule(nn.Module):
    ...     def __init__(self, n_features):
    ...         super(MyModule, self).__init__()
    ...         self.dense0 = nn.Linear(n_features,3)
    ...
    ...     def forward(self, X, **kwargs):
    ...         X = self.dense0(X)
    ...         return X

    >>> dataset = stream.iter_sklearn_dataset(
    ...         dataset=datasets.load_linnerud(),
    ...         shuffle=True,
    ...         seed=42
    ...     )
    >>> model = compose.Pipeline(
    ...     preprocessing.StandardScaler(),
    ...     MultiTargetRegressor(
    ...         module=MyModule,
    ...         loss_fn='mse',
    ...         lr=0.3,
    ...         optimizer_fn='sgd',
    ...     ))
    >>> metric = metrics.multioutput.MicroAverage(metrics.MAE())
    >>> ev = evaluate.progressive_val_score(dataset, model, metric)
    >>> print(f"MicroAverage(MAE): {metric.get():.2f}")
    MicroAverage(MAE): 34.31

    """

    def __init__(
        self,
        module: Type[torch.nn.Module],
        loss_fn: Union[str, Callable] = "mse",
        optimizer_fn: Union[str, Callable] = "sgd",
        lr: float = 1e-3,
        device: str = "cpu",
        seed: int = 42,
        **kwargs,
    ):
        super().__init__(
            module=module,
            loss_fn=loss_fn,
            device=device,
            optimizer_fn=optimizer_fn,
            lr=lr,
            seed=seed,
            **kwargs,
        )
        self.observed_targets: OrderedDict[FeatureName, RegTarget] = OrderedDict()

    @classmethod
    def _unit_test_params(cls):
        """
        Returns a dictionary of parameters to be used for unit
        testing the respective class.

        Yields
        -------
        dict
            Dictionary of parameters to be used for unit testing the
            respective class.
        """

        yield {
            "module": _TestModule,
            "loss_fn": "l1",
            "optimizer_fn": "sgd",
        }

    @classmethod
    def _unit_test_skips(cls) -> set:
        """
        Indicates which checks to skip during unit testing.
        Most estimators pass the full test suite.
        However, in some cases, some estimators might not
        be able to pass certain checks.
        Returns
        -------
        set
            Set of checks to skip during unit testing.
        """
        return {
            "check_shuffle_features_no_impact",
            "check_emerging_features",
            "check_disappearing_features",
            "check_predict_proba_one",
            "check_predict_proba_one_binary",
            "check_learn_one",
            "check_pickling",
        }

    def _learn(self, x: torch.Tensor, y: torch.Tensor):
        self.module.train()
        self.optimizer.zero_grad()
        y_pred = self.module(x)
        loss = self.loss_func(y_pred, y)
        loss.backward()
        self.optimizer.step()

    def learn_one(
        self,
        x: dict,
        y: dict[FeatureName, RegTarget],
        **kwargs,
    ) -> None:
        if not self.module_initialized:
            self._update_observed_features(x)
            self.initialize_module(x=x, **self.kwargs)
        x_t = dict2tensor(x, SortedSet(x.keys()), device=self.device)
        self.observed_targets.update(y) if y is not None else None
        y_t = float2tensor(y, self.device)
        self._learn(x_t, y_t)

    def predict_one(self, x: dict) -> typing.Dict[FeatureName, RegTarget]:
        """
        Predicts the target value for a single example.

        Parameters
        ----------
        x
            Input example.

        Returns
        -------
        RegTarget
            Predicted target value.
        """
        if not self.module_initialized:
            self._update_observed_features(x)
            self.initialize_module(x=x, **self.kwargs)
        x_t = dict2tensor(x, SortedSet(x.keys()), device=self.device)
        self.module.eval()
        with torch.inference_mode():
            y_pred_t = self.module(x_t).squeeze().tolist()
            y_pred = {t: y_pred_t[i] for i, t in enumerate(self.observed_targets)}
        return y_pred


class MultiTargetRegressorInitialized(
    base.MultiTargetRegressor, DeepEstimatorInitialized
):
    """ """

    def __init__(
        self,
        module: torch.nn.Module,
        loss_fn: Union[str, Callable] = "mse",
        optimizer_fn: Union[str, Callable] = "sgd",
        is_feature_incremental: bool = False,
        is_target_incremental: bool = False,
        lr: float = 1e-3,
        device: str = "cpu",
        seed: int = 42,
        **kwargs,
    ):
        super().__init__(
            module=module,
            loss_fn=loss_fn,
            optimizer_fn=optimizer_fn,
            lr=lr,
            device=device,
            seed=seed,
            is_feature_incremental=is_feature_incremental,
            **kwargs,
        )
        self.is_target_incremental = is_target_incremental
        self.observed_targets: SortedSet = SortedSet()

    @classmethod
    def _unit_test_params(cls):
        """
        Returns a dictionary of parameters to be used for unit
        testing the respective class.

        Yields
        -------
        dict
            Dictionary of parameters to be used for unit testing the
            respective class.
        """

        yield {
            "module": _TestModule(10, 3),
            "loss_fn": "l1",
            "optimizer_fn": "sgd",
            "is_feature_incremental": True,
            "is_target_incremental": True,
        }

    @classmethod
    def _unit_test_skips(cls) -> set:
        return {
            "check_shuffle_features_no_impact",
        }

    def learn_one(self, x: dict, y: dict[FeatureName, RegTarget], **kwargs) -> None:
        """Learns from a single example."""
        self._update_observed_features(x)
        self._update_observed_targets(y)
        x_t = self._dict2tensor(x)
        self._learn(x_t, y)

    def learn_many(self, X: pd.DataFrame, y: pd.Series) -> None:
        """Learns from a batch of examples."""
        self._update_observed_features(X)

        x_t = self._df2tensor(X)
        self._learn(x_t, y)

    def _update_observed_targets(self, y) -> bool:
        """
        Updates observed classes dynamically if new classes appear.
        Expands the output layer if is_class_incremental is True.
        """
        if isinstance(y, (base.typing.ClfTarget, np.bool_)):  # type: ignore[arg-type]
            self.observed_targets.update(y)
        else:
            self.observed_targets.update(y)

        if (self.is_target_incremental and self.output_layer) and len(
            self.observed_targets
        ) > self._get_output_size():
            self._expand_layer(
                self.output_layer,
                target_size=max(len(self.observed_targets), self._get_output_size()),
                output=True,
            )
            return True
        return False

    def predict_one(self, x: dict) -> typing.Dict[FeatureName, RegTarget]:
        """
        Predicts the target value for a single example.
        """

        self._update_observed_features(x)
        x_t = self._dict2tensor(x)
        self.module.eval()
        with torch.inference_mode():
            y_pred_t = self.module(x_t).squeeze().tolist()
            y_pred = {t: y_pred_t[i] for i, t in enumerate(self.observed_targets)}
        return y_pred
