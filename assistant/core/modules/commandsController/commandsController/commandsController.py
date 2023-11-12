from core.modules.commandsController.commands.baseCommand import BaseCommand
from core.modules.commandsController.commands.callProgrammCommand import CallProgrammCommand
from core.modules.commandsController.commands.systemCommand import SysCommand
from core.modules.commandsController.commands.commandsEnum import CommandTypes
from core.modules.logger.logFuncs import LogClient
from core.modules.logger.logFuncs import logMethodToFile


class CommandController(LogClient):

    commands: dict[str, BaseCommand] = None

    def __init__(self, logFile) -> None:
        super().__init__(logFile)
        self.loggerRegister()
        self.commands = {}

    # adds commands from list
    @logMethodToFile('adding commands from batch')
    def addCommands(self, commandsList: list) -> None:
        for cmd in commandsList:
            self.addCommand(cmd)
    # adds commands from list

    # adds command to commands map
    @logMethodToFile('adding new command')
    def addCommand(self, commandData: dict[str, str]) -> None:
        self.commands[commandData['uuid']] = self.createCommand(commandData)
    # adds command to commands map

    # calls command by uuid
    @logMethodToFile('calling command by id')
    def callCommandByUuid(self, uuid: str) -> None:
        self.commands[uuid].execute()
    # calls command by uuid

    # creates command from command data by cmd type
    @logMethodToFile('creating command')
    def createCommand(self, data: dict[str, str]) -> BaseCommand:
        match data['type']:
            case CommandTypes.CALL_PROG.value:
                return self.createCallProgCommand(data)
            case CommandTypes.SYS_COMMAND.value:
                return self.createSysCommand(data)
    # creates command from command data by cmd type

    # creates call programm command
    @logMethodToFile('creating programm call programm')
    def createCallProgCommand(self,
                              data: dict[str, str]) -> CallProgrammCommand:
        return CallProgrammCommand(data['uuid'],
                                   CommandTypes.CALL_PROG,
                                   data['prog_path'],
                                   data['prog_args'])
    # creates call programm command

    # creates system command
    @logMethodToFile('creating system command')
    def createSysCommand(self,
                         data: dict[str, str]) -> CallProgrammCommand:
        return SysCommand(data['uuid'],
                          CommandTypes.SYS_COMMAND,
                          data['sys_command'])
    # creates system command

    # returns commands data as list
    def serializeCommands(self) -> list:
        result: list = []

        for cmd in self.commands:
            result.append(self.commands[cmd].serialize())

        return result
    # returns commands data as list
