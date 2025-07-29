# setup.py
from setuptools import setup, find_packages

setup(
    name='projectdoctor',
    version='1.0.0',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'click',
        'radon',
        'astroid',
        'vulture',
    ],
    entry_points={
        'console_scripts': [
            'projectdoctor = projectdoctor.cli:cli',
        ],
    },
)
