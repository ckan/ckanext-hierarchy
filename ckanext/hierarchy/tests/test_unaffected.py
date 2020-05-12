'''Tests that this extension doesn't break unrelated things'''


from ckan.tests import helpers


class TestSearchApi(object):
    def test_package_search_is_unaffected(self, data_tree, app):
        parent_org, child_org, parent_dataset, child_dataset = data_tree

        # package_search API is unaffected by ckanext-hierarchy (only searches
        # via the front-end are affected)
        package_search_result = helpers.call_action(
            'package_search',
            fq='owner_org:{}'.format(parent_org['id']))
        search_results = \
            [result['name'] for result in package_search_result['results']]

        assert(set(search_results) == set(('parent',)))


class TestPages(object):
    def test_home_page(self, data_tree, app):
        app.get(url='/')
