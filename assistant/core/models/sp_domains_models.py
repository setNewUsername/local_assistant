import peewee
from peewee import Model
from core.models.commands_models import Command
from core.models.modeInterface import ModelInterface
from core.modules.modelsController.viewsController import ViewsController, DBViewEnum
import core.models.commands_models as com


class Domain(peewee.Model, ModelInterface):
    command = peewee.ForeignKeyField(Command, null=True)
    domain_word = peewee.CharField()
    domain_uuid = peewee.CharField()

    class Meta:
        db_table = 'domains'

    @staticmethod
    def fromJSONtoDB(jsonData, fgKey: peewee.Model = None):

        commandObj = com.Command.get_or_none(com.Command.command_uuid == jsonData['command_uuid'])
        # not strict adding skip
        newDomain = ModelInterface.addIfNone(Domain, Domain.domain_uuid,
                                             jsonData['domain_uuid'],
                                             domain_uuid=jsonData['domain_uuid'],
                                             command=commandObj,
                                             domain_word=jsonData['domain_word'].encode('cp1251'))
        # not strict adding skip
        parentDom = Domain.get_or_none(Domain.domain_uuid == jsonData['parent_dom_uuid'])
        DomainsRel.fromJSONtoDB(newDomain, parentDom)

    @staticmethod
    def fromDBtoJSON(domUUID: str, viewController: ViewsController) -> dict:
        result = {
            'domain_uuid': domUUID
        }

        dbData = viewController.queryToView(f"select * from {DBViewEnum.DOMAINS_FULL_DATA.value} where domain_uuid = '{domUUID}'")
        for row in dbData:
            result['domain_word'] = row[1]
            result['parent_dom_uuid'] = row[3]
            command = com.Command.get_or_none(id=row[0])
            result['command_uuid'] = None if command is None else command.command_uuid
        return result


class DomainsRel(peewee.Model, ModelInterface):
    children_domain = peewee.ForeignKeyField(Domain, related_name='children')
    parent_domain = peewee.ForeignKeyField(Domain, related_name='parent', null=True)

    class Meta:
        db_table = 'domains_relations'

    @staticmethod
    def fromJSONtoDB(dom: Model = None, parentDom: Model = None):
        check = DomainsRel.get_or_none(DomainsRel.children_domain == dom, DomainsRel.parent_domain == parentDom)
        if check is None:
            domRel = DomainsRel(children_domain=dom, parent_domain=parentDom)
            domRel.save()
