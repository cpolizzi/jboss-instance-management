import sys
import os


class PathUtil:
    def locality_path():
        """
        Returns the absolute path where Locality is installed.
        """
        return os.path.realpath(os.path.dirname(os.path.abspath(os.path.dirname(sys.argv[0]))))

    def common_services_path():
        """
        Returns the absolute path to Locality's common services file.
        """
        return PathUtil.locality_path() + "/docker-compose.yaml"

    def libexec_path():
        """
        Returns the absolute path to Locality's libexec.
        """
        return PathUtil.locality_path() + "/libexec/bin"

    def resources_path():
        """
        Returns the absolute path to Locality's resources.
        """
        return PathUtil.locality_path() + "/resources"


    def main_config_path():
        """
        Returns the absolute path to Locality's main configuration.
        """
        return PathUtil.resources_path() + "/config.json"


    def config_path():
        """
        Returns the aboslute path to Locality's configuration path.
        """
        return f"{os.environ['HOME']}/.config/locality"

    def meta_path():
        """
        Returns the absoluite path to Locality's meta information file
        """
        return PathUtil.config_path() + "/meta.json"

    def storage_path():
        """
        Returns the absolute path to Locality's storage configuration file
        """
        return PathUtil.config_path() + "/storage.json"
