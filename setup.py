import os

from setuptools import setup


here = os.path.abspath(os.path.dirname(__file__))
README = open(os.path.join(here, 'README.md')).read()

setup(
    name='directus-api',
    description='Directus API',
    long_description=README,
    classifiers=[
      'Programming Language :: Python :: 3',
      'Programming Language :: Python :: 3.7',
    ],
    author='Volodymyr Trotsyhyn',
    author_email='devova@gmail.com',
    url='https://github.com/devova/directus-api',
    packages=['directus'],
    include_package_data=True,
    install_requires=open(os.path.join(here, 'requirements.txt')).read().splitlines(),
    zip_safe=True,
    entry_points={
        'console_scripts': [
            'directus-api=directus.manage:entry',
        ]
    },
    setup_requires=['setuptools_scm'],
    use_scm_version={'root': '.', 'relative_to': __file__}
)
