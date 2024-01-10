select command_uuid, field_data, field_name, type_name from commands
inner join commands_data
on commands_data.command_id = commands.id
inner join command_fields_data
on commands_data.field_data_id = command_fields_data.id
inner join command_types_fields
on command_fields_data.command_type_field_id = command_types_fields.id
inner join command_types
on commands.command_type_id = command_types.id;