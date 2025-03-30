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
    'version': '0.0.2',
    'description': '',
    'long_description': '# Incant\n\nIncant is a frontend for [Incus](https://linuxcontainers.org/incus/) that provides a descriptive way to define and manage development environments. It simplifies the creation, configuration, and provisioning of Incus instances using YAML-based configuration files.\n\nIncant is inspired by Vagrant, and intended as an Incus-based replacement for Vagrant.\n\n## Features\n\n- **Declarative Configuration**: Define your development environments using simple YAML files.\n- **Instance Management**: Easily create, start, stop, and destroy instances.\n- **Provisioning Support**: Run provisioning scripts automatically.\n- **Shared Folder Support**: Mount the current working directory into the instance.\n\n## Installation\n\nFIXME\n\nEnsure you have Python installed and `incus` available on your system.\n\n```sh\n# Clone the repository\n$ git clone https://github.com/your-repo/incant.git\n$ cd incant\n\n# Install dependencies\n$ pip install .\n```\n\n## Usage\n\n## Configure Incant\n\nIncant looks for a configuration file named `incant.yaml`, `incant.yaml.j2`, or `incant.yaml.mako` in the current directory. Here is an example:\n\n```yaml\ninstances:\n  my-instance:\n    image: ubuntu:22.04\n    vm: false # use a container, not a KVM virtual machine\n    provision:\n      - echo "Hello, World!"\n      - apt-get update && apt-get install -y curl\n```\n\n\n### Initialize and Start an Instance\n\n```sh\n$ incant up\n```\n\nor for a specific instance:\n\n```sh\n$ incant up my-instance\n```\n\n### Provision an Instance\n\n```sh\n$ incant provision\n```\n\nor for a specific instance:\n\n```sh\n$ incant provision my-instance\n```\n\n### Destroy an Instance\n\n```sh\n$ incant destroy\n```\n\nor for a specific instance:\n\n```sh\n$ incant destroy my-instance\n```\n\n### View Configuration (especially useful if you use Mako or Jinja2 templates)\n\n```sh\n$ incant dump\n```\n\n## Migrating from Vagrant\n\nIncant is inspired by Vagrant and shares some of its features.\n\nFIXME\n\n## License\n\nThis project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.\n\n',
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
