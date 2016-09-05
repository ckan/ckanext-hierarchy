import sys

import ckan.model as model
import ckan.logic as logic
import ckan.lib.maintain as maintain
import helpers as hierarchy_helpers
from ckan.common import c, _, g, request, OrderedDict
import ckan.lib.helpers as h
import ckan.authz as authz
import ckan.lib.search as search

import ckan.controllers.organization as organization


import logging

log = logging.getLogger(__name__)
get_action = logic.get_action

def _children_name_list(children):
     name_list = []
     for child in children:
         name = child.get('name', "")
         name_list += [name] + _children_name_list(child.get('children', []))
     return name_list


class HierarchyOrganizationController(organization.OrganizationController):
    def _read(self, id, limit, group_type):

        c.include_children_selected = False

        if c.group_dict.get('is_organization'):
            ''' This is common code used by both read and bulk_process'''
            context = {'model': model, 'session': model.Session,
                       'user': c.user or c.author,
                       'schema': self._db_to_form_schema(group_type=group_type),
                       'for_view': True, 'extras_as_string': True}

            q = c.q = request.params.get('q', '')

            # Search within subgroups
            if request.params.get('_include_children'):
                c.include_children_selected = True
                log.debug("Include Subgroups: " + str( request.params.get('_include_children')))
                children = _children_name_list(hierarchy_helpers.group_tree_section( c.group_dict.get('id'), include_parents=False, include_siblings=False).get('children',[]))
                if(children):
                    if (len(q.strip())>0):
                        q += ' AND '
                    q += '(organization:%s' % c.group_dict.get('name')
                    for name in children:
                        if name:
                            q += ' OR organization:%s' %  name
                    q += ")"
                    c.description_formatted = \
                        h.render_markdown(c.group_dict.get('description'))

                    context['return_query'] = True

                    # c.group_admins is used by CKAN's legacy (Genshi) templates only,
                    # if we drop support for those then we can delete this line.
                    c.group_admins = authz.get_group_or_org_admin_ids(c.group.id)

                    page = self._get_page_number(request.params)

                    # most search operations should reset the page counter:
                    params_nopage = [(k, v) for k, v in request.params.items()
                                     if k != 'page']
                    sort_by = request.params.get('sort', None)

                    def search_url(params):
                        controller = lookup_group_controller(group_type)
                        action = 'bulk_process' if c.action == 'bulk_process' else 'read'
                        url = h.url_for(controller=controller, action=action, id=id)
                        params = [(k, v.encode('utf-8') if isinstance(v, basestring)
                                   else str(v)) for k, v in params]
                        return url + u'?' + urlencode(params)

                    def drill_down_url(**by):
                        return h.add_url_param(alternative_url=None,
                                               controller='group', action='read',
                                               extras=dict(id=c.group_dict.get('name')),
                                               new_params=by)

                    c.drill_down_url = drill_down_url

                    def remove_field(key, value=None, replace=None):
                        return h.remove_url_param(key, value=value, replace=replace,
                                                  controller='group', action='read',
                                                  extras=dict(id=c.group_dict.get('name')))

                    c.remove_field = remove_field

                    def pager_url(q=None, page=None):
                        params = list(params_nopage)
                        params.append(('page', page))
                        return search_url(params)

                    try:
                        c.fields = []
                        search_extras = {}
                        for (param, value) in request.params.items():
                            if not param in ['q', 'page', 'sort'] \
                                    and len(value) and not param.startswith('_'):
                                if not param.startswith('ext_'):
                                    c.fields.append((param, value))
                                    q += ' %s: "%s"' % (param, value)
                                else:
                                    search_extras[param] = value

                        fq = 'capacity:"public"'
                        user_member_of_orgs = [org['id'] for org
                                               in h.organizations_available('read')]

                        if (c.group and c.group.id in user_member_of_orgs):
                            fq = ''
                            context['ignore_capacity_check'] = True

                        facets = OrderedDict()

                        default_facet_titles = {'organization': _('Organizations'),
                                                'groups': _('Groups'),
                                                'tags': _('Tags'),
                                                'res_format': _('Formats'),
                                                'license_id': _('Licenses')}

                        for facet in g.facets:
                            if facet in default_facet_titles:
                                facets[facet] = default_facet_titles[facet]
                            else:
                                facets[facet] = facet

                        # Facet titles
                        self._update_facet_titles(facets, group_type)

                        if 'capacity' in facets and (group_type != 'organization' or
                                                     not user_member_of_orgs):
                            del facets['capacity']

                        c.facet_titles = facets

                        data_dict = {
                            'q': q,
                            'fq': fq,
                            'facet.field': facets.keys(),
                            'rows': limit,
                            'sort': sort_by,
                            'start': (page - 1) * limit,
                            'extras': search_extras
                        }

                        context_ = dict((k, v) for (k, v) in context.items()
                                        if k != 'schema')
                        query = get_action('package_search')(context_, data_dict)

                        c.page = h.Page(
                            collection=query['results'],
                            page=page,
                            url=pager_url,
                            item_count=query['count'],
                            items_per_page=limit
                        )

                        c.group_dict['package_count'] = query['count']
                        c.facets = query['facets']
                        maintain.deprecate_context_item('facets',
                                                        'Use `c.search_facets` instead.')

                        c.search_facets = query['search_facets']
                        c.search_facets_limits = {}
                        for facet in c.facets.keys():
                            limit = int(request.params.get('_%s_limit' % facet,
                                                           g.facets_default_number))
                            c.search_facets_limits[facet] = limit
                        c.page.items = query['results']

                        c.sort_by_selected = sort_by

                    except search.SearchError, se:
                        log.error('Group search error: %r', se.args)
                        c.query_error = True
                        c.facets = {}
                        c.page = h.Page(collection=[])

                    self._setup_template_variables(context, {'id': id},
                                                   group_type=group_type)
                    return
        return super(HierarchyOrganizationController, self)._read(id, limit, group_type)
