from box import Box
import os
import psutil
import time

from base import *
from .state import InstanceStateManager, InstanceState
import config
import util


# TODO Support different output formats: YAML, JSON, table
class InstanceImpl(Command):
    """
    Implements the Typer CLI.

    - Uses a backing YAML file for the configuration which records all salient information per instance as well as global
      defaults and critical paths.

    - Uses a second backing YAML file for runtime instance state management / information such as the PID
      (Process IDentifier) of the instance.
    """
    _name : str
    _path : str
    _profile : str
    _jboss_properties : util.Properties
    _jvm_options : dict

    TERMINATE_WAIT_TIME = 10

    def __init__(
            self,
            name : str,
    ):
        """
        Creates an instace.

        ### Arguments
        - name : str
            - Instance name.
        """
        self._name = name

    def add(
            self,
    ) -> None:
        """
        Adds a managed instance.

        ### Returns
        - Nothing.
        """
        conf = config.Config.load()


    def remove(
        self,
    ) -> None:
        """
        Removes a managed instance.

        ### Returns
        - Nothing.
        """
        conf = config.Config.load()


    # TODO Warn if instance does not actually exist on the filesystem
    # TODO Add an option for verbose to show complete configuration?
    @staticmethod
    def list() -> None:
        """
        Lists known managed instances.

        ### Returns
        - Nothing.
        """
        conf = config.Config.load()
        if conf.instances:
            for instance in conf.instances:
                print(f"{instance.name}")


    def start(
            self,
            background: bool = False,
    ) -> None:
        """
        Starts this managed instance.

        ### Arguments
        - background :  bool
            - Whether or not to start the instance in the background and detached from the TTY.

        ### Returns
        - Nothing.

        ### Raises
        - NameError
            - If the instance does not exist.
        """
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
        pid_or_exit_status = self.execute(command = command, args = args, debug = False, background = background)
        if background:
            # Obtain PID of JVM which is a child process of the executed command, but we must wait for it to be created
            # so we have to poll.
            proc = psutil.Process(pid_or_exit_status)
            while len(proc.children()) == 0:
                time.sleep(1)

            instance_state = Box(name = self._name, pid = proc.children()[0].pid)
            state_manager.update(instance_state)
            state_manager.save(conf)


    def stop(
            self,
    ) -> None:
        """
        Stops this managed instance. First the instance is requested to gracefully termimate and then after
        `TERMINATE_WAIT_TIME` forcefully terminates it.

        ### Returns
        - Nothing.

        ### Raises
        - NameError
            - If the instance does not exist.
        """
        # Load configuration
        conf = config.Config.load()

        # Validate instance exists
        if not self.exists(conf):
            raise NameError(self._name, f"Instance {self._name} does not exist")
        
        # Determine current instance state
        state_manager = InstanceStateManager.load(conf)
        instance_state : InstanceState = None
        proc : psutil.Process = state_manager.is_running(self._name)
        if proc:
            # Instance is running, ensure that it a JBoss JVM process
            instance_state = state_manager.state_for(self._name)
            print(f"Stopping instance {self._name} with PID {instance_state.pid}")
            if proc.name() == "java" and len(proc.cmdline()) > 1 and proc.cmdline()[1] == "-D[Standalone]":
                # Gracefully stop and wait for 10 seconds and then forcefully terminate
                proc.terminate()
                try:
                    proc.wait(self.TERMINATE_WAIT_TIME)
                except psutil.NoSuchProcess:
                    pass
                except psutil.TimeoutExpired:
                    proc.kill()
        else:
            # Instance is not running
            print(f"Instance {self._name} is not running")
            instance_state = Box(name = self._name)

        # Remove instance state
        state_manager.remove(instance_state)
        state_manager.save(conf)


    def restart(
            self,
    ) -> None:
        """
        Restarts this  managed instance using the semantics described by `stop()` and `start()`.

        ### Returns
        - Nothing.

        ### Raises
        - NameError
            - If the instance does not exist.
        """
        # Load configuration
        conf = config.Config.load()

        self.stop()
        self.start(background = True)


    def status(
            self,
    ) -> None:
        """
        Displays the current state of this managed instance.

        ### Returns
        - Nothing.

        ### Raises
        - NameError
            - If the instance does not exist.
        """
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
            # Instance is not running, remove state
            print(f"Instance {self._name} is not running")
            instance_state = Box(name = self._name)
            state_manager.remove(instance_state)
            state_manager.save(conf)
        

    def kill(
            self,
    ) -> None:
        """
        Forcefully stops this managed instance.

        ### Returns
        - Nothing.

        ### Raises
        - NameError
            - If the instance does not exist.
        """
        # Load configuration
        conf = config.Config.load()

        # Validate instance exists
        if not self.exists(conf):
            raise NameError(self._name, f"Instance {self._name} does not exist")
        
        # Determine current instance state
        state_manager = InstanceStateManager.load(conf)
        instance_state : InstanceState = None
        proc : psutil.Process = state_manager.is_running(self._name)
        if proc:
            # Instance is running, ensure that it a JBoss JVM process
            instance_state = state_manager.state_for(self._name)
            print(f"Stopping instance {self._name} with PID {instance_state.pid}")
            if proc.name() == "java" and len(proc.cmdline()) > 1 and proc.cmdline()[1] == "-D[Standalone]":
                # Forcefully terminate
                proc.kill()
        else:
            # Instance is not running
            print(f"Instance {self._name} is not running")
            instance_state = Box(name = self._name)

        # Remove instance state
        state_manager.remove(instance_state)
        state_manager.save(conf)


    # TODO Handle 3 cases: 1) interactive; 2) non-interactive command execution; 3) non-interactive file execution
    def cli(
            self,
            command: str,
            file: str,
    ) -> None:
        """
        Executes the JBoss CLI against this managed instance. Ixf both are specified then `command` is performed first
        and then the CLI commands contained in `file` are processed. If neither is provided then an interactive
        session is created.

        ### Arguments
        - command : str
            - CLI command to execute.
        - file : str
            - File containing CLI commands to execute.

        ### Returns
        - Nothing.

        ### Raises
        - NameError
            - If the instance does not exist.
        """
        # Load configuration
        conf = config.Config.load()

        # Validate instance exists
        if not self.exists(conf):
            raise NameError(self._name, f"Instance {self._name} does not exist")

        # Compose JBoss properties
        self._jboss_properties = self.composeJBossProperties(conf = conf)

        # Compose command to execute
        command = f"{conf.paths.jboss}/bin/jboss-cli.sh"
        args = []
        args = args + self._jboss_properties.compose_as_list(util.Properties.ComposeForm.CLI)

        # Execute command
        print(f"Start CLI instance {self._name}")
        pid_or_exit_status = self.execute(command = command, args = args, debug = False, background = False)


    def exists(
            self,
            conf : config.Config,
    ) -> bool:
        """
        Returns whether or not this managed instance exists in the configuration and on the filesystem.

        ### Arguments
        - conf : config.Config
            - Configuration file instance which serves as the source of truth for all managed instances.

        ### Returns
        - True if the managed instance exists, False otherwise.
        """
        instance = next((x for x in conf.instances if x.name == self._name), None)
        return instance and os.path.isdir(f"{conf.paths.instances}/{self._name}")
    

    def composeJBossProperties(
            self,
            conf : config.Config,
    ) -> util.Properties:
       """
       Composes JBoss and JVM properties suitable for use in managed instance lifecycle operations.
       
       ### Arguments
       - conf : config.Config
            - Configuration file instance which serves as the source of truth for all managed instances.

       ### Returns
        - A util.Properties instance based on the backing configuration for this managed instance.
       """
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
        """
        Composes JBoss and JVM properties suitable for use in managed instance lifecycle operations.
       
        ### Arguments
        - conf : config.Config
             - Configuration file instance which serves as the source of truth for all managed instances.

        ### Returns
        - A util.Properties instance based on the backing configuration for this managed instance.
        """
        
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
