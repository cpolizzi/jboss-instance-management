from base import *


class ExpressionImpl(Command):
    def __init__(
            self,
            name,
    ):
        self._name = name
    

    def encrypt(
            self,
            expression: str,
            resolver: str,
    ) -> str:
        command = "standalone.sh"
        args = []
        args.append(f"{self._name}")
        return
        self.execute(command = command, args = args)
