import time

import torch
from django.test import TestCase
from torchvision.models import get_model, list_models


class TorchvisionModelsTest(TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()
        cls.all_models = list_models()

    def test_list_models_returns_list(self):
        """Test if list_models() returns a list."""
        assert isinstance(  # noqa: S101
            self.all_models, list
        ), "list_models() should return a list"

    def test_list_models_not_empty(self):
        """Test if list_models() returns a non-empty list."""
        assert (  # noqa: S101
            len(self.all_models) > 0
        ), "list_models() should not return an empty list"

    def test_known_model_in_list(self):
        """Test if a known model is included in the list."""
        known_model = "resnet50"  # Example of a known model
        assert (  # noqa: S101
            known_model in self.all_models
        ), f"{known_model} should be in the list of models"

    def test_unique_model_names(self):
        """Test if all model names in the list are unique."""
        assert len(self.all_models) == len(  # noqa: S101
            set(self.all_models)
        ), "Model names should be unique"

    def test_model_creation(self):
        """Test if each model in the list can be created."""
        for model_name in self.all_models:
            with self.subTest(model=model_name):
                try:
                    print(f"Creating model: {model_name}")  # noqa: T201
                    # Start timing
                    start_time = time.time()

                    # Create the model
                    model = get_model(model_name, pretrained=False)

                    # Test forward pass with a dummy input
                    dummy_input = torch.randn(1, 3, 224, 224)
                    model.eval()
                    with torch.no_grad():
                        output = model(dummy_input)

                    # Calculate and print the elapsed time
                    elapsed_time = time.time() - start_time

                    # Check if the output is not None
                    assert (  # noqa: S101
                        output is not None
                    ), f"Model {model_name} failed to return output"

                    print(  # noqa: T201
                        f"Model {model_name} created successfully in {elapsed_time:.2f} seconds"
                    )

                except Exception as e:
                    self.fail(
                        f"Model {model_name} creation failed with error: {e}"
                    )
