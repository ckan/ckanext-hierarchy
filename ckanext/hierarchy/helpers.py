import ckan.plugins as p
import ckan.model as model

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

def group_tree_highlight(organizations, group_tree_list):

    def traverse_highlight(group_tree, name_list):
        if group_tree.get('name', "") in name_list:
            group_tree['highlighted'] = True
        for child in group_tree.get('children', []):
            traverse_highlight(child, name_list)

    selected_names = [ o.get('name',None) for o in organizations]
    print(selected_names)

    for group in group_tree_list:
        traverse_highlight(group, selected_names)
    return group_tree_list

def get_allowable_parent_groups(group_id):
    if group_id:
        group = model.Group.get(group_id)
        allowable_parent_groups = \
            group.groups_allowed_to_be_its_parent(type='organization')
    else:
        allowable_parent_groups = model.Group.all(
            group_type='organization')
    return allowable_parent_groups
