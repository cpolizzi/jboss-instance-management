import sys
import os


class Paths:
    _home : str = ""

    def home(path : str = "") -> str:
        if not Paths._home:
            Paths._home = path
        return Paths._home

    def configs() -> str:
        """
        Returns the absolute path to configuration resources.
        """
        return f"{Paths.resources()}/config"

    def resources() -> str:
        """
        Returns the absolute path to resources.
        """
        return f"{Paths.home()}/resources"

    def schemas() -> str:
        """
        Returns the absolute path to schema resources.
        """
        return f"{Paths.resources()}/schema"
