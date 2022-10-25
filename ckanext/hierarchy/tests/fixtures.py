import pytest

from ckan.tests import factories
from ckan import model


@pytest.fixture
def initial_data():
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
