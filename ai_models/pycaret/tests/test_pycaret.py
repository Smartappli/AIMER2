import time

from django.test import TestCase
from pycaret.anomaly import models as get_anomaly_models
from pycaret.anomaly import setup as setup_anomaly
from pycaret.classification import models as get_classification_models
from pycaret.classification import setup as setup_classification
from pycaret.clustering import models as get_clustering_models
from pycaret.clustering import setup as setup_clustering
from pycaret.datasets import get_data
from pycaret.regression import models as get_regression_models
from pycaret.regression import setup as setup_regression


class PyCaretModelsTestCase(TestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        # Load sample datasets
        cls.classification_data = get_data("iris")
        cls.regression_data = get_data("boston")
        cls.clustering_data = get_data("jewellery")
        cls.anomaly_data = get_data("anomaly")

    def test_classification_models(self) -> None:
        setup_classification(
            self.classification_data,
            target="species",
            silent=True,
            html=False,
        )
        models = get_classification_models()
        for model in models:
            with self.subTest(model=model):
                start_time = time.time()
                assert model is not None  # noqa: S101
                time.time() - start_time

    def test_regression_models(self) -> None:
        setup_regression(
            self.regression_data,
            target="medv",
            silent=True,
            html=False,
        )
        models = get_regression_models()
        for model in models:
            with self.subTest(model=model):
                start_time = time.time()
                assert model is not None  # noqa: S101
                time.time() - start_time

    def test_clustering_models(self) -> None:
        setup_clustering(self.clustering_data, silent=True, html=False)
        models = get_clustering_models()
        for model in models:
            with self.subTest(model=model):
                start_time = time.time()
                assert model is not None  # noqa: S101
                time.time() - start_time

    def test_anomaly_models(self) -> None:
        setup_anomaly(self.anomaly_data, silent=True, html=False)
        models = get_anomaly_models()
        for model in models:
            with self.subTest(model=model):
                start_time = time.time()
                assert model is not None  # noqa: S101
                time.time() - start_time
