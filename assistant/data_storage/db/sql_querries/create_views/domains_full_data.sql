select domains.command_id, 
	   domains.domain_word, 
	   domains.domain_uuid,
	   (select domain_uuid from domains where id = domains_relations.parent_domain_id) parent_uuid
	   from domains
join domains_relations on domains.id = domains_relations.children_domain_id;