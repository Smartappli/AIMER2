import time
from django.test import TestCase
from pycaret.classification import (
    get_all_models as get_classification_models,
    setup as setup_classification,
)
from pycaret.regression import (
    get_all_models as get_regression_models,
    setup as setup_regression,
)
from pycaret.clustering import (
    get_all_models as get_clustering_models,
    setup as setup_clustering,
)
from pycaret.anomaly import (
    get_all_models as get_anomaly_models,
    setup as setup_anomaly,
)
from pycaret.datasets import get_data


class PyCaretModelsTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Load sample datasets
        cls.classification_data = get_data("iris")
        cls.regression_data = get_data("boston")
        cls.clustering_data = get_data("jewellery")
        cls.anomaly_data = get_data("anomaly")

    def test_classification_models(self):
        setup_classification(
            self.classification_data, target="species", silent=True, html=False
        )
        models = get_classification_models()
        for model in models:
            with self.subTest(model=model):
                start_time = time.time()
                self.assertIsNotNone(model)
                end_time = time.time()
                execution_time = end_time - start_time
                print(
                    f"Classification model {model} executed in {execution_time:.4f} seconds"
                )

    def test_regression_models(self):
        setup_regression(
            self.regression_data, target="medv", silent=True, html=False
        )
        models = get_regression_models()
        for model in models:
            with self.subTest(model=model):
                start_time = time.time()
                self.assertIsNotNone(model)
                end_time = time.time()
                execution_time = end_time - start_time
                print(
                    f"Regression model {model} executed in {execution_time:.4f} seconds"
                )

    def test_clustering_models(self):
        setup_clustering(self.clustering_data, silent=True, html=False)
        models = get_clustering_models()
        for model in models:
            with self.subTest(model=model):
                start_time = time.time()
                self.assertIsNotNone(model)
                end_time = time.time()
                execution_time = end_time - start_time
                print(
                    f"Clustering model {model} executed in {execution_time:.4f} seconds"
                )

    def test_anomaly_models(self):
        setup_anomaly(self.anomaly_data, silent=True, html=False)
        models = get_anomaly_models()
        for model in models:
            with self.subTest(model=model):
                start_time = time.time()
                self.assertIsNotNone(model)
                end_time = time.time()
                execution_time = end_time - start_time
                print(
                    f"Anomaly detection model {model} executed in {execution_time:.4f} seconds"
                )


if __name__ == "__main__":
    unittest.main()
