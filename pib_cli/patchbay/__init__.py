"""Patch Endpoints For Tests"""

CLI_COMMANDS = 'pib_cli.cli.Commands'
CLI_SYS_EXIT = 'pib_cli.cli.sys.exit'
CLI_CLICK_ECHO = 'pib_cli.cli.click.echo'
CLI_PIB_CLI_EXECUTE = 'pib_cli.cli.execute'

PATH_MANAGER_OS_CHDIR = 'pib_cli.support.paths.os.chdir'

PROCESS_MANAGER_OS_SYSTEM = 'pib_cli.support.processes.os.system'
PROCESS_MANAGER_SPAWN_SINGLE = (
    'pib_cli.support.processes.ProcessManager.spawn_single')

COMMANDS_IS_CONTAINER = 'pib_cli.support.commands.Commands.is_container'
COMMANDS_OS_ENVIRON = 'pib_cli.support.commands.os.environ'
COMMANDS_OS_PATH_EXISTS = 'pib_cli.support.commands.os.path.exists'
COMMANDS_PATH_MANAGER = 'pib_cli.support.commands.PathManager'
COMMANDS_PROCESS_MANAGER = 'pib_cli.support.commands.ProcessManager'
COMMANDS_SETUP_BASH = 'pib_cli.support.commands.Commands.setup_bash'
COMMANDS_SHUTIL_COPY = 'pib_cli.support.commands.shutil.copy'
