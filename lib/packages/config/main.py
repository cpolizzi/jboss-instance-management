from box import Box
from jsonschema import validate
import os
import yaml

import paths


class Config:
    """
    Represents managed instance configuration et al. Responsible for persistence of the backing YAML file for
    the configuration.
    """
    def __init__(
            self,
            **entries,
    ):
        """
        Creates an instance from an existing dictionary such that dictionary keys are exposed as members.

        ### Arguments
        - entries
            - Object or other iterable dictionary to dynamical;y create instance level members for.
        """
        self.__dict__.update(entries)


    @staticmethod
    def schema() -> str:
        """
        Returns the absolute path to the configuration schema.

        ### Returns
        - Configuration schema path.
        """
        return f"{paths.Paths.schemas()}/config.schema.yaml"


    @staticmethod
    def config() -> str:
        """
        Returns the absolute path to the configuration.

        ### Returns
        - Configuration path.
        """
        return f"{paths.Paths.configs()}/config.yaml"


    @classmethod
    def load(cls):
        """
        Loads the configuration, validates it against the configuration schema and returns the result as a dynamic object.

        ### Returns
        - Configuration with its backing data populated.
        """
        result : Config = None

        # Load schema
        with open(Config.schema(), "r") as f:
            schema = yaml.safe_load(f)

        # Load configuration and validate against schema
        conf_data = {}
        try:
            with open(Config.config(), "r") as f:
                conf_data = yaml.safe_load(f)
            validate(conf_data, schema)
        except FileNotFoundError:
            # Config file does not exist
            conf_data = {
                "paths": {
                    "jboss": "/opt/jboss",
                    "instances": "/opt/app/jboss",
                    "run": "/var/run/jboss",
                },
                "defaults": {
                    "jboss": {
                        "profile": "standalone-full.xml",
                    },
                },
                "instances": [],
            }

        result = Config(**Box(conf_data))

        return result
    

    def save(
            self,
    ) -> None:
        """
        Saves the configuration.

        ### Returns
        - Nothing.
        """
        os.makedirs(os.path.dirname(Config.config()), exist_ok = True)
        Box(vars(self)).to_yaml(filename = self.config(), indent = 2, sort_keys = False, default_flow_style = False)
