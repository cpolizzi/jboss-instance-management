import os

from base import *
import config
import util


class InstanceImpl(Command):
    _name : str
    _path : str
    _profile : str
    _jboss_properties : util.Properties
    _jvm_properties : util.Properties

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
        if not self._exists(conf):
            raise NameError(self._name, f"Instance {self._name} does not exist")

        # Compose JBoss properties
        self._properties = self._buildJBossProperties(conf = conf)

        # Compose command
        command = f"{conf.paths.jboss}/bin/standalone.sh"
        args = []
        args.append(self._properties.compose(util.Properties.ComposeForm.CLI))

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


    def _exists(
            self,
            conf : config.Config
    ) -> bool:
        return self._name in conf.instances and os.path.isdir(f"{conf.paths.instances}/{self._name}")


    def _buildJBossProperties(
            self,
            conf : config.Config,
    ) -> util.Properties:
       result : util.Properties = util.Properties()

       result.add("jboss.server.base.dir", f"{conf.paths.instances}/{self._name}")
       result.add("jboss.server.default.config", f"{conf.defaults.jboss.profile}")

       return result