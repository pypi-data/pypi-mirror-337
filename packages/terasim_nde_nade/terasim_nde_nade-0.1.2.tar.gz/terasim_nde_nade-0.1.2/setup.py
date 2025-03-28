# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['terasim_nde_nade',
 'terasim_nde_nade.adversity',
 'terasim_nde_nade.adversity.static',
 'terasim_nde_nade.adversity.vehicles',
 'terasim_nde_nade.adversity.vru',
 'terasim_nde_nade.envs',
 'terasim_nde_nade.utils',
 'terasim_nde_nade.utils.adversity',
 'terasim_nde_nade.utils.agents',
 'terasim_nde_nade.utils.base',
 'terasim_nde_nade.utils.collision',
 'terasim_nde_nade.utils.geometry',
 'terasim_nde_nade.utils.nade',
 'terasim_nde_nade.utils.trajectory',
 'terasim_nde_nade.vehicle',
 'terasim_nde_nade.vru']

package_data = \
{'': ['*']}

install_requires = \
['Cython>=3.0.8',
 'hydra-core>=1.3.2',
 'loguru>=0.7.0',
 'omegaconf>=2.3.0',
 'shapely>=2.0.3',
 'toml>=0.10.2']

setup_kwargs = {
    'name': 'terasim_nde_nade',
    'version': '0.1.2',
    'description': 'TeraSim NDE NADE package',
    'long_description': 'None',
    'author': 'Haowei Sun',
    'author_email': 'haoweis@umich.edu',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/michigan-traffic-lab/TeraSim-NDE-ITE',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10',
}
from build import *
build(setup_kwargs)

setup(**setup_kwargs)
