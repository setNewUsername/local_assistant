import peewee
from enum import Enum
import os
from core.modules.logger.logFuncs import LogClient
from core.modules.logger.logFuncs import logMethodToFile


class DBViewEnum(Enum):
    COMMANDS_FULL_DATA = 'commands_full_data'
    DOMAINS_FULL_DATA = 'domains_full_data'


class ViewsController(LogClient):
    dbConnDescriptor: peewee.Database

    createViewsDir: str = None

    upprovedViews: list[str] = None

    def __init__(self, db, CVDir: str, logFile) -> None:
        super().__init__(logFile)
        self.loggerRegister()
        self.dbConnDescriptor = db
        self.createViewsDir = CVDir
        self.upprovedViews = []

    @logMethodToFile('creating views from file')
    def createViewFromSQLFiles(self) -> None:
        enumValues = list(map(lambda c: c.value, DBViewEnum))
        for file in os.listdir(self.createViewsDir):
            self.innerLogToFile(f'processing file {file}')
            if file.removesuffix('.sql') in enumValues:
                self.innerLogToFile('found view in views-list; creating')
                with open(os.path.join(self.createViewsDir, file), 'r') as input:
                    try:
                        viewName = file.removesuffix(".sql")
                        self.dbConnDescriptor.execute_sql(f'CREATE OR REPLACE VIEW public.{viewName} AS {input.read()} ALTER TABLE public.{viewName} OWNER TO local_assistant_db_user;')
                    except Exception as e:
                        self.innerLogToFile(f'error occured through view-table creation; {e}')
                    else:
                        self.innerLogToFile(f'view created: {file.removesuffix(".sql")}')
                        self.upprovedViews.append(file.removesuffix('.sql'))

    @logMethodToFile('executing query to specified view')
    def queryToView(self, query: str):
        result = ''

        try:
            result = self.dbConnDescriptor.execute_sql(query)
        except Exception as e:
            self.innerLogToFile(f'error occured through view-table query execution process; {e}')
        else:
            self.innerLogToFile('query completed')

        return result
