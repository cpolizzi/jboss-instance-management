import enum

__version__ = "0.0.1"

from .main import Properties as Properties
class OutputFormat(enum.Enum):
    """
    CLI output formats.
    """
    JSON = "json"
    TABLE = "table"
    TEXT = "text"
    YAML = "yaml"
