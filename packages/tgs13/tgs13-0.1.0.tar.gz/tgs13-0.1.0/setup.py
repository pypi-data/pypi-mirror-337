from setuptools import setup

setup(
    name='tgs13',
    version='0.1.0',
    description='Third tea package dependent on tgs11 and tgs12',
    url='https://github.com/ganisacik/tgs13',
    author='ganisacik',
    author_email='senin-email@example.com',
    packages=['tgs13'],
    install_requires=[
        'tgs11',
        'tgs12',
    ],
    project_urls={
        'Source': 'https://github.com/ganisacik/tgs13',
    },
)
