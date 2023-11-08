class ConfigFile:
    fileName: str = None
    mode: str = None

    def __init__(self, filename, mode) -> None:
        self.fileName = filename
        self.mode = mode

    def __enter__(self):
        self.file = open(self.fileName, self.mode)
        return self.file

    def __exit__(self, type, value, traceback):
        self.file.close()
