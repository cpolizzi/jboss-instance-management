from box import Box
import os

from base import *
from .state import InstanceStateManager, InstanceState
import config
import util


# TODO Support different output formats: YAML, JSON, table
class InstanceImpl(Command):
    _name : str
    _path : str
    _profile : str
    _jboss_properties : util.Properties
    _jvm_options : dict

    def __init__(
            self,
            name : str,
    ):
        self._name = name

    def add(
            self,
    ) -> None:
        conf = config.Config.load()


    def remove(
        self,
    ) -> None:
        conf = config.Config.load()


    # TODO Warn if instance does not actually exist on the filesystem
    # TODO Add an option for verbose to show complete configuration?
    @staticmethod
    def list() -> None:
        conf = config.Config.load()
        if conf.instances:
            for instance in conf.instances:
                print(f"{instance.name}")


    def start(
            self,
            background: bool = False,
    ) -> None:
        #<><> BEGIN boiler plate logic
        # Load configuration
        conf = config.Config.load()

        # Validate instance exists
        if not self.exists(conf):
            raise NameError(self._name, f"Instance {self._name} does not exist")
        
        # Determine current instance state
        state_manager = InstanceStateManager.load(conf)
        instance_state : InstanceState
        if state_manager.is_running(self._name):
            # Instance is running, nothing more to do
            instance_state = state_manager.state_for(self._name)
            print(f"Instance {self._name} is already running and has PID {instance_state.pid}")
            return
        #<><> END boiler plate logic
        
        # Compose JBoss properties
        self._jboss_properties = self.composeJBossProperties(conf = conf)

        # Compose JVM options and make available via environment variable
        self._jvm_options = self.composeJvmOptions(conf = conf)
        java_opts : str = ""
        for k, v in self._jvm_options.items():
            java_opts = java_opts + f"{k}{v} "
        os.environ["JAVA_OPTS"] = java_opts.strip()

        # Compose command to execute
        command = f"{conf.paths.jboss}/bin/standalone.sh"
        args = []
        args = args + self._jboss_properties.compose_as_list(util.Properties.ComposeForm.CLI)

        # Execute command
        print(f"Starting instance {self._name}")
        exec_status = self.execute(command = command, args = args, debug = False, background = background)
        if background:
            instance_state = Box(name = self._name, pid = exec_status)
            state_manager.update(instance_state)
            state_manager.save(conf)


    # TODO Build properties
    # TODO Validate instance exists in config
    # TODO Determine instance state
    # TODO Stop instance
    # TODO Update instance state
    def stop(
            self,
    ) -> None:
        conf = config.Config.load()


    # TODO Build properties
    # TODO Validate instance exists in config
    # TODO Determine instance state
    # TODO Restart instance
    # TODO Update instance state
    def restart(
            self,
    ) -> None:
        conf = config.Config.load()


    def status(
            self,
    ) -> None:
        #<><> BEGIN boiler plate logic
        # Load configuration
        conf = config.Config.load()

        # Validate instance exists
        if not self.exists(conf):
            raise NameError(self._name, f"Instance {self._name} does not exist")
        
        # Determine current instance state
        state_manager = InstanceStateManager.load(conf)
        instance_state : InstanceState
        if state_manager.is_running(self._name):
            # Instance is running
            instance_state = state_manager.state_for(self._name)
            print(f"Instance {self._name} is running and has PID {instance_state.pid}")
        else:
            # Instance is not running
            print(f"Instance {self._name} is not running")
        #<><> END boiler plate logic
        

    # TODO Build properties
    # TODO Validate instance exists in config
    # TODO Determine instance state
    # TODO Kill instance
    # TODO Update instance state
    def kill(
            self,
    ) -> None:
        conf = config.Config.load()


    # TODO Build properties
    # TODO Validate instance exists in config
    # TODO Execute CLI
    def cli(
            self,
            command: str,
            file: str,
    ) -> None:
        conf = config.Config.load()
        pass


    def exists(
            self,
            conf : config.Config,
    ) -> bool:
        instance = next((x for x in conf.instances if x.name == self._name), None)
        return instance and os.path.isdir(f"{conf.paths.instances}/{self._name}")
    

    def composeJBossProperties(
            self,
            conf : config.Config,
    ) -> util.Properties:
       result : util.Properties = util.Properties()

       # Calculated defaults controlled by this tool and default configuration paths
       result.add("jboss.server.base.dir", f"{conf.paths.instances}/{self._name}")
       result.add("jboss.server.default.config", f"{conf.defaults.jboss.profile}")

       # Add default JBoss specific properties from configuration
       try:
           for k, v in conf.defaults.jboss.properties.items():
               result.add(k, v)
       except KeyError:
           pass
       
       # Add default JVM properties from configuration
       try:
           for k, v in conf.defaults.java.properties.items():
               result.add(k, v)
       except KeyError:
           pass
       
       # Add instance JVM properties from configuration
       instance = next((x for x in conf.instances if x.name == self._name), None)
       try:
           for k, v in instance.java.properties.items():
               result.add(k, v)
       except KeyError:
           pass 

       return result
    

    def composeJvmOptions(
            self,
            conf : config.Config,
    ) -> dict:
        result : dict = dict()

        # Default options
        try:
            for k, v in conf.defaults.jvm.options.items():
                result[k] = v
        except KeyError:
            pass

        # Instance options
        instance = next((x for x in conf.instances if x.name == self._name), None)
        try:
            for k, v in instance.jvm.options.items():
                result[k] = v
        except KeyError:
            pass

        return result
