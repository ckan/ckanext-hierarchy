# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup


class TestOrgPage(object):

    def test_search_parent_including_children(self, data_tree, app):
        parent_org, child_org, parent_dataset, child_dataset = data_tree
        response = app.get(
            url='/organization/parent_org?ext_include_children=True')

        search_results = scrape_search_results(response)
        assert(search_results == set(('parent', 'child')))

    def test_search_parent_excluding_children(self, data_tree, app):
        parent_org, child_org, parent_dataset, child_dataset = data_tree
        response = app.get(
            url='/organization/parent_org')

        search_results = scrape_search_results(response)
        assert(search_results == set(('parent',)))

    def test_search_child_including_children(self, data_tree, app):
        parent_org, child_org, parent_dataset, child_dataset = data_tree
        response = app.get(
            url='/organization/child_org?ext_include_children=True')

        search_results = scrape_search_results(response)
        assert(search_results == set(('child',)))


def scrape_search_results(response):
    soup = BeautifulSoup(response.body)
    dataset_names = set()
    for dataset_li in soup.find_all('li', class_='dataset-item'):
        dataset_names.add(dataset_li.find('a')['href'].split('/')[-1])
    return dataset_names
