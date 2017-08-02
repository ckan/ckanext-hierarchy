from ckan.plugins import toolkit


def group_tree(organizations=[], type='organization'):
    full_tree_list = toolkit.get_action('group_tree')({}, {'type': type})

    if not organizations:
        return full_tree_list
    else:
        filtered_tree_list = group_tree_filter(organizations, full_tree_list)
        return filtered_tree_list

def group_tree_filter(organizations, group_tree_list, highlight=False):
    # this method leaves only the sections of the tree corresponding to the list
    # since it was developed for the users, all children organizations from the
    # organizations in the list are included
    def traverse_select_highlighted(group_tree, selection=[], highlight=False):
        # add highlighted branches to the filtered tree
        if group_tree['highlighted']:
            # add to the selection and remove highlighting if necessary
            if highlight:
                selection += [group_tree]
            else:
                selection += group_tree_highlight([], [group_tree])
        else:
            # check if there is any highlighted child tree
            for child in group_tree.get('children', []):
                traverse_select_highlighted(child, selection)

    filtered_tree=[]
    # first highlights all the organizations from the list in the three
    for group in group_tree_highlight(organizations, group_tree_list):
        traverse_select_highlighted(group, filtered_tree, highlight)

    return filtered_tree

def group_tree_highlight(organizations, group_tree_list):

    def traverse_highlight(group_tree, name_list):
        if group_tree.get('name', "") in name_list:
            group_tree['highlighted'] = True
        else:
            group_tree['highlighted'] = False
        for child in group_tree.get('children', []):
            traverse_highlight(child, name_list)

    selected_names = [ o.get('name',None) for o in organizations]
    print(selected_names)

    for group in group_tree_list:
        traverse_highlight(group, selected_names)
    return group_tree_list


def group_tree_section(id, type='organization', include_parents=True, include_siblings=True):
    return toolkit.get_action('group_tree_section')(
        {'include_parents':include_parents, 'include_siblings':include_siblings}, {'id': id, 'type': type,})