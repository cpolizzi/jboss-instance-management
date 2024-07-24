from box import Box
from jsonschema import validate
import os
import psutil
import yaml

import config
import paths


class InstanceState:
    """
    Represents a managed instance state suitable for use with YAML or JSON persistence and manipulation.
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


class InstanceStateManager:
    """
    Managed instance stage low level state manager. Responsible for persistence of the backing YAML file for instance
    states and provides an easy to use mechanism to update instance states.
    """
    # TODO Consider instead just using in the configuration `paths.run` (which right now is just a directory)
    STATE_FILE = "instance-states.yaml"

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
        Returns the absolute path to the managed instance state schema.

        ### Returns
        - Managed instance state schema path.
        """
        return f"{paths.Paths.schemas()}/instance-state.schema.yaml"


    @classmethod
    def load(
            cls,
            config : config.Config,
    ):
        """
        Loads instance states, validates it against the schema and returns the result as a dynamic object.

        ### Arguments
        - config : config.Config
            - Managed instance configuration.

        ### Returns
        - Instance state manager with its backing data populated.
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
        Saves the managed instance states.

        ### Arguments
        - config : config.Config
            - Managed instance configuration.

        ### Returns
        - Nothing.
        """
        state_file = f"{config.paths.run}/{InstanceStateManager.STATE_FILE}"
        os.makedirs(os.path.dirname(state_file), exist_ok = True)
        Box(vars(self)).to_yaml(filename = state_file, indent = 2, sort_keys = False, default_flow_style = False)


    def state_for(
            self,
            name : str,
    ) -> InstanceState:
        """
        Helper to easily obtain the managed instance state from the persisted instance states.

        ### Arguments
        - name : str
            - Managed instance name.

        ### Returns
        - Managed instance state of `None` if it is unavailable.
        """
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
        """
        Helper to obtain the current runtime information for a managed instance.

        ### Arguments
        - name : str
            - Managed instance name.

        ### Returrns
        - Runtime information at the system process level or `None` if the managed instance is not in a running state.
        """
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
        """
        Updates the managed instance state to what is provided.

        ### Arguments
        - state : InstanceState
            - Managed instance desired state.

        ### Returns
        - Nothing.
        """
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
        """
        Removes tne managed instance state.

        ### Arguments
        - state : InstanceState
            - Managed instance state to remove.

        ### Returns
        - Nothing.
        """
        for i, x in enumerate(self.instances):
            if x.name == state.name:
                del self.instances[i]
