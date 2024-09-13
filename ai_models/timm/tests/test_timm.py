import time

from django.test import TestCase
from timm import create_model, list_models, list_modules


class TimmModelsTest(TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()
        # Get list of modules and their respective models
        cls.models = {
            module: list(list_models(module=module))
            for module in list_modules()
        }
        cls.num_classes = 10

    def test_model_creation(self) -> None:
        num = 1
        # Iterate through each module and its models
        for module_name, model_list in self.models.items():
            print(f"Module: {module_name}")  # Display module name  # noqa: T201
            for model_name in model_list:
                with self.subTest(model=model_name):
                    print(  # noqa: T201
                        f"    Testing model: {model_name}"
                    )  # Display model name
                    try:
                        start_time = time.time()
                        # Attempt to create the model with pretrained weights
                        create_model(
                            model_name,
                            pretrained=True,
                            num_classes=self.num_classes,
                        )
                        print(  # noqa: T201
                            f"    {model_name} (pretrained=True) created in {time.time() - start_time:.4f} seconds"
                        )
                    except RuntimeError:
                        start_time = time.time()
                        # If pretrained fails, create the model without pretrained weights
                        create_model(
                            model_name,
                            pretrained=False,
                            num_classes=self.num_classes,
                        )
                        print(  # noqa: T201
                            f"    {model_name} (pretrained=False) created in {time.time() - start_time:.4f} seconds"
                        )
                    num += 1
