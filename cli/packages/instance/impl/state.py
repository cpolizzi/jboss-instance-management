from box import Box
from jsonschema import validate
import os
import psutil
import yaml

import config
import paths


class InstanceState:
    def __init__(
            self,
            **entries,
    ):
        self.__dict__.update(entries)


class InstanceStateManager:
    STATE_FILE = "instance-states.yaml"

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
        Returns the absolute path to the instance state schema.
        """
        return f"{paths.Paths.schemas()}/instance-state.schema.yaml"


    @classmethod
    def load(
            cls,
            config : config.Config,
    ):
        """
        Loads instance states, validates it against the schema and returns the result as a dynamic object.
        """
        result : InstanceStateManager = None

        # Load schema
        with open(InstanceStateManager.schema(), "r") as f:
            schema = yaml.safe_load(f)

        # Load configuration and validate against schema
        state_data = {}
        state_file = f"{config.paths.run}/{InstanceStateManager.STATE_FILE}"
        try:
            with open(state_file, "r") as f:
                state_data = yaml.safe_load(f)
            validate(state_data, schema)
        except FileNotFoundError:
            # State data does not exist
            state_data = {
                "instances": [],
            }

        result = InstanceStateManager(**Box(state_data))

        return result
    

    def save(
            self,
            config : config.Config,
    ) -> None:
        """
        Saves the configuration.
        """
        state_file = f"{config.paths.run}/{InstanceStateManager.STATE_FILE}"
        os.makedirs(os.path.dirname(state_file), exist_ok = True)
        Box(vars(self)).to_yaml(filename = state_file, indent = 2, sort_keys = False, default_flow_style = False)


    def state_for(
            self,
            name : str,
    ) -> InstanceState:
        result =  None

        state = next((x for x in self.instances if x.name == name), None)
        if state:
            result = InstanceState(**state)
        return result


    # TODO This really shouldn't be called this since it returns more than a boolean
    def is_running(
            self,
            name : str,
    ) -> psutil.Process:
        result : psutil.Process = None

        try:
            state = self.state_for(name)
            if state:
                proc = psutil.Process(state.pid)
                if proc.is_running:
                    result = proc
        except psutil.NoSuchProcess:
            pass
        
        return result


    def update(
            self,
            state : InstanceState,
    ) -> None:
        instance_state = next((x for x in self.instances if x.name == state.name), None)
        if instance_state is None:
            self.instances.append(state)
        else:
            for i, x in enumerate(self.instances):
                if x.name == state.name:
                    self.instances[i] = state


    def remove(
            self,
            state : InstanceState,
    ) -> None:
        for i, x in enumerate(self.instances):
            if x.name == state.name:
                del self.instances[i]
