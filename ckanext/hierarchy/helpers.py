import ckan.plugins as p


def group_tree(type_='organization'):
    return p.toolkit.get_action('group_tree')({}, {'type': type_})


def group_tree_section(id_, type_='organization'):
    return p.toolkit.get_action('group_tree_section')(
        {}, {'id': id_, 'type': type_})
