from pyduinocli.commands.base import CommandBase
from pyduinocli.constants import flags, paths

import pkgutil
import importlib
import pyduinocli.commands as commands
import os, requests
from zipfile import ZipFile


class ArduinoCliCommand(CommandBase):
    """
    This is the main class of pyduinocli. This class wraps all calls to :code:`arduino-cli`.

    This is the only class that a user should create instances of.
    """

    __FORMAT_JSON = 'json'

    def __init__(self, cli_path='arduino-cli', config_file=None, additional_urls=None, log_file=None, log_format=None,
                 log_level=None, no_color=None):
        """
        :param cli_path: The :code:`arduino-cli` command name if available in :code:`$PATH`. Can also be a direct path to the executable
        :type cli_path: str
        :param config_file: The path to the :code:`arduino-cli` configuration file to be used
        :type config_file: str or NoneType
        :param additional_urls: A list of URLs to custom board definitions files
        :type additional_urls: list or NoneType
        :param log_file: A path to a file where logs will be stored
        :type log_file: str or NoneType
        :param log_format: The format the logs will use
        :type log_format: str or NoneType
        :param log_level: The log level for the log file
        :type log_level: str or NoneType
        :param no_color: Disable colored output
        :type no_color: bool or NoneType
        """
        
        # automagically import all the command classes from `pyduinocli/commands/`
        for loader, module_name, is_pkg in pkgutil.iter_modules(commands.__path__):
            module = importlib.import_module(f"{commands.__name__}.{module_name}")
            globals().update({
                name: obj for name, obj in vars(module).items()
                if name.endswith("Command")  # or any naming rule you want
            })
        
        # print(f"library path: {paths.LIB_DIR}")
        # print(f"cli path: {cli_path}")
        # print(f"defaault cli tool dir: {paths.DEFAULT_CLI_TOOL_DIR}")
        # print(f"cli yaml path: {paths.CLI_YAML_PATH}")
        # print(f"cli data path: {paths.CLI_DATA_PATH}")
        # print(f"cli user path: {paths.CLI_USER_PATH}")
        
        # import time
        # while(True):
        #     time.sleep(1)
        
        # if there is no CLI tool at `cli_path`, download the official tool
        
        loc_cli_exists = (os.path.isfile(os.path.join(paths.DEFAULT_CLI_TOOL_DIR, 'arduino-cli.exe'))) or (os.path.isfile(os.path.join(paths.DEFAULT_CLI_TOOL_DIR, 'arduino-cli')))
        arg_cli_exists = os.path.isfile(cli_path)
        
        if arg_cli_exists:
            pass
        elif loc_cli_exists:
            if os.name == 'nt':
                exec_name = 'arduino-cli.exe'
            elif os.name == 'posix':
                exec_name = 'arduino-cli'
            else:
                raise Exception("OS not supported :(")
            cli_path = os.path.join(paths.DEFAULT_CLI_TOOL_DIR.as_posix(), exec_name)
        else:
            cli_path = self.__install_arduino_cli(paths.DEFAULT_CLI_TOOL_DIR.as_posix())
            
        if config_file is None:
            config_file = paths.CLI_YAML_PATH.as_posix()
            
            
        base_args = [cli_path, flags.FORMAT, ArduinoCliCommand.__FORMAT_JSON]
        if config_file:
            base_args.extend([flags.CONFIG_FILE, CommandBase._strip_arg(config_file)])
        if additional_urls:
            base_args.extend([flags.ADDITIONAL_URLS, ",".join(CommandBase._strip_args(additional_urls))])
        if log_file:
            base_args.extend([flags.LOG_FILE, CommandBase._strip_arg(log_file)])
        if log_format:
            base_args.extend([flags.LOG_FORMAT, CommandBase._strip_arg(log_format)])
        if log_level:
            base_args.extend([flags.LOG_LEVEL, CommandBase._strip_arg(log_level)])
        if no_color is True:
            base_args.append(flags.NO_COLOR)
        CommandBase.__init__(self, base_args)
        
        self.__board = BoardCommand(self._base_args)
        self.__cache = CacheCommand(self._base_args)
        self.__compile = CompileCommand(self._base_args)
        self.__config = ConfigCommand(self._base_args)
        self.__core = CoreCommand(self._base_args)
        self.__daemon = DaemonCommand(self._base_args)
        self.__debug = DebugCommand(self._base_args)
        self.__lib = LibCommand(self._base_args)
        self.__sketch = SketchCommand(self._base_args)
        self.__upload = UploadCommand(self._base_args)
        self.__version = VersionCommand(self._base_args)
        self.__burn_bootloader = BurnBootloaderCommand(self._base_args)
        self.__completion = CompletionCommand(self._base_args)
        self.__outdated = OutdatedCommand(self._base_args)
        self.__update = UpdateCommand(self._base_args)
        self.__upgrade = UpgradeCommand(self._base_args)
        self.__monitor = MonitorCommand(self._base_args)
        
        # if its None, use the config file in the ../../arduino-cli directory (same place as CLI tool) if
        # it exists, otherwise create a one
        if config_file is None:
            if not os.path.isfile(config_file):
                self.config.init(dest_file=config_file)
            
            
        self.config.set('directories.data', [paths.CLI_DATA_PATH.as_posix()])
        self.config.set('directories.user', [paths.CLI_USER_PATH.as_posix()])

    @property
    def board(self):
        """
        The board command wrapper for this :code:`arduino-cli` wrapper

        :type: :class:`pyduinocli.commands.board.BoardCommand`
        """
        return self.__board

    @property
    def cache(self):
        """
        The cache command wrapper for this :code:`arduino-cli` wrapper

        :type: :class:`pyduinocli.commands.cache.CacheCommand`
        """
        return self.__cache

    @property
    def compile(self):
        """
        The compile command wrapper for this :code:`arduino-cli` wrapper

        :type: :class:`pyduinocli.commands.compile.CompileCommand`
        """
        return self.__compile

    @property
    def config(self):
        """
        The config command wrapper for this :code:`arduino-cli` wrapper

        :type: :class:`pyduinocli.commands.config.ConfigCommand`
        """
        return self.__config

    @property
    def core(self):
        """
        The core command wrapper for this :code:`arduino-cli` wrapper

        :type: :class:`pyduinocli.commands.core.CoreCommand`
        """
        return self.__core

    @property
    def daemon(self):
        """
        The daemon command wrapper for this :code:`arduino-cli` wrapper

        :type: :class:`pyduinocli.commands.daemon.DaemonCommand`
        """
        return self.__daemon

    @property
    def debug(self):
        """
        The debug command wrapper for this :code:`arduino-cli` wrapper

        :type: :class:`pyduinocli.commands.debug.DebugCommand`
        """
        return self.__debug

    @property
    def lib(self):
        """
        The lib command wrapper for this :code:`arduino-cli` wrapper

        :type: :class:`pyduinocli.commands.lib.LibCommand`
        """
        return self.__lib

    @property
    def sketch(self):
        """
        The sketch command wrapper for this :code:`arduino-cli` wrapper

        :type: :class:`pyduinocli.commands.sketch.SketchCommand`
        """
        return self.__sketch

    @property
    def upload(self):
        """
        The upload command wrapper for this :code:`arduino-cli` wrapper

        :type: :class:`pyduinocli.commands.upload.UploadCommand`
        """
        return self.__upload

    @property
    def version(self):
        """
        The version command wrapper for this :code:`arduino-cli` wrapper

        :type: :class:`pyduinocli.commands.version.VersionCommand`
        """
        return self.__version

    @property
    def burn_bootloader(self):
        """
        The burn-bootloader command wrapper for this :code:`arduino-cli` wrapper

        :type: :class:`pyduinocli.commands.burn_bootloader.BurnBootloaderCommand`
        """
        return self.__burn_bootloader

    @property
    def completion(self):
        """
        The completion command wrapper for this :code:`arduino-cli` wrapper

        :type: :class:`pyduinocli.commands.completion.CompletionCommand`
        """
        return self.__completion

    @property
    def outdated(self):
        """
        The outdated command wrapper for this :code:`arduino-cli` wrapper

        :type: :class:`pyduinocli.commands.outdated.OutdatedCommand`
        """
        return self.__outdated

    @property
    def update(self):
        """
        The update command wrapper for this :code:`arduino-cli` wrapper

        :type: :class:`pyduinocli.commands.update.UpdateCommand`
        """
        return self.__update

    @property
    def upgrade(self):
        """
        The upgrade command wrapper for this :code:`arduino-cli` wrapper

        :type: :class:`pyduinocli.commands.upgrade.UpgradeCommand`
        """
        return self.__upgrade

    @property
    def monitor(self):
        """
        The monitor command wrapper for this :code:`arduino-cli` wrapper

        :type: :class:`pyduinocli.commands.monitor.MonitorCommand`
        """
        return self.__monitor

    # installing the arduino-cli
    def __install_arduino_cli(self, path: str) -> str:
        import subprocess
        
        # install the arduino-cli
        # if windows, download the cli exe
        if os.name == 'nt':
            print("Downloading Windows arduino-cli...")
            
            try:
                os.mkdir(path)
            except FileExistsError:
                print('folder exists!')
            
            url = "https://downloads.arduino.cc/arduino-cli/arduino-cli_latest_Windows_64bit.zip"
            
            r = requests.get(url)
            with open(os.path.join(path, "arduino-cli.zip"), "wb") as f:
                f.write(r.content)

            # extract the zip file
            with ZipFile(os.path.join(path, "arduino-cli.zip"), 'r') as zip_ref:
                zip_ref.extractall(path)
            
            # remove the zip file and license
            os.remove(os.path.join(path, "arduino-cli.zip"))
            os.remove(os.path.join(path, "LICENSE.txt"))
            return os.path.join(path, 'arduino-cli.exe')
            
        elif os.name == 'posix':
            print("Downloading Mac/Linux arduino-cli...")

            try:
                os.mkdir(path)
            except FileExistsError:
                # print('Folder exists!')
                pass
            
            posixcmd = f'curl -fsSL https://raw.githubusercontent.com/arduino/arduino-cli/master/install.sh | BINDIR={path} sh'
            
            # run the install script
            subprocess.run(posixcmd, shell=True, check=True)
            return os.path.join(path, 'arduino-cli')
        else:
            raise SystemError("OS not supported.")
        
