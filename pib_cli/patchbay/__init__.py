"""Patch Endpoints For Tests."""

EXTERNAL_COMMANDS_PROCESS_MANAGER = (
    'pib_cli.support.external_commands.ProcessManager'
)
EXTERNAL_COMMANDS_SYS_EXIT = 'pib_cli.support.external_commands.sys.exit'
EXTERNAL_COMMANDS = 'pib_cli.support.external_commands.ExternalCommands'

PROCESS_MANAGER_OS_ENVIRON = 'pib_cli.support.processes.os.environ'
PROCESS_MANAGER_OS_SYSTEM = 'pib_cli.support.processes.os.system'
PROCESS_MANAGER_SPAWN_SINGLE = (
    'pib_cli.support.processes.ProcessManager.spawn_single'
)
