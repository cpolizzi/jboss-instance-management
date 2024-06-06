from enum import Enum


class Properties:
    _properties : dict

    class ComposeForm(Enum):
        CLI = 1,
        FILE = 2,


    def __init__(
            self,
    ):
        self._properties = dict()


    def add(
            self,
            name : str,
            value : str,
    ) -> object:
        self._properties[name] = value
        return self
    

    def compose_as_string(
            self,
            form : ComposeForm = ComposeForm.FILE,
    ) -> str:
        if form is Properties.ComposeForm.CLI:
            return self._compose_as_cli_string()
        elif form is Properties.ComposeForm.FILE:
            return self._compose_as_file_string()
        

    def compose_as_list(
            self,
            form : ComposeForm = ComposeForm.FILE,
    ) -> list:
        if form is Properties.ComposeForm.CLI:
            return self._compose_as_cli_list()
        elif form is Properties.ComposeForm.FILE:
            return self._compose_as_file_list()


    def _compose_as_cli_string(
            self,
    ) -> str:
        result : str = ""
        for k, v in self._properties.items():
            result = result + f"-D{k}={v} "
        
        return result.strip()
    
    def _compose_as_file_string(
            self,
    ) -> str:
        result : str = ""
        for k, v in self._properties.items():
            result = result + f"{k}={v}\n"

        return result.strip()
    

    def _compose_as_cli_list(
            self,
    ) -> list:
        result : list = list()
        for k, v in self._properties.items():
            result.append(f"-D{k}={v}")

        return result
    
    def _compose_as_file_list(
            self,
    ) -> list:
        result : list = list()
        for k, v in self._properties.items():
            result.append(f"{k}={v}")

        return result