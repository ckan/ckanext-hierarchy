#!/bin/bash
set -e

pytest --ckan-ini=subdir/test.ini --cov=ckanext.hierarchy ckanext/hierarchy/tests
