import os

from base import *
import config
import util


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


    @staticmethod
    def list() -> None:
        conf = config.Config.load()
        if conf.instances:
            for instance in conf.instances:
                print(f"{instance}")


    # TODO Determine instance state
    # TODO Update instance state
    # TODO Ensure instance start is separated from the TTY and in the background
    # TODO Build JVM properties
    def start(
            self,
    ) -> None:
        # Load configuration
        conf = config.Config.load()

        # Validate instance
        if not self.exists(conf):
            raise NameError(self._name, f"Instance {self._name} does not exist")

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
        self.execute(command = command, args = args, debug = True)


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


    # TODO Build properties
    # TODO Validate instance exists in config
    # TODO Determine instance state
    # TODO Provide status
    def status(
            self,
    ) -> None:
        conf = config.Config.load()


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
            conf : config.Config
    ) -> bool:
        return self._name in conf.instances and os.path.isdir(f"{conf.paths.instances}/{self._name}")


    def composeJBossProperties(
            self,
            conf : config.Config,
    ) -> util.Properties:
       result : util.Properties = util.Properties()

       # Calculated defaults controlled by this tool and default configuration
       result.add("jboss.server.base.dir", f"{conf.paths.instances}/{self._name}")
       result.add("jboss.server.default.config", f"{conf.defaults.jboss.profile}")

       # Add additional default properties
       for k, v in conf.defaults.jboss.properties.items():
           result.add(k, v)

       return result
    

    # TODO Merge instance level JVM options
    def composeJvmOptions(
            self,
            conf : config.Config,
    ) -> dict:
        result : dict = dict()
        for k, v in conf.defaults.jvm.options.items():
            result[k] = v

        return result
