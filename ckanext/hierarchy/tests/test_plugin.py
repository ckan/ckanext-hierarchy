import nose.tools
from bs4 import BeautifulSoup

from ckan.tests import helpers, factories
from ckan import model


eq = nose.tools.assert_equals


class TestOrgPage(helpers.FunctionalTestBase):

    def test_search_parent_including_children(self):
        parent_org, child_org, parent_dataset, child_dataset = \
            create_fixtures()

        app = self._get_test_app()
        response = app.get(
            url='/organization/parent_org?include_children=True')

        search_results = scrape_search_results(response)
        eq(search_results, set(('parent', 'child')))

    def test_search_parent_excluding_children(self):
        parent_org, child_org, parent_dataset, child_dataset = \
            create_fixtures()

        app = self._get_test_app()
        response = app.get(
            url='/organization/parent_org')

        search_results = scrape_search_results(response)
        eq(search_results, set(('parent',)))

    def test_search_child_including_children(self):
        parent_org, child_org, parent_dataset, child_dataset = \
            create_fixtures()

        app = self._get_test_app()
        response = app.get(
            url='/organization/child_org?include_children=True')

        search_results = scrape_search_results(response)
        eq(search_results, set(('child',)))


def scrape_search_results(response):
    soup = BeautifulSoup(response.body)
    dataset_names = set()
    for dataset_li in soup.find_all('li', class_='dataset-item'):
        dataset_names.add(dataset_li.find('a')['href'].split('/')[-1])
    return dataset_names


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


def create_fixtures():
    parent_org = factories.Organization(name='parent_org', title='Parent')
    child_org = factories.Organization(name='child_org', title='child')
    member = model.Member(
        group=model.Group.get(child_org['id']),
        table_id=parent_org['id'], table_name='group', capacity='parent')
    model.Session.add(member)
    model.Session.commit()
    parent_dataset = factories.Dataset(name='parent', title='Parent',
                                       owner_org=parent_org['id'])
    child_dataset = factories.Dataset(name='child', title='Child',
                                      owner_org=child_org['id'])
    factories.Dataset(name='decoy', title='Decoy')
    return parent_org, child_org, parent_dataset, child_dataset
