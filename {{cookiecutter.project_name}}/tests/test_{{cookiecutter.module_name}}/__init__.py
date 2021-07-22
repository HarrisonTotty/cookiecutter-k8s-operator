'''
Operator Unit Tests
'''

import pkgutil
import pytest
import yaml

import {{ cookiecutter.module_name }} as op


def test_crds():
    '''
    Verifies that the custom resource definitions associated with this operator
    are valid.
    '''
    crd_text = pkgutil.get_data(op.__name__, 'crds.yaml')
    crd_data = yaml.safe_load_all(crd_text)
    for crd in crd_data:
        assert crd['apiVersion'] == 'apiextensions.k8s.io/v1'
        assert crd['kind'] == 'CustomResourceDefinition'
        assert isinstance(crd['metadata']['name'], str)
        spec = crd['spec']
        assert isinstance(spec['group'], str)
        assert isinstance(spec['names']['kind'], str)
        assert isinstance(spec['names']['plural'], str)
        assert isinstance(spec['names']['singular'], str)
        if 'categories' in spec['names']:
            assert isinstance(spec['names']['categories'], list)
        if 'shortNames' in spec['names']:
            assert isinstance(spec['names']['shortNames'], list)
        assert spec['scope'] in ['Namespaced', 'Cluster']
        assert isinstance(spec['versions'], list)
        assert len(spec['versions']) > 0
        for version in spec['versions']:
            assert isinstance(version['name'], str)
            assert isinstance(version['served'], bool)
            assert isinstance(version['schema'], dict)
            assert isinstance(version['schema']['openAPIV3Schema'], dict)
            assert isinstance(version['schema']['openAPIV3Schema']['properties'], dict)
            assert version['schema']['openAPIV3Schema']['type'] == 'object'
            assert isinstance(version['storage'], bool)
