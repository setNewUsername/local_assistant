import subprocess
import threading
from core.modules.commandsController.commands.baseCommand import BaseCommand


class CallProgrammCommand(BaseCommand):

    programmPath: str = None
    programmArgs: list[str] = None

    def __init__(self, uuid: str,
                 type,
                 progPath: str,
                 progArgs: list[str] = []) -> None:
        super().__init__(uuid, type)

        self.programmArgs = progArgs
        self.programmPath = progPath

    def run(self) -> None:
        subprocess.run([self.programmPath, ' '.join(self.programmArgs)],
                       capture_output=True)

    def execute(self) -> bool:
        th = threading.Thread(target=self.run)
        th.start()

    def serialize(self) -> dict[str, str]:
        data = super().serialize()
        data.update({
            'prog_path': self.programmPath,
            'prog_args': self.programmArgs
        })
        return data
