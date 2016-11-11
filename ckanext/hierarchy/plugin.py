import ckan.plugins as p
from ckanext.hierarchy.logic import action
from ckanext.hierarchy import helpers
from ckan.lib.plugins import DefaultOrganizationForm
from ckan.lib.plugins import DefaultGroupForm
import ckan.logic.schema as s
from ckan.common import c, request
import logging
import re

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
    p.implements(p.IPackageController, inherit=True)

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
                'is_include_children_selected': helpers.is_include_children_selected,
                }


    # IPackageController
    # Modify the search query to include the datasets from
    # the children organizations in the result list
    def before_search(self, search_params):

        ''' If include children selected the query string is modified '''

        def _children_name_list(children):
            name_list = []
            for child in children:
                name = child.get('name', "")
                name_list += [name] + _children_name_list(child.get('children', []))
            return name_list

        query = search_params.get('q', None)
        c.include_children_selected = False

        # fix the issues with multiple times repeated fields
        # remove the param from the fields
        new_fields = set()
        for field,value in c.fields:
            if (field != 'include_children'):
                new_fields.add((field,value))
        c.fields = list(new_fields)

        # parse the query string to check if children are requested
        if query:
            base_query = []
            #  remove whitespaces between fields and values
            query = re.sub(': +', ':',  query)
            for item in query.split(' '):
                field = item.split(':')[0]
                value = item.split(':')[-1]
                # skip organization 
                if (field == 'owner_org'):
                    org_id = value
                    continue
                # skip include children andset option value
                if (field == 'include_children'):
                    if (value.upper() != "FALSE"):
                        c.include_children_selected = True
                    continue
                base_query += [item]
        if c.include_children_selected:
            # add all the children organizations in an 'or' join
            children = _children_name_list(helpers.group_tree_section(c.group_dict.get('id'), include_parents=False, include_siblings=False).get('children',[]))
            if(children):
                search_params['q'] = " ".join(base_query)
                if (len(search_params['q'].strip())>0):
                    search_params['q'] += ' AND '
                search_params['q'] += '(organization:%s' % c.group_dict.get('name')
                for name in children:
                    if name:
                        search_params['q'] += ' OR organization:%s' %  name
                search_params['q'] += ")"
            # add it back to fields
            c.fields += [('include_children','True')]

        return search_params


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
