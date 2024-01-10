from core.modules.logger.logFuncs import LogClient
from core.modules.logger.logFuncs import logMethodToFile
import json
import os
import peewee


# database connection interface
class dbConnRunnerInterface:
    def __init__(self) -> None:
        pass

    # connects to DB by conn file
    # returns connection descriptor
    def connectToDb(self):
        ...

    def disconnect(self) -> None:
        ...


# database connection interface for remote databases
class remoteDBConnRunnerInterface(dbConnRunnerInterface):
    configsDir = 'connection_configs'
    connectionMandatoryFile: str = None

    def __init__(self) -> None:
        super().__init__()


# database connector for PostgreSQL databases
class dbConnRunnerPGSQL(LogClient, remoteDBConnRunnerInterface):
    connectionDescriptor = None

    def __init__(self, logFile, dataStorateDir, connFile) -> None:
        super().__init__(logFile)
        self.loggerRegister()
        self.connectionMandatoryFile = os.path.join(os.path.join(dataStorateDir, self.configsDir), connFile)

    # uses peewee connection class
    @logMethodToFile('connecting to PostgreSQL database')
    def connectToDb(self):
        with open(self.connectionMandatoryFile, 'r') as connFile:
            connData = json.load(connFile)
            self.innerLogToFile(f'conneting to server: {connData["server_ip"]}, db: {connData["db"]}...')
            self.connectionDescriptor = peewee.PostgresqlDatabase(
                    connData['db'],
                    user=connData['user'],
                    password=connData['password'],
                    host=connData['server_ip'],
                    port=connData['port']
                )
            try:
                self.connectionDescriptor.connect()
            except Exception as e:
                self.innerLogToFile(f'connection failed: {e}')
            else:
                self.innerLogToFile(f'connection established to server: {connData["server_ip"]}, db: {connData["db"]}')
            return self.connectionDescriptor

    @logMethodToFile('connection to PostgreSQL closed')
    def disconnect(self) -> None:
        self.connectionDescriptor.close()
