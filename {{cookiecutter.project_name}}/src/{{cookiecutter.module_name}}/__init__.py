'''
{{ cookiecutter.project_title }}

{{ cookiecutter.project_desc }}
'''

__VERSION__ = "0.1.0"

import kopf
import kubernetes
import logging
import pkgutil
import yaml


@kopf.on.cleanup()
def cleanup(logger, **kwargs):
    '''
    Provides additional events to occur upon shutdown of the operator.
    '''
    logging.debug('Shutting down...')


@kopf.on.startup()
def startup(logger, **kwargs):
    '''
    Provides additional events to occur upon startup of the operator.
    '''
    logging.debug('Loading kubernetes client configuration...')
    try:
        kubernetes.config.load_kube_config()
    except Exception as e:
        raise Exception(f'Unable to handle operator startup - unable to load k8s config - {e}')
    logging.debug('Loading custom resource definition(s)...')
    try:
        data = yaml.safe_load_all(pkgutil.get_data(__name__, 'crds.yaml'))
    except Exception as e:
        raise Exception(f'Unable to handle operator startup - unable to load CRDs - {e}')
    logging.debug('Creating custom resource definition(s)...')
    try:
        client = kubernetes.client.ApiClient()
        kubernetes.utils.create_from_dict(client, data)
    except Exception as e:
        raise Exception(f'Unable to handle operator startup - unable to create CRDs - {e}')
