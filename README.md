# ckanext-hierarchy - Organization hierarchy for CKAN

Provides a new field on the organization edit form to select a parent
organization. This new hierarchical arrangement of organizations is displayed
using templates in this extension, instead of the usual list. An organization
page also displays the section of the tree that it is part of, under the
'About' tab.

Forms (hierachy_form plugin):
* /organization/new
* /organization/edit/{id}

Templates (hierarchy_display plugin):
* /organization - now shows the organization hierarchy instead of list
* /organization/about/{id} - now also shows the relevant part of the hierarchy

Snippets (used by hierarchy_display and ckanext-scheming):
* /scheming/form_snippets/org_hierarchy.html

You can use this extension with CKAN as it is, enabling both plugins. Or if you
use an extension to customise the form already with an IGroupForm, then you
will want to only use the hierarchy_display plugin, and copy bits of the
hierarchy_form into your own. If you have your own templates then you can use
the snippets (or logic functions) that this extension provides to display the
trees.

In order to make hierarchy works with ckanext-scheming you need to enable just
hierarchy_display and then use corresponding form_snippet in your org_schema.
For example, you may add next field:
```
{
    "field_name": "not_used",
    "label": "Parent organization",
    "display_snippet": null,
    "form_snippet": "org_hierarchy.html",
    "validators": "ignore_missing"
}
```

Optionally one could also specify a full name and leave the field 'title' for
the short name or acronym (more convenient for  display).
```
{
    "field_name": "longname",
    "label": "Full Name",
    "validators": "ignore_missing unicode",
    "form_snippet": "large_text.html",
    "form_attrs": {"data-module": "slug-preview-target"},
    "form_placeholder": "My Organization full name",
    "display_snippet": null
}
```



TODO:
* make the trees prettier with JSTree

## Compatibility

This extension requires CKAN v2.2 or later. Specifically it uses these changes CKAN: https://github.com/ckan/ckan/pull/1247/files

## Installation

Install the extension in your python environment
```
$ . /usr/lib/ckan/default/bin/activate
(pyenv) $ cd /usr/lib/ckan/default/src
(pyenv) $ pip install -e "git+https://github.com/datagovuk/ckanext-hierarchy.git#egg=ckanext-hierarchy"
```
Then change your CKAN ini file (e.g. development.ini or production.ini).  Note that hierarchy_display
should come before hierarchy_form
```
ckan.plugins = stats text_view recline_view ... hierarchy_display hierarchy_form
```

## Copyright & Licence

This module is Crown Copyright 2013 and openly licensed with AGPLv3 - see LICENSE file.
