import glob
import os
import sys
from typing import Optional

import yaml

from elements.model import ModelConfig
from elements.utils import Logger

logger = Logger.setup_logger()


class ConfigParser:
    """
    Holds the logic to parse the config.yaml file consisting the settings for each model
    """
    def __init__(self, template: Optional[str] = None):
        self.base_path = getattr(sys, '_MEIPASS', os.path.abspath(os.path.dirname(__file__)))
        self.config_path = os.path.join(self.base_path, 'config.yaml')
        self.weight_extensions = ["ckpt", "pth", "pt"]
        self.all_configs: list[ModelConfig] = []
        self.trackers: list[str] = []
        self.task_type_models: dict[str, list[ModelConfig]] = {}
        self.template = template
        self.current_config: Optional[ModelConfig] = None

        self.initialize()

    def initialize(self) -> None:
        """
        Initialize the configuration by loading weights and validating against the config file.
        """
        try:
            config_file = self.read_config_content()
            weight_files = self._assemble_weights_list()
            self._assemble_tracker_list()

            for weight_file in weight_files:
                model_config = self._process_weight_file(weight_file, config_file)
                if model_config:
                    self.all_configs.append(model_config)

            if self.template is not None:
                self.current_config = self.get_current_config()


        except Exception as e:
            logger.exception(f"Failed to initialize ConfigParser: {e}")

    def update_current_config(self, architecture: str, weights: str) -> None:
        """
        Update the current config with the new config.
        """
        self.current_config = self.get_current_config(architecture=architecture, weights=weights)

    def _assemble_tracker_list(self) -> None:
        """
        Fill the tracker list against the config file.
        """
        try:
            config_file = self.read_config_content()

            for tracker in config_file["trackers"]:
                self.trackers.append(tracker)

        except Exception as e:
            logger.exception(f"Failed to initialize ConfigParser: {e}")

    def _process_weight_file(self, weight_file: str, config_file: dict) -> Optional[ModelConfig]:
        """
        Process an individual weight file and return a valid ModelConfig object if applicable.
        """
        if "models" not in weight_file:
            return None

        architecture = os.path.normpath(weight_file).split(os.sep)[-2]
        weights = os.path.basename(weight_file)

        if architecture not in config_file:
            logger.warning(f"Model {architecture} not found in the config file.")
            return None

        model_config_data = config_file.get(architecture, {})
        model_config = ModelConfig(architecture=architecture, weights=weights)

        # Set model properties
        model_config.input_width = model_config_data.get("input_width")
        model_config.input_height = model_config_data.get("input_height")
        model_config.task_type = model_config_data.get("task_type")
        model_config.version = model_config_data.get("version")
        model_config.normalize_type = model_config_data.get("normalize_type")
        self._add_to_list_in_dict(dictionary=self.task_type_models, key=model_config.task_type, value=model_config)

        model_config.classes = model_config_data.get("weights").get(weights).get("classes", [])
        model_config.tracked_classes = model_config_data.get("weights").get(weights).get("tracked_classes", [])
        model_config.showed_classes = model_config_data.get("weights").get(weights).get("showed_classes", [])
        model_config.load_model_type = model_config_data.get("load_model_type")
        model_config.box_threshold = model_config_data.get("box_threshold")

        return model_config

    def get_trackers(self) -> list[str]:
        """
        Getter for the tracker list
        """
        return self.trackers

    def get_current_config(self, architecture: Optional[str] = None, weights: Optional[str] = None) -> Optional[ModelConfig]:
        """
        Get the current ModelConfig based on a template.
        """
        try:
            config_file = self.read_config_content()
            if architecture is None or weights is None:
                template_config = config_file.get("templates", {}).get(self.template, {})
                weights = template_config.get("weights")
                architecture = template_config.get("architecture")

            tracker = config_file.get(architecture, {}).get("tracker")

            for config in self.all_configs:
                if config.weights == weights and config.architecture == architecture:
                    config.tracker = tracker
                    return config

            logger.warning(f"Template '{self.template}' not found in configurations.")
        except Exception as e:
            logger.exception(f"Error retrieving current config for template '{self.template}': {e}")
        return None

    def get_all_configs(self) -> list[ModelConfig]:
        return self.all_configs

    def get_task_type_models(self) -> dict[str, list[ModelConfig]]:
        return self.task_type_models

    def read_config_content(self) -> dict:
        """
         Read and parse the YAML configuration file.
         """
        try:
            with open(self.config_path, "r") as file:
                return yaml.safe_load(file)
        except FileNotFoundError:
            logger.error(f"Config file not found: {self.config_path}")
            raise
        except yaml.YAMLError as e:
            logger.error(f"Error parsing YAML file: {e}")
            raise

    def _add_to_list_in_dict(self, dictionary: dict, key: str, value: ModelConfig) -> None:
        """
        Add a value to a list in a dictionary. Create the list if it doesn't exist.
        """
        dictionary.setdefault(key, []).append(value)

    def _assemble_weights_list(self) -> list[str]:
        """
        Gather all weight files matching the specified extensions.
        """
        weight_files = []
        for extension in self.weight_extensions:
            weight_files.extend(glob.glob(f"models/**/*.{extension}", recursive=True))
        return weight_files
