'''
{{ cookiecutter.project_title }}

{{ cookiecutter.project_desc }}
'''

__VERSION__ = "0.1.0"

import kopf
import kubernetes
import logging
import os
import pkgutil
import yaml

from . import utils


@kopf.on.cleanup()
def cleanup(logger, **kwargs):
    '''
    Provides additional events to occur upon shutdown of the operator.
    '''
    logging.debug('Shutting down...')


@kopf.on.login()
def login(**kwargs):
    '''
    Handles cluster authentication.
    '''
    logging.debug('Authenticating with kubernetes...')
    return kopf.login_with_service_account(**kwargs) or kopf.login_with_kubeconfig(**kwargs)


@kopf.on.startup()
def startup(settings: kopf.OperatorSettings, **kwargs):
    '''
    Provides additional events to occur upon startup of the operator.
    '''
    logging.debug('Loading initial kubernetes cluster configuration...')
    try:
        if os.getenv('KUBECONFIG', '') or os.path.exists(os.path.expanduser('~/.kube/config')):
            logging.debug('Loading local cluster configuration...')
            kubernetes.config.load_kube_config()
        else:
            logging.debug('Loading cluster configuration from service account...')
            kubernetes.config.load_incluster_config()
    except Exception as e:
        raise Exception(f'Unable to load initial kubernetes cluster configuration - {e}')
    logging.debug('Loading custom resource definition(s)...')
    try:
        crds = list(yaml.safe_load_all(pkgutil.get_data(__name__, 'crds.yaml')))
    except Exception as e:
        raise Exception(f'Unable to handle operator startup - unable to load CRDs - {e}')
    logging.debug('Creating custom resource definition(s)...')
    try:
        for crd in crds:
            utils.apply_resource(crd)
    except Exception as e:
        raise Exception(f'Unable to handle operator startup - unable to create CRDs - {e}')
