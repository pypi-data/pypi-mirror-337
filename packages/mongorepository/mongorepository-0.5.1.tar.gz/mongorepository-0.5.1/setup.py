# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['mongorepository', 'mongorepository.repositories', 'mongorepository.utils']

package_data = \
{'': ['*']}

install_requires = \
['motor>=3.1.1,<4.0.0']

setup_kwargs = {
    'name': 'mongorepository',
    'version': '0.5.1',
    'description': '',
    'long_description': '# Mongo Repository\n\nThis package provide a sync and async repositories utilities for mongodb.',
    'author': 'Ramon Rodrigues',
    'author_email': 'ramon.srodrigues01@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
