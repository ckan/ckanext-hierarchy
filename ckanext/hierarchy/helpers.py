import ckan.plugins as p
import ckan.model as model

def group_tree(type_='organization'):
    return p.toolkit.get_action('group_tree')({}, {'type': type_})


def group_tree_section(id_, type_='organization'):
    return p.toolkit.get_action('group_tree_section')(
        {}, {'id': id_, 'type': type_})


def get_allowable_parent_groups(group_id):
    if group_id:
        group = model.Group.get(group_id)
        allowable_parent_groups = \
            group.groups_allowed_to_be_its_parent(type='organization')
    else:
        allowable_parent_groups = model.Group.all(
            group_type='organization')
    return allowable_parent_groups
