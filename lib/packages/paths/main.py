import sys
import os


class Paths:
    """
    Helper to provide location of critical paths in a relocatable manner.
    """
    _home : str = ""

    def home(path : str = "") -> str:
        """
        Returns the root path where this tool resides thereby removing any need for tbis tool to be installed in a specific
        location. This behaves in a singleton pattern.

        ### Arguments
        - path : str
            - Root path; subsequent invocations of this method with different paths will be ignored.

        ### Returns
        - Root path as provided by the first provided value.
        """
        if not Paths._home:
            Paths._home = path
        return Paths._home

    def configs() -> str:
        """
        Returns the absolute path to configuration resources.

        ### Returns
        - Path to configuration resources.
        """
        return f"{Paths.resources()}/config"

    def resources() -> str:
        """
        Returns the absolute path to resources.

        ### Returns
        - Path to configuration resources.
        """
        return f"{Paths.home()}/resources"

    def schemas() -> str:
        """
        Returns the absolute path to schema resources.

        ### Returns
        - Patn to schema resources.
        """
        return f"{Paths.resources()}/schema"
