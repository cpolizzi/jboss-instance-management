from enum import Enum


class Properties:
    """
    Support to compose Java properties composition.
    """
    _properties : dict

    class ComposeForm(Enum):
        """
        Output form that properties should be output as.
        """
        CLI = 1,
        FILE = 2,


    def __init__(
            self,
    ):
        """
        Creates an instance.
        """
        self._properties = dict()


    def add(
            self,
            name : str,
            value : str,
    ) -> object:
        """
        Adds a property.

        ### Aguments
        - name : str
            - Property name.
        - value : str
            - Property value.

        ### Returns
        - Current `util.Properties` instance.
        """
        self._properties[name] = value
        return self
    

    def compose_as_string(
            self,
            form : ComposeForm = ComposeForm.FILE,
    ) -> str:
        """
        Composes a string representation suitable for use in accordance with `form`,

        ### Arguments
        - form : ComposeForm
            - Desired representation.

        ### Returns
        - String representation in alignment with the desired composition form.
        """
        if form is Properties.ComposeForm.CLI:
            return self._compose_as_cli_string()
        elif form is Properties.ComposeForm.FILE:
            return self._compose_as_file_string()
        

    def compose_as_list(
            self,
            form : ComposeForm = ComposeForm.FILE,
    ) -> list:
        """
        Composes a list representation where each item is suitable for use in accordance with `form`.

        ### Arguments
        - form : ComposeForm
            - Desired representation of each item.

        ### Returns
        - List representation such that each item is in alignment with the desired composition form.
        """
        if form is Properties.ComposeForm.CLI:
            return self._compose_as_cli_list()
        elif form is Properties.ComposeForm.FILE:
            return self._compose_as_file_list()


    def _compose_as_cli_string(
            self,
    ) -> str:
        """
        Private implementation to compose a string representation suitable for use in accordance with `form`,

        ### Returns
        - String representation in alignment with the desired composition form.
        """
        result : str = ""
        for k, v in self._properties.items():
            result = result + f"-D{k}={v} "
        
        return result.strip()
    
    def _compose_as_file_string(
            self,
    ) -> str:
        """
        Private implementation to compose a list representation as a string suitable for use in a properties file.

        ### Returns
        - String representation suitable for use in a properties file.
        """
        result : str = ""
        for k, v in self._properties.items():
            result = result + f"{k}={v}\n"

        return result.strip()
    
 
    def _compose_as_cli_list(
            self,
    ) -> list:
        """
        Private implementation to compose a list representation where each item is suitable for use on the CLI.

        ### Returns
        - List representation such that each item is suitable for use on the CLI.
        """
        result : list = list()
        for k, v in self._properties.items():
            result.append(f"-D{k}={v}")

        return result
    
    def _compose_as_file_list(
            self,
    ) -> list:
        """
        Private implementatyion to compose a list rpresentation where each item is suitable for use a properties file.

        ### Returns
        - List representation such that each item is suitable for use in a properties file.
        """
        result : list = list()
        for k, v in self._properties.items():
            result.append(f"{k}={v}")

        return result