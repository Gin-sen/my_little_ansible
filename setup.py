from setuptools import setup, find_packages

setup(
    name='my_little_ansible',
    version='0.0.1',
    url='',
    license='',
    author='maxime.places',
    author_email='',
    description='',
    package_dir={"": "src"},
    packages=find_packages(
        where='src',
        include=['*'],  # alternatively: `exclude=['additional*']`
    ),
    entry_points={
        'console_scripts': [
            'mla = my_little_ansible:init_click_cmd',
        ]
    }
)
