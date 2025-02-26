# CKAN Hierarchy extension Changelog

## 1.2.2

New features:
 - Test for CKAN 2.11, drop support for CKAN 2.9 [#72](https://github.com/ckan/ckanext-hierarchy/pull/72)
   + [#70](https://github.com/ckan/ckanext-hierarchy/pull/70)

Bug fixes:
 - Add missing webassets [#71](https://github.com/ckan/ckanext-hierarchy/pull/71)

## 1.2.1

New features:
 - Prepare extension for CKAN 2.10 [#61](https://github.com/ckan/ckanext-hierarchy/pull/61)
Bug Fixes:
 - Avoid using custom _show_ functions for custom group types.
   We always use `organization_show` and `group_show` functions now.
   [#64](https://github.com/ckan/ckanext-hierarchy/pull/64).
 - Several fixes for custom group types

## 1.2.0

New features:
 - Add sub groups [#55](https://github.com/ckan/ckanext-hierarchy/pull/55)
 - Frontend and templates improvements.
