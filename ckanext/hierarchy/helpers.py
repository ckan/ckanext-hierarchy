from ckan.plugins import toolkit


def group_tree():
    return toolkit.get_action('group_tree')()