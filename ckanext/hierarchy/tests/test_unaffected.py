'''Tests that this extension doesn't break unrelated things'''

import pytest
from ckan.tests import helpers

from common import create_fixtures


@pytest.mark.usefixtures('clean_db', 'clean_index')
class TestSearchApi():

    def test_package_search_is_unaffected(self, app):
        parent_org, child_org, parent_dataset, child_dataset = \
            create_fixtures()

        # package_search API is unaffected by ckanext-hierarchy (only searches
        # via the front-end are affected)
        package_search_result = helpers.call_action(
            'package_search',
            fq='owner_org:{}'.format(parent_org['id']))
        search_results = \
            [result['name'] for result in package_search_result['results']]

        assert set(search_results) == set(('parent',))


@pytest.mark.usefixtures('clean_db', 'clean_index')
class TestPages():

    def test_home_page(self, app):
        parent_org, child_org, parent_dataset, child_dataset = \
            create_fixtures()

        app.get(url='/')
