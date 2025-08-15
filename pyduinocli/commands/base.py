import json
from subprocess import Popen, run, PIPE
from pyduinocli.errors.arduinoerror import ArduinoError


class CommandBase:

    def __init__(self, base_args):
        self._base_args = list(base_args)

    @staticmethod
    def _strip_arg(arg):
        return arg.lstrip("-")

    @staticmethod
    def _strip_args(args):
        out = list()
        for arg in args:
            out.append(CommandBase._strip_arg(arg))
        return out

    @staticmethod
    def __parse_output(data):
        try:
            return json.loads(data)
        except ValueError:
            return data

    def _exec(self, args):
        command = list(self._base_args)
        command.extend(args)
        # p = Popen(command, stdout=PIPE, stderr=PIPE)
        # stdout, stderr = p.communicate()
        # stdout = stdout.decode("utf-8").strip()
        # stderr = stderr.decode("utf-8").strip()
        p = run(command, text=True, capture_output=True)
        result = dict(
            __stdout=p.stdout,
            __stderr=p.stderr,
            result=self.__parse_output(p.stdout)
        )
        if p.returncode != 0:
            raise ArduinoError(result)
        return result
