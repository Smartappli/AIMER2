import time
from django.test import TestCase
from timm import list_modules, list_models, create_model


class TimmModelsTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.models = {i: list(list_models(module=i)) for i in list_modules()}
        cls.num_classes = 10

    def test_model_creation(self):
        num = 1
        for module, model_list in self.models.items():
            for model_name in model_list:
                with self.subTest(model=model_name):
                    try:
                        start_time = time.time()
                        create_model(
                            model_name,
                            pretrained=True,
                            num_classes=self.num_classes,
                        )
                        elapsed_time = time.time() - start_time
                        print(
                            f"{num}: {model_name} - ok (time: {elapsed_time:.3f} seconds)"
                        )
                    except RuntimeError as e:
                        start_time = time.time()
                        create_model(
                            model_name,
                            pretrained=False,
                            num_classes=self.num_classes,
                        )
                        elapsed_time = time.time() - start_time
                        print(
                            f"{num}: {model_name} - ok without pretrained (time: {elapsed_time:.3f} seconds)"
                        )
                    num += 1
