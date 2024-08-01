import os
import time

import keras
from keras import applications

os.environ["KERAS_BACKEND"] = "tensorflow"

print(keras.__version__)
keras_models = [m for m in dir(applications) if m[0].isupper()]
total = len(keras_models)

# Test the initialization of each model
for model_name in keras_models:
    try:
        # Dynamically get the model class from keras.applications
        model_class = getattr(applications, model_name)

        # Initialize the model (some models might require specific arguments)
        print(f"Testing model: {model_name}")
        start_time = time.time()
        model_instance = model_class(
            weights=None
        )  # Initialize without pre-trained weights
        elapsed_time = time.time() - start_time
        print(
            f"{model_name} initialized successfully (time: {elapsed_time:.3f} seconds).\n"
        )
    except Exception as e:
        print(f"Error initializing {model_name}: {e}\n")
