'''
kind: {{ cookiecutter.crd_kind }}
'''

import asyncio
import kopf
import kubernetes

GROUP = '{{ cookiecutter.crd_group }}'
KIND  = '{{ cookiecutter.crd_kind }}'

@kopf.on.create(group=GROUP, kind=KIND, verison='v1')
async def create(body, **kwargs):
    '''
    Handles the creation of the associated custom resource.
    '''

@kopf.on.delete(group=GROUP, kind=KIND, verison='v1')
async def delete(body, **kwargs):
    '''
    Handles the deletion of the associated custom resource.
    '''

@kopf.on.resume(group=GROUP, kind=KIND, verison='v1')
async def resume(body, **kwargs):
    '''
    Handles resuming control of the associated custom resource after an operator
    restart.
    '''

@kopf.on.update(group=GROUP, kind=KIND, verison='v1')
async def update(body, **kwargs):
    '''
    Handles an update of the associated custom resource.
    '''
