"""Patch Endpoints For Tests"""

CLI_CLICK_ECHO = 'pib_cli.cli.click.echo'
CLI_EXECUTE_EXTERNAL_COMMAND = 'pib_cli.cli.execute_external_command'
CLI_EXECUTE_INTERNAL_COMMAND = 'pib_cli.cli.execute_internal_command'

CONTAINER_MANAGER_IS_CONTAINER = (
    'pib_cli.support.container.ContainerManager.is_container'
)
CONTAINER_MANAGER_OS_PATH_EXISTS = 'pib_cli.support.container.os.path.exists'

CONFIGURATION_MANAGER_FIND_CONFIG = (
    'pib_cli.support.configuration.ConfigurationManager.find_config_entry'
)
CONFIGURATION_MANAGER_IS_CONFIG_EXECUTABLE = (
    'pib_cli.support.configuration.ConfigurationManager.is_config_executable'
)
CONFIGURATION_MANAGER_GET_CONFIG_PATH_METHOD = (
    'pib_cli.support.configuration.ConfigurationManager.get_config_path_method'
)

EXTERNAL_COMMANDS_PATH_MANAGER = (
    'pib_cli.support.external_commands.PathManager'
)
EXTERNAL_COMMANDS_PROCESS_MANAGER = (
    'pib_cli.support.external_commands.ProcessManager'
)
EXTERNAL_COMMANDS_SYS_EXIT = 'pib_cli.support.external_commands.sys.exit'
EXTERNAL_COMMANDS = 'pib_cli.support.external_commands.ExternalCommands'

INTERNAL_COMMANDS_OS_PATH_EXISTS = (
    'pib_cli.support.internal_commands.os.path.exists'
)
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

PATH_MANAGER_OS_CHDIR = 'pib_cli.support.paths.os.chdir'

PROCESS_MANAGER_OS_ENVIRON = 'pib_cli.support.processes.os.environ'
PROCESS_MANAGER_OS_SYSTEM = 'pib_cli.support.processes.os.system'
PROCESS_MANAGER_SPAWN_SINGLE = (
    'pib_cli.support.processes.ProcessManager.spawn_single'
)
