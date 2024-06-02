import sys
import os


class Command:
    def execute(
            self,
            append_to_logfile : bool = False,
            args : list = [],
            command : str = None,
            debug : bool = False,
            logfile : str = None,
            stderr = sys.stderr,
            stdout = sys.stdout,
    ) -> None:
        cmdline = "{} {}".format(command, " ".join(args))
        if debug:
            print(f"Executing command: {cmdline}")
        os.system(cmdline)
