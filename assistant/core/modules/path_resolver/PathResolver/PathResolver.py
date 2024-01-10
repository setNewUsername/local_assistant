import os
from pocketsphinx import get_model_path


class PathResolver:
    # data storage dirs
    dataStorageDirName: str = 'data_storage'
    localDataStorageDirName: str = 'local_storage'
    dbDataStorageDirName: str = 'db'

    dbSQLDirName: str = 'sql_querries'
    dbSQLCreateViewsDirName: str = 'create_views'
    # data storage dirs

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

    # returns full path of 3d_parth dir
    # example: root dir -> D:\prj\local_projects\local_assistant\assistant\
    # result: D:\prj\local_projects\local_assistant\3d_party
    def get3dParthPath(self) -> str:
        return os.path.join(
            self.rootAssistantFolderPath.removesuffix('assistant'),
            '3d_party')

    def getModelDictDir(self) -> str:
        return get_model_path()

    def getGrammarFileDir(self) -> str:
        return get_model_path()

    def getModelPath(self) -> str:
        return get_model_path()

    # returns full path of sql querries
    # example: root dir -> D:\prj\local_projects\local_assistant\assistant\
    # result: D:\prj\local_projects\local_assistant\assistant\data_storage\db\sql_querries
    def getSQLQuerryDir(self) -> str:
        return os.path.join(self.getDBDataStoragePath(), self.dbSQLDirName)

    # returns full path of sql querries for view creation
    # example: root dir -> D:\prj\local_projects\local_assistant\assistant\
    # result: D:\prj\local_projects\local_assistant\assistant\data_storage\db\sql_querries\create_view
    def getSQLCreateViewsDir(self) -> str:
        return os.path.join(self.getSQLQuerryDir(), self.dbSQLCreateViewsDirName)
