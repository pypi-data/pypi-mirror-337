# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['incant']

package_data = \
{'': ['*']}

install_requires = \
['click>=8.1.3,<9.0.0',
 'jinja2>=3.1.2,<4.0.0',
 'mako>=1.1.3,<2.0.0',
 'pyyaml>=6.0,<7.0']

entry_points = \
{'console_scripts': ['incant = incant.cli:cli']}

setup_kwargs = {
    'name': 'incus-incant',
    'version': '0.0.1',
    'description': '',
    'long_description': '# incant',
    'author': 'Lucas Nussbaum',
    'author_email': 'lucas@debian.org',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.11,<4.0',
}


setup(**setup_kwargs)
