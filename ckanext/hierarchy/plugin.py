import ckan.plugins as p
from ckanext.hierarchy.logic import action
from ckanext.hierarchy import helpers
from ckan.lib.plugins import DefaultOrganizationForm
from ckan.lib.plugins import DefaultGroupForm
import ckan.logic.schema as s

import logging

log = logging.getLogger(__name__)

# This plugin is designed to work only these versions of CKAN
p.toolkit.check_ckan_version(min_version='2.0')

def custom_convert_from_extras(key, data, errors, context):

    '''Converts values from extras, tailored for groups.'''

    # Set to empty string to remove Missing objects
    data[key] = ""

    to_remove = []
    for data_key in data.keys():
        if (data_key[0] == 'extras'):
            data_value = data[data_key]
            if( 'key' in data_value and data_value['key'] == key[-1]):
               data[key] = data_value['value']
               to_remove.append(data_key)
               break
    else:
        return

    for remove_key in to_remove:
        del data[remove_key]

class HierarchyDisplay(p.SingletonPlugin):

    p.implements(p.IConfigurer, inherit=True)
    p.implements(p.IActions, inherit=True)
    p.implements(p.ITemplateHelpers, inherit=True)
    p.implements(p.IRoutes, inherit=True)

    # IConfigurer

    def update_config(self, config):
        p.toolkit.add_template_directory(config, 'templates')
        p.toolkit.add_template_directory(config, 'public')
        p.toolkit.add_resource('public/scripts/vendor/jstree', 'jstree')
        p.toolkit.add_resource('fanstatic', 'hierarchy')

    # IActions

    def get_actions(self):
        return {'group_tree': action.group_tree,
                'group_tree_section': action.group_tree_section,
                }

    # ITemplateHelpers
    def get_helpers(self):
        return {'group_tree': helpers.group_tree,
                'group_tree_section': helpers.group_tree_section,
                'group_tree_parents': helpers.group_tree_parents,
                'group_tree_get_longname': helpers.group_tree_get_longname,
                'group_tree_highlight': helpers.group_tree_highlight,
                'get_allowable_parent_groups': helpers.get_allowable_parent_groups,
                }


    # IRouter
    # Redirect organization_read /organization/{id} to custom controller
    # to include the datasets from the children organizations in the list

    def before_map(self, map):
        map.connect('organization_read', '/organization/{id}',
                     controller='ckanext.hierarchy.controller:HierarchyOrganizationController',
                     action='read')
        return map


class HierarchyForm(p.SingletonPlugin, DefaultOrganizationForm):

    p.implements(p.IGroupForm, inherit=True)


    # IGroupForm

    def group_types(self):
        return ('organization',)

    def group_controller(self):
        return 'organization'

    def setup_template_variables(self, context, data_dict):
        from pylons import tmpl_context as c

        group_id = data_dict.get('id')
        c.allowable_parent_groups = helpers.get_allowable_parent_groups(group_id)
