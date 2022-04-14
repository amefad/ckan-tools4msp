import ckan.plugins as plugins
import ckan.plugins.toolkit as toolkit

import json


class SchemasPlugin(plugins.SingletonPlugin):
    plugins.implements(plugins.IConfigurer)
    plugins.implements(plugins.IFacets, inherit=True)
    plugins.implements(plugins.IPackageController, inherit=True)

    # IConfigurer

    def update_config(self, config_):
        toolkit.add_template_directory(config_, 'templates')
        toolkit.add_public_directory(config_, 'public')
        toolkit.add_resource('fanstatic',
            'schemas')

    # IFacets

    def dataset_facets(self, facets_dict, package_type):
        if 'groups' in facets_dict:
            del facets_dict['groups']
        facets_dict['vocab_category'] = toolkit._('Category')
        facets_dict['sub_category'] = toolkit._('Sub Category')
        facets_dict['owner'] = toolkit._('Owner')
        facets_dict['vocab_web_services'] = toolkit._('Web services')
        return facets_dict

    def group_facets(self, facets_dict, group_type, package_type):
        return self.dataset_facets(facets_dict, package_type)

    def organization_facets(self, facets_dict, organization_type, package_type):
        return self.dataset_facets(facets_dict, package_type)


    # IPackageController

    def before_index(self, pkg_dict):
        for field in ('category', 'web_services'):
            data = pkg_dict.get(field)
            if data:
                try:
                    data = json.loads(data)
                except ValueError:
                    data = []
            else:
                data = []
            pkg_dict["vocab_"+field] = data
        return pkg_dict
