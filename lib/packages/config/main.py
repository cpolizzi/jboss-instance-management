from box import Box
from jsonschema import validate
import os
import yaml

import paths


# TODO Add to `.paths.pids` for the directory in which PID files should be stored (we need runtime status)

# TODO Add JVM properties per instance
class Config:
    def __init__(
            self,
            **entries,
    ):
        """
        Creates an instance.
        """
        self.__dict__.update(entries)


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


    @classmethod
    def load(cls):
        """
        Loads the configuration, validates it against the configuration schema and returns the result as a dynamic object.
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
        """
        os.makedirs(os.path.dirname(Config.config()), exist_ok = True)
        Box(vars(self)).to_yaml(filename = self.config(), indent = 4, sort_keys = False, default_flow_style = False)
