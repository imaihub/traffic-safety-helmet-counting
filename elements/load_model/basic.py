import os
from typing import Any

import torch

from elements.utils import Logger

logger = Logger.setup_logger()


def dynamic_load_weights_pt(model: torch.nn.Module, weights: dict) -> None:
    """
    Dynamically loads weights into a PyTorch model, handling potential mismatches in layer sizes. Provides verbose feedback on any mismatched layers and skips only those layers while keeping the rest intact.

    :param model: The PyTorch model into which the weights are being loaded.
    :param weights: A dictionary containing the model weights, typically loaded from a checkpoint or pre-trained model.

    """
    # Get the current model's state dictionary
    current_model_dict = model.state_dict()

    # Track mismatched layers
    mismatched_layers = []

    # Dry run: attempt loading weights with strict=True to identify mismatches
    try:
        model.load_state_dict(weights, strict=True)
        print("All weights successfully loaded with strict=True.")
        return
    except RuntimeError as e:
        print("Identifying mismatched layers...")
        error_message = str(e)
        lines = error_message.split('\n')
        for line in lines:
            if "size mismatch" in line:
                mismatched_layer = line.split("size mismatch for ")[1].split(":")[0]
                mismatched_layers.append(mismatched_layer)

    # Log mismatched layers
    if mismatched_layers:
        print("The following layers have size mismatches and will be skipped:")
        for layer in mismatched_layers:
            print(f"- {layer}")

    # Remove mismatched layers from weights and reload
    filtered_weights = {k: v if k not in mismatched_layers else current_model_dict[k] for k, v in weights.items()}
    model.load_state_dict(filtered_weights, strict=False)
    print("Model weights loaded with mismatched layers resolved.")


def load_model_pt(model: torch.nn.Module, path: str, strict: bool = True, force: bool = False) -> dict[str, Any]:
    """
    This method loads a model from path into the model object.

    :param model: A PyTorch model object with empty/random weights.
    :param path: Path to the model saved with :meth:~`elements.basic.save_model.save_model_pt`.
    :param strict: Ignores the weights for the head of the model if for example the num_classes don't match in the pretrained weights and the passed model
    :param force: If True handle potential mismatches by skipping incompatible layers while loading in the weights.

    :returns: The raw dictionary contents from path.

    """
    # Load the checkpoint data
    data = torch.load(path, map_location=torch.device('cpu'))

    # Ensure the checkpoint contains the required keys
    if 'model' not in data:
        logger.warning("The checkpoint file is missing the 'model' key.")
        model_weights = data
    else:
        model_weights = data['model']

    if 'type' not in data:
        logger.warning("The checkpoint file does not contain a 'type' key. Skipping type validation.")

    # Handle forced loading with dynamic mismatch resolution (https://stackoverflow.com/questions/67838192/size-mismatch-runtime-error-when-trying-to-load-a-pytorch-model)
    if force:
        dynamic_load_weights_pt(model, weights=data)
        logger.info(f"Loaded model with dynamic mismatch resolution from {os.path.abspath(path)}.")
    elif 'type' in data and not str(type(model)) == data['type']:
        # Validate model type if 'type' key exists
        logger.warning(f"The type in the file ({data['type']}) is different from the passed model ({type(model)}).")
        model.load_state_dict(model_weights, strict=strict)
        logger.info(f"Loaded model from {os.path.abspath(path)} with potential mismatches (strict={strict}).")
    else:
        # Normal weight loading
        model.load_state_dict(model_weights, strict=strict)
        logger.info(f"Loaded model from {os.path.abspath(path)} with strict={strict}.")

    return data
