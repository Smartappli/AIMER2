import os
import time

from keras import applications

os.environ["KERAS_BACKEND"] = "tensorflow"

keras_models = [m for m in dir(applications) if m[0].isupper()]
total = len(keras_models)

# Test the initialization of each model
for model_name in keras_models:
    try:
        # Dynamically get the model class from keras.applications
        model_class = getattr(applications, model_name)

        # Initialize the model (some models might require specific arguments)
        start_time = time.time()
        model_instance = model_class(
            weights=None,
        )  # Initialize without pre-trained weights
        elapsed_time = time.time() - start_time
    except Exception:
        pass
