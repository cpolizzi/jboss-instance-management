from base import *
import config


class InstanceImpl(Command):
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


    # TODO Build properties
    # TODO Validate instance exists in config
    # TODO Determine instance state
    # TODO Start instance
    # TODO Update instance state
    def start(
            self,
    ) -> None:
        conf = config.Config.load()

        props = self._propertiesForInstance()
        print(props)
        command = "standalone.sh"
        args = []
        args.append(f"{self._name}")
        return
        self.execute(command = command, args = args)


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


    # TODO Needs to be used outside of this class, so make it available in a better way (maybe a new class?)
    # TODO Load config and use paths accordingly from that
    # TODO Validate instance exists in config
    def _propertiesForInstance(self) -> str:
       result = {
            f"jboss.server.base.dir": "/tmp/jboss/instances/{self._name}",
            f"jboss.server.default.config": "standalone-full.xml",
       }
       return result
