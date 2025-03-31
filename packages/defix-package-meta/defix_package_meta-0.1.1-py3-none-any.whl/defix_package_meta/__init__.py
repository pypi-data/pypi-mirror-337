from typing import Dict
from uuid import uuid4

initialized = False
name = None


def initialize(opts: Dict):
    global initialized, name

    if initialized:
        return

    if opts.get('name') is None or len(opts['name']) < 1:
        raise Exception('Service name is missing')

    name = opts['name']

    initialized = True


def generate_meta():
    if not initialized:
        raise Exception('Package meta is not initialized')

    return {
        'initializer': name,
        'service': name,
        'xid': str(uuid4())
    }


__all__ = ['initialize', 'generate_meta']
