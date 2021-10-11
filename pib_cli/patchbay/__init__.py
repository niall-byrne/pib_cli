"""Patch Endpoints For Tests."""

CLI_CLICK_ECHO = 'pib_cli.cli.click.echo'
CLI_EXECUTE_EXTERNAL_COMMAND = 'pib_cli.cli.execute_external_command'
CLI_EXECUTE_INTERNAL_COMMAND = 'pib_cli.cli.execute_internal_command'

CONTAINER_MANAGER_IS_CONTAINER = (
    'pib_cli.support.dev_container.DevContainer.is_container'
)
CONTAINER_MANAGER_OS_PATH_EXISTS = (
    'pib_cli.support.dev_container.os.path.exists'
)

CONFIGURATION_MANAGER_FIND_CONFIG = (
    'pib_cli.support.configuration.ConfigurationManager.find_config_entry'
)
CONFIGURATION_MANAGER_IS_CONFIG_EXECUTABLE = (
    'pib_cli.support.configuration.ConfigurationManager.is_config_executable'
)
CONFIGURATION_MANAGER_GET_CONFIG_PATH_METHOD = (
    'pib_cli.support.configuration.ConfigurationManager.get_config_path_method'
)
CONFIGURATION_MANAGER_LOAD_CONFIG = (
    'pib_cli.support.configuration.ConfigurationManager._load_config'
)

EXTERNAL_COMMANDS_PROCESS_MANAGER = (
    'pib_cli.support.external_commands.ProcessManager'
)
EXTERNAL_COMMANDS_SYS_EXIT = 'pib_cli.support.external_commands.sys.exit'
EXTERNAL_COMMANDS = 'pib_cli.support.external_commands.ExternalCommands'

INTERNAL_COMMANDS_OS_PATH_EXISTS = (
    'pib_cli.support.internal_commands.os.path.exists'
)
INTERNAL_COMMANDS_MAKE_DIRS = 'pib_cli.support.internal_commands.os.makedirs'
INTERNAL_COMMANDS_SHUTIL_COPY = (
    'pib_cli.support.internal_commands.shutil.copy'
)
INTERNAL_COMMANDS_CLASS = 'pib_cli.support.internal_commands.InternalCommands'
INTERNAL_COMMANDS_EXTERNAL_COMMAND_EXECUTOR = (
    'pib_cli.support.internal_commands.execute_external_command'
)
INTERNAL_COMMANDS_SPAWN = (
    'pib_cli.support.internal_commands.ProcessManager.spawn'
)
INTERNAL_COMMANDS_GET_CONFIG_FILE_NAME = (
    'pib_cli.support.internal_commands.get_config_file_name'
)

PATH_MANAGER_OS_CHDIR = 'pib_cli.support.paths.os.chdir'
PATH_MANAGER_OS_PATH_EXISTS = 'pib_cli.support.paths.os.path.exists'
PATH_MANAGER_CONTAINER_PATH_MANAGER = (
    'pib_cli.support.paths.DevContainerPathManager'
)

PROCESS_MANAGER_OS_ENVIRON = 'pib_cli.support.processes.os.environ'
PROCESS_MANAGER_OS_SYSTEM = 'pib_cli.support.processes.os.system'
PROCESS_MANAGER_SPAWN_SINGLE = (
    'pib_cli.support.processes.ProcessManager.spawn_single'
)
