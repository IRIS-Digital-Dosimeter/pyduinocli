from pathlib import Path

# LIB_DIR = os.path.dirname(os.path.join(os.path.abspath(__file__), '..', '..'))
LIB_DIR = Path(__file__).resolve().parent.parent

DEFAULT_CLI_TOOL_DIR = Path(LIB_DIR, 'arduino-cli').resolve()
CLI_YAML_PATH = Path(DEFAULT_CLI_TOOL_DIR, 'arduino-cli.yaml').resolve()
CLI_DATA_PATH = Path(DEFAULT_CLI_TOOL_DIR, 'data').resolve()
CLI_USER_PATH = Path(DEFAULT_CLI_TOOL_DIR, 'user').resolve()