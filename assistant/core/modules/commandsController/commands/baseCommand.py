from core.modules.commandsController.commands.commandsEnum import CommandTypes


class BaseCommand:

    commandType: str = None
    commandUuid: str = None

    def __init__(self, uuid: str, type: CommandTypes) -> None:
        self.commandUuid = uuid
        self.commandType = type.value

    def execute(self) -> bool:
        ...

    def serialize(self) -> dict[str, str]:
        return {
            'uuid': self.commandUuid,
            'type': self.commandType,
        }
