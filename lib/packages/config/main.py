from jsonschema import validate
from munch import DefaultMunch
import os
import yaml

import paths


class Config:
    def __init__(
            self,
    ):
        """
        Creates an instance.
        """
        self._config = {}


    @staticmethod
    def schema() -> str:
        """
        Returns the absolute path to the configuration schema.
        """
        return f"{paths.Paths.schemas()}/config.schema.yaml"


    @staticmethod
    def config() -> str:
        """
        Returns the absolute path to the configuration.
        """
        return f"{paths.Paths.configs()}/config.yaml"


    def load(
            self,
    ) -> DefaultMunch:
        """
        Loads the configuration, validates it against the configuration schema and returns the result as a dynamic object.
        """
        result = DefaultMunch()

        # Load schema
        with open(Config.schema(), "r") as f:
            schema = yaml.safe_load(f)

        # Load configuration and validate against schema
        try:
            with open(Config.config(), "r") as f:
                self._config = yaml.safe_load(f)
            validate(self._config, schema)
        except FileNotFoundError:
            pass

        # Convert loaded configuration document into an object
        result = DefaultMunch.fromDict(self._config)

        return result
    

    def save(
            self,
    ) -> None:
        """
        Saves the configuration.
        """
        os.makedirs(os.path.dirname(Config.config()), exist_ok = True)
        with open(Config.config() + ".1", "w") as f:
            yaml.dump(self._config, f, indent = 4, sort_keys = True, default_flow_style = False)
