import peewee
from core.modules.logger.logFuncs import LogClient
from core.modules.logger.logFuncs import logMethodToFile
from core.modules.configurationController.configurationController.configurationController import ConfigController
import core.models.commands_models as com
import core.models.sp_domains_models as dom
from core.modules.modelsController.viewsController import ViewsController


class ModelsController(LogClient):
    confCont: ConfigController = None
    viewsCont: ViewsController = None

    def __init__(self, logFile, confCont: ConfigController, vCont: ViewsController) -> None:
        super().__init__(logFile)
        self.loggerRegister()
        self.confCont = confCont
        self.viewsCont = vCont

    # uses peewee models to create tables
    @logMethodToFile('creating tables')
    def createTables(self, modelsList: list[peewee.Model], dataBase: peewee.Database) -> bool:
        try:
            for model in modelsList:
                # dynamically set database attribute to meta class object
                setattr(model._meta, 'database', dataBase)
                model.create_table()
        except Exception as e:
            self.innerLogToFile(f'error during tables creation process: {e}')
            return False
        else:
            self.innerLogToFile(f'tables created: {len(modelsList)}')
            return True

    # reads JSON config file
    # writes to DB
    def transferFromJSONtoDB(self, dataBase: peewee.Database) -> None:
        commandsData = self.confCont.getComandsData()
        # fill commands
        for comDat in commandsData:
            com.CommandType.fromJSONtoDB(comDat, dataBase)

        domainsData = self.confCont.getDomainsData()
        for domDat in domainsData:
            dom.Domain.fromJSONtoDB(domDat, dataBase)

    def transferFromDBtoJSON(self) -> dict:
        result = {
            'commands': [],
            'domains': []
        }
        # collect commands data
        cmds = com.Command.select(com.Command.command_uuid)
        for uuid in [row.command_uuid for row in cmds]:
            result['commands'].append(com.Command.fromDBtoJSON(uuid, self.viewsCont))

        doms = dom.Domain.select(dom.Domain.domain_uuid)
        for uuid in [row.domain_uuid for row in doms]:
            result['domains'].append(dom.Domain.fromDBtoJSON(uuid, self.viewsCont))

        return result
