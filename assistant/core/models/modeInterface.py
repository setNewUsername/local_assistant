import peewee


class ModelInterface:

    @staticmethod
    def fromJSONtoDB(jsonData, fgKey: peewee.Model = None):
        ...

    @staticmethod
    def fromDBtoJSON() -> dict:
        ...

    @staticmethod
    def addIfNone(model: peewee.Model, getField, getFData, *args, **kwargs) -> peewee.Model:
        check = model.get_or_none(getField == getFData)
        if check is None:
            check = model(*args, **kwargs)
            check.save()
        else:
            check = model.get(getField == getFData)
        return check
