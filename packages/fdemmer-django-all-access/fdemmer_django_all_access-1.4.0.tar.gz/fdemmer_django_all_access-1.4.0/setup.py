from pathlib import Path

from setuptools import find_packages, setup

VERSION = __import__('allaccess').__version__
github_url = 'https://github.com/fdemmer/django-all-access'


setup(
    name='fdemmer-django-all-access',
    version=VERSION,
    author='Florian Demmer',
    author_email='fdemmer@gmail.com',
    description=' '.join(__import__('allaccess').__doc__.splitlines()).strip(),
    long_description=(Path(__file__).parent.resolve() / 'README.rst').read_text(),
    download_url=f'{github_url}/archive/v{VERSION}.tar.gz',
    url=github_url,
    project_urls={
        'Changelog': f'{github_url}/blob/v{VERSION}/docs/releases.rst',
    },
    license='BSD',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Framework :: Django :: 3.2',
        'Framework :: Django :: 4.2',
        'Framework :: Django :: 5.0',
        'Framework :: Django :: 5.1',
        'Framework :: Django :: 5.2',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3 :: Only',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
        'Programming Language :: Python :: 3.13',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    packages=find_packages(),
    include_package_data=True,
    python_requires='>=3.8',
    setup_requires=['wheel'],
    install_requires=[
        'Django>=3.2',
        'pycryptodome>=3.9',
        'requests>=2.0',
        'requests_oauthlib>=0.4.2',
        'oauthlib>=0.6.2',
    ],
    extras_require={
        'cov': [
            'coverage[toml]~=6.0',
        ],
        'docs': [
            'sphinx',
        ],
    },
    options={'bdist_wheel': {'universal': '1'}},
)
