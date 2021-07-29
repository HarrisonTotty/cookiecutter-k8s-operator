'''
Common Utility Functions
'''

import kopf
import kubernetes
import logging


def apply_resource(body: dict):
    '''
    Creates or updates the specified kubernetes resource, as if you had run
    `kubectl apply -f`.
    '''
    kind = body['kind']
    name = body['metadata']['name']
    namespace = body['metadata'].get('namespace')
    api = get_api(body['apiVersion'], kind)
    rstr = f'[{api.kind}] {namespace}/{name}'
    logging.debug(f'Checking if "{rstr}" already exists...')
    existing = get_resource(name=name, namespace=namespace, api=api)
    if existing is None:
        logging.info(f'Creating "{rstr}"...')
        apply_method = api.create
    else:
        logging.info(f'Patching "{rstr}"...')
        apply_method = api.patch
    try:
        if namespace is None:
            response = apply_method(body=body, name=name)
        else:
            response = apply_method(body=body, name=name, namespace=namespace)
    except Exception as e:
        logging.error(f'Unable to apply resource "{rstr}" - {e}')
        raise e
    return response


def delete_resource(name: str, namespace: str = None, body: dict = None, api = None, api_version: str = None, kind: str = None):
    '''
    Deletes the specified resource. Note that either `api` or `api_version` and
    `kind` must be specified. The body of the resource may be specified instead
    of `name` and `namespace`.
    '''
    if body is None:
        _api_version = api_version
        _kind        = kind
        _name        = name
        _namespace   = namespace
    else:
        _api_version = body['apiVersion']
        _kind        = body['kind']
        _name        = body['metadata']['name']
        _namespace   = body['metadata'].get('namespace')
    if api is None:
        api = get_api(_api_version, _kind)
    rstr = f'[{api.kind}] {_namespace}/{_name}'
    logging.info(f'Deleting "{rstr}"...')
    try:
        if _namespace is None:
            api.delete(body={}, name=_name)
        else:
            api.delete(body={}, name=_name, namespace=_namespace)
    except Exception as e:
        logging.error('Unable to delete "{rstr}" - {e}')
        raise e


def get_api(api_version: str, kind: str):
    '''
    Returns a dynamic API given the specified `api_version` and `kind`.
    '''
    client = kubernetes.dynamic.DynamicClient(kubernetes.client.ApiClient())
    return client.resources.get(api_version=api_version, kind=kind)


def get_resource(name: str, namespace: str = None, api = None, api_version: str = None, kind: str = None) -> dict:
    '''
    Gets the body of the specified resource, returning `None` if the resource
    can't be found. Note that either `api` and `api_version` and `kind` must be
    specified.
    '''
    if api is None:
        api = get_api(api_version, kind)
    rstr = f'[{api.kind}] {namespace}/{name}'
    existing = None
    logging.debug(f'Getting resource "{rstr}"...')
    try:
        if namespace is None:
            existing = api.get(name=name).to_dict()
        else:
            existing = api.get(name=name, namespace=namespace).to_dict()
    except kubernetes.client.ApiException as e:
        if e.reason == 'Not Found':
            logging.debug(f'Resource "{rstr}" does not exist.')
            pass
        else:
            logging.debug(f'Unable to get resource "{rstr}" - {e}')
    return existing
