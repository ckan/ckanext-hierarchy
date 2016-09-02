import ckan.plugins as p


def group_tree(type_='organization'):
    return p.toolkit.get_action('group_tree')({}, {'type': type_})


def group_tree_section(id_, type_='organization', include_parents=True, include_siblings=True):
    return p.toolkit.get_action('group_tree_section')(
        {'include_parents':include_parents, 'include_siblings':include_siblings}, {'id': id_, 'type': type_,})

def group_tree_parents(id_, type_='organization'):
     tree_node =  p.toolkit.get_action('organization_show')({},{'id':id_})
     if (tree_node['groups']):
         parent_id = tree_node['groups'][0]['name']
         parent_node =  p.toolkit.get_action('organization_show')({},{'id':parent_id})
         return group_tree_parents(parent_id) + [parent_node]
     else:
         return []


def group_tree_get_longname(id_, default="", type_='organization'):
     tree_node =  p.toolkit.get_action('organization_show')({},{'id':id_})
     longname = tree_node.get("longname", default)
     if not longname:
         return default
     return longname


