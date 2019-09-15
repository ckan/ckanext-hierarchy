'''Tests that this extension doesn't break unrelated things'''

import nose.tools

from ckan.tests import helpers

from common import create_fixtures

eq = nose.tools.assert_equals


class TestSearchApi(object):
    def setup(self):
        helpers.reset_db()

    def test_package_search_is_unaffected(self):
        parent_org, child_org, parent_dataset, child_dataset = \
            create_fixtures()

        # package_search API is unaffected by ckanext-hierarchy (only searches
        # via the front-end are affected)
        package_search_result = helpers.call_action(
            'package_search',
            fq='owner_org:{}'.format(parent_org['id']))
        search_results = \
            [result['name'] for result in package_search_result['results']]

        eq(set(search_results), set(('parent',)))


class TestPages(helpers.FunctionalTestBase):
    def setup(self):
        helpers.reset_db()

    def test_home_page(self):
        parent_org, child_org, parent_dataset, child_dataset = \
            create_fixtures()

        app = self._get_test_app()
        app.get(url='/')
