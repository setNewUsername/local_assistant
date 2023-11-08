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
        self.commands = {}

    @logMethodToFile('adding new command')
    def addCommand(self, commandData: dict[str, str]) -> None:
        print(commandData['uuid'])
        self.commands[commandData['uuid']] = self.createCommand(commandData)

    @logMethodToFile('calling command by id')
    def callCommandByUuid(self, uuid: str) -> None:
        self.commands[uuid].execute()

    @logMethodToFile('creating command')
    def createCommand(self, data: dict[str, str]) -> BaseCommand:
        match data['type']:
            case CommandTypes.CALL_PROG.value:
                return self.createCallProgCommand(data)
            case CommandTypes.SYS_COMMAND.value:
                return self.createSysCommand(data)

    @logMethodToFile('creating programm call programm')
    def createCallProgCommand(self,
                              data: dict[str, str]) -> CallProgrammCommand:
        return CallProgrammCommand(data['uuid'],
                                   CommandTypes.CALL_PROG,
                                   data['prog_path'],
                                   data['prog_args'])

    @logMethodToFile('creating system command')
    def createSysCommand(self,
                         data: dict[str, str]) -> CallProgrammCommand:
        return SysCommand(data['uuid'],
                          CommandTypes.SYS_COMMAND,
                          data['sys_command'])

    def serializeCommands(self) -> list:
        result: list = []

        for cmd in self.commands:
            result.append(self.commands[cmd].serialize())

        return result
