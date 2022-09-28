import pytest
from bs4 import BeautifulSoup

from common import create_fixtures


@pytest.mark.usefixtures('clean_db', 'clean_index')
class TestOrgPage():

    def test_search_parent_including_children(self, app):
        parent_org, child_org, parent_dataset, child_dataset = \
            create_fixtures()

        response = app.get(
            url='/organization/parent_org?include_children=True')

        search_results = scrape_search_results(response)
        assert search_results == set(('parent', 'child'))

    def test_search_parent_excluding_children(self, app):
        parent_org, child_org, parent_dataset, child_dataset = \
            create_fixtures()

        response = app.get(
            url='/organization/parent_org')

        search_results = scrape_search_results(response)
        assert search_results == set(('parent',))

    def test_search_child_including_children(self, app):
        parent_org, child_org, parent_dataset, child_dataset = \
            create_fixtures()

        response = app.get(
            url='/organization/child_org?include_children=True')

        search_results = scrape_search_results(response)
        assert search_results == set(('child',))


def scrape_search_results(response):
    soup = BeautifulSoup(response.body)
    dataset_names = set()
    for dataset_li in soup.find_all('li', class_='dataset-item'):
        dataset_names.add(dataset_li.find('a')['href'].split('/')[-1])
    return dataset_names
