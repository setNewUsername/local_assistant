import peewee
from peewee import Model
from core.models.modeInterface import ModelInterface
from core.modules.modelsController.viewsController import ViewsController, DBViewEnum


class CommandType(peewee.Model, ModelInterface):
    type_name = peewee.TextField(unique=True)

    class Meta:
        db_table = 'command_types'

    @staticmethod
    def fromJSONtoDB(jsonData, fgKey: peewee.Model = None):
        # not strict adding skip
        newComType = ModelInterface.addIfNone(CommandType, CommandType.type_name, jsonData['type'], type_name=jsonData['type'])
        # not strict adding skip

        Command.fromJSONtoDB(jsonData, newComType)
        CommandTypesFields.fromJSONtoDB(jsonData, newComType)


class CommandTypesFields(peewee.Model, ModelInterface):
    command_type = peewee.ForeignKeyField(CommandType)
    field_name = peewee.TextField(unique=True)

    class Meta:
        db_table = 'command_types_fields'

    @staticmethod
    def fromJSONtoDB(jsonData: dict[str, str], fgKey: peewee.Model):
        for datK in jsonData.keys():
            if datK not in ['type', 'uuid']:
                # not strict adding skip
                newComTypeF = ModelInterface.addIfNone(CommandTypesFields,
                                                       CommandTypesFields.field_name,
                                                       datK,
                                                       field_name=datK,
                                                       command_type=fgKey)
                # not strict adding skip

                CommandFieldsData.fromJSONtoDB(jsonData[datK], newComTypeF, jsonData['uuid'])


class CommandFieldsData(peewee.Model, ModelInterface):
    command_type_field = peewee.ForeignKeyField(CommandTypesFields)
    field_data = peewee.TextField()

    class Meta:
        db_table = 'command_fields_data'

    @staticmethod
    def fromJSONtoDB(data: str, fgKey: peewee.Model, commandUUID: str):
        # check if pare already exists
        # transfer string to list
        if type(data) is not list:
            data = [data]
        # check count for all of list members
        for dat in data:
            checkData: peewee.ModelSelect = CommandFieldsData.select().where(CommandFieldsData.command_type_field == fgKey.get_id(), CommandFieldsData.field_data == dat)
            if checkData.count() == 0:
                newComFieldData = CommandFieldsData(command_type_field=fgKey, field_data=dat)
                newComFieldData.save()
                cmd = Command.get(Command.command_uuid == commandUUID)
                CommandsData.fromJSONtoDB(cmd, newComFieldData)


class Command(peewee.Model, ModelInterface):
    command_type = peewee.ForeignKeyField(CommandType)
    command_uuid = peewee.TextField(unique=True)

    class Meta:
        db_table = 'commands'

    @staticmethod
    def fromJSONtoDB(jsonData: dict[str, str], fgKey: peewee.Model):
        ModelInterface.addIfNone(Command,
                                 Command.command_uuid,
                                 jsonData['uuid'],
                                 command_type=fgKey,
                                 command_uuid=jsonData['uuid'])

    @staticmethod
    def fromDBtoJSON(cmdUUID: str, viewController: ViewsController) -> dict:
        result = {
            'uuid': cmdUUID
        }

        dbData = viewController.queryToView(f"select * from {DBViewEnum.COMMANDS_FULL_DATA.value} where command_uuid = '{cmdUUID}'")
        # fill command type
        for row in dbData:
            result['type'] = row[3]
            if row[2] in result:
                if type(result[row[2]]) is list:
                    result[row[2]].append(row[1])
                else:
                    tmp = result[row[2]]
                    result[row[2]] = []
                    result[row[2]].append(tmp)
                    result[row[2]].append(row[1])
            else:
                result[row[2]] = row[1]

        return result


class CommandsData(peewee.Model, ModelInterface):
    command = peewee.ForeignKeyField(Command)
    field_data = peewee.ForeignKeyField(CommandFieldsData)

    class Meta:
        db_table = 'commands_data'

    @staticmethod
    def fromJSONtoDB(fgKeyCmd: Model = None, fgKeyData: Model = None):
        cmdData = CommandsData(command=fgKeyCmd, field_data=fgKeyData)
        cmdData.save()
