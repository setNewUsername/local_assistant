import os
from core.modules.commandsController.commands.baseCommand import BaseCommand


class SysCommand(BaseCommand):
    systemCommand: str = None

    def __init__(self, uuid: str, type, sysCmd: str) -> None:
        super().__init__(uuid, type)

        self.systemCommand = sysCmd

    def execute(self) -> bool:
        os.system(self.systemCommand)

    def serialize(self) -> dict[str, str]:
        data = super().serialize()
        data.update({
            'sys_command': self.systemCommand
        })
        return data
