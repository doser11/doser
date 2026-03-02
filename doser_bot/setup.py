"""
Setup script for Doser
"""

from setuptools import setup, find_packages
from pathlib import Path

# Read README
readme_file = Path(__file__).parent / "README.md"
long_description = readme_file.read_text(encoding='utf-8') if readme_file.exists() else ""

# Read requirements
requirements_file = Path(__file__).parent / "requirements.txt"
requirements = []
if requirements_file.exists():
    requirements = [
        line.strip() 
        for line in requirements_file.read_text().split('\n')
        if line.strip() and not line.startswith('#')
    ]

setup(
    name='doser',
    version='1.0.0',
    description='Instagram Account Creator with GUI and CLI',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='Doser Team',
    author_email='support@doser.app',
    url='https://github.com/doser-team/doser',
    packages=find_packages(),
    include_package_data=True,
    install_requires=requirements,
    entry_points={
        'console_scripts': [
            'doser=main:main',
        ],
    },
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: End Users/Desktop',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.8',
    keywords='instagram automation account creator bot selenium',
    project_urls={
        'Bug Reports': 'https://github.com/doser-team/doser/issues',
        'Source': 'https://github.com/doser-team/doser',
    },
)
