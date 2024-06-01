from base import *


# TODO Consult instance config as we need here at a minimumum: PID (if any), JBoss install path, instances directory path, JBoss config file to use
class InstanceImpl(Command):
    def __init__(
            self,
            name : str,
    ):
        self._name = name


    def start(
            self,
    ):
        props = self._propertiesForInstance()
        print(props)
        command = "standalone.sh"
        args = []
        args.append(f"{self._name}")
        return
        self.execute(command = command, args = args)


    def stop(
            self,
    ):
        pass

    def restart(
            self,
    ):
        pass


    def status(
            self,
    ):
        pass


    def kill(
            self,
    ):
        pass


    def cli(
            self,
            command: str,
            file: str,
    ):
        pass


    def _propertiesForInstance(self) -> str:
       result = {
            f"jboss.server.base.dir": "/tmp/jboss/instances/{self._name}",
            f"jboss.server.default.config": "standalone-full.xml",
       }
       return result
