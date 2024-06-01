import sys
import os

import paths

class Config:
    def schema() -> str:
        """
        Returns the absolute path to the configuration schema.
        """
        return f"{paths.Paths.schemas()}/config.schema.yaml"

    def config() -> str:
        """
        Returns the absolute path to the configuration.
        """
        return f"{paths.Paths.configs()}/config.yaml"
