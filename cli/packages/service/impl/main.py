from base import *


class ServiceImpl(Command):
    def __init__(
            self,
            name : str,
    ):
        self._name = name
    

    def add(
            self,
    ):
        command = "standalone.sh"
        args = []
        args.append(f"{self._name}")
        return
        self.execute(command = command, args = args)


    def remove(
            self,
    ):
        command = "standalone.sh"
        args = []
        args.append(f"{self._name}")
        return
        self.execute(command = command, args = args)
