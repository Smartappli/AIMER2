from django.test import TestCase
from timm import create_model, list_models, list_modules


class TimmModelsTest(TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()
        cls.models = {i: list(list_models(module=i)) for i in list_modules()}
        cls.num_classes = 10

    def test_model_creation(self) -> None:
        num = 1
        for model_list in self.models.values():
            for model_name in model_list:
                with self.subTest(model=model_name):
                    try:
                        start_time = time.time()
                        create_model(
                            model_name,
                            pretrained=True,
                            num_classes=self.num_classes,
                        )
                        time.time() - start_time
                    except RuntimeError:
                        start_time = time.time()
                        create_model(
                            model_name,
                            pretrained=False,
                            num_classes=self.num_classes,
                        )
                        time.time() - start_time
                    num += 1
