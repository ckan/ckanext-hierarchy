# ckanext-hierarchy - Organization hierarchy for CKAN

Organizations can be arranged into a tree hierarchy.

This new hierarchical arrangement of organizations is displayed
using templates in this extension, instead of the usual list:
![Screenshot of organizations page](screenshots/orgs_page.png)

Provides a new field on the organization edit form to select a parent
organization:
![Screenshot of organization edit page](screenshots/org_edit.png)

When viewing an organization you see its context within the tree in the side bar. In addition you can widen search of the organization's datasets to include datasets in sub-organizations too:
![Screenshot of organization page](screenshots/org_page.png)

## Detail

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

In order to make hierarchy work with ckanext-scheming you need to enable just
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

This extension requires CKAN v2.7 or later.

## Installation

Install the extension in your python environment
```
$ . /usr/lib/ckan/default/bin/activate
(pyenv) $ cd /usr/lib/ckan/default/src
(pyenv) $ pip install -e "git+https://github.com/davidread/ckanext-hierarchy.git#egg=ckanext-hierarchy"
```
Then change your CKAN ini file (e.g. development.ini or production.ini).  Note that hierarchy_display
should come before hierarchy_form
```
ckan.plugins = stats text_view recline_view ... hierarchy_display hierarchy_form
```

## Licence and copyright

This module is openly licensed with AGPLv3 - see LICENSE file.

Copyright belongs to commit authors. Commits 2013-2017 by @davidread are Crown Copyright.

