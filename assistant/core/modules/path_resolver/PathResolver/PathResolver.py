import os


class PathResolver:
    dataStorageDirName: str = 'data_storage'
    localDataStorageDirName: str = 'local_storage'
    dbDataStorageDirName: str = 'db'

    logDirName: str = 'logs'

    configFolderName: str = 'configuration'

    rootAssistantFolderPath: str = None

    def __init__(self) -> None:
        self.rootAssistantFolderPath = self.resolveAssistantRootFolderPath()

    # returns root dir path
    # example:
    # D:\prj\local_projects\local_assistant\assistant\core\modules\path_resolver
    # result: D:\prj\local_projects\local_assistant\assistant
    def resolveAssistantRootFolderPath(self) -> str:
        fullPath = os.path.abspath(__file__)
        startIndex = fullPath.find('core')
        result = fullPath[0:startIndex - 1]
        return result

    # returns full path of local data storage dir
    # example: root dir -> D:\prj\local_projects\local_assistant\assistant\
    # result:
    # D:\prj\local_projects\local_assistant\assistant\data_storage\local_storage
    def getLocalDataStoragePath(self) -> str:
        lclStoragePath: str = os.path.join(self.dataStorageDirName,
                                           self.localDataStorageDirName)
        return os.path.join(self.rootAssistantFolderPath, lclStoragePath)

    # returns full path of database data storage dir
    # example: root dir -> D:\prj\local_projects\local_assistant\assistant\
    # result: D:\prj\local_projects\local_assistant\assistant\data_storage\db
    def getDBDataStoragePath(self) -> str:
        dbStoragePath: str = os.path.join(self.dataStorageDirName,
                                          self.dbDataStorageDirName)
        return os.path.join(self.rootAssistantFolderPath, dbStoragePath)

    # returns full path of logs dir
    # example: root dir -> D:\prj\local_projects\local_assistant\assistant\
    # result: D:\prj\local_projects\local_assistant\assistant\logs
    def getLogsPath(self) -> str:
        return os.path.join(self.rootAssistantFolderPath, self.logDirName)

    # returns full path of configs dir
    # example: root dir -> D:\prj\local_projects\local_assistant\assistant\
    # result: D:\prj\local_projects\local_assistant\assistant\configuration
    def getConfigsPath(self) -> str:
        return os.path.join(self.rootAssistantFolderPath,
                            self.configFolderName)
