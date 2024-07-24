import sys
import os
import subprocess


class Command:
    def execute(
            self,
            args : list = [],
            command : str = None,
            debug : bool = False,
            background : bool = False,
    ) -> int:
        """
        Executes a command.

        If `background` is `True` then the command is executed in the background detachad from the TTY, *stdout*, 
        *stderr* and *stdin* are suppresed and the PID is returned. Otherwise the comamnd is executed in the 
        foreground, *stdout*, *stderr* and *stdim* are preserved amd the exit status of the command is returned.
        """
        result = None

        cmdline = "{} {}".format(command, " ".join(args))
        if debug:
            print(f"Executing command: {cmdline}")
        if not background:
            # Run command in the foreground and wait for it to exit
            result = os.waitstatus_to_exitcode(os.system(cmdline))
        else:
            # Run command in the background, detached, and do not wait for it at all
            # args = [ command ] + args
            # result = os.spawnv(os.P_NOWAITO, command, args)
            args = [ command ] + args
            result = subprocess.Popen(args, stdout = subprocess.DEVNULL, stderr = subprocess.STDOUT, stdin = subprocess.DEVNULL).pid
 
        return result