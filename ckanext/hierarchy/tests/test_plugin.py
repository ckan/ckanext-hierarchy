import pytest
from bs4 import BeautifulSoup


@pytest.mark.usefixtures('clean_db', 'clean_index', 'with_request_context')
class TestOrgPage():

    def test_search_parent_including_children(self, initial_data, app):
        parent_org, child_org, parent_dataset, child_dataset = \
            initial_data

        response = app.get(
            url='/organization/parent_org?include_children=True')

        search_results = scrape_search_results(response)
        assert search_results == set(('parent', 'child'))

    def test_search_parent_excluding_children(self, initial_data, app):
        parent_org, child_org, parent_dataset, child_dataset = \
            initial_data

        response = app.get(
            url='/organization/parent_org')

        search_results = scrape_search_results(response)
        assert search_results == set(('parent',))

    def test_search_child_including_children(self, initial_data, app):
        parent_org, child_org, parent_dataset, child_dataset = \
            initial_data

        response = app.get(
            url='/organization/child_org?include_children=True')

        search_results = scrape_search_results(response)
        assert search_results == set(('child',))

    def test_org_about(self, initial_data, app):
        """ Test the about view works and show the child org """
        parent_org, child_org, _, _ = initial_data

        response = app.get(
            url='/organization/about/%s' % parent_org["name"],
            status=200,
        )

        assert str(child_org["title"]) in response.body

    def test_org_home(self, initial_data, app):
        """ Test the org home view works and show the child org """
        parent_org, child_org, _, _ = initial_data

        response = app.get(
            url='/organization/%s' % parent_org["name"],
            status=200,
        )

        assert str(child_org["title"]) in response.body


def scrape_search_results(response):
    try:
        body = response.data
    except AttributeError:
        body = response.body
    soup = BeautifulSoup(body)
    dataset_names = set()
    for dataset_li in soup.find_all('li', class_='dataset-item'):
        dataset_names.add(dataset_li.find('a')['href'].split('/')[-1])
    return dataset_names
