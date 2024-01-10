import peewee
from core.models.commands_models import Command


class Domain(peewee.Model):
    command = peewee.ForeignKeyField(Command)
    domain_word = peewee.CharField()
    domain_uuid = peewee.CharField()

    class Meta:
        db_table = 'domains'


class DomainsRel(peewee.Model):
    children_domain = peewee.ForeignKeyField(Domain, related_name='children')
    parent_domain = peewee.ForeignKeyField(Domain, related_name='parent')

    class Meta:
        db_table = 'domains_relations'
