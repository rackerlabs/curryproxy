import os
import setuptools

requires = os.path.join('tools', 'pip-requires')

setuptools.setup(
    name='curryproxy',
    version='0.1',
    description='Proxy for globally distributed APIs',
    license="TBD",
    author='Bryan Davidson',
    author_email='bryan.davidson@rackspace.com',
    url='https://github.com/rackerlabs/Curry',
    packages=setuptools.find_packages(
        exclude=['bin', "*.tests", "*.tests.*", "tests.*", "tests"]),
    include_package_data=True,
    test_suite='nose.collector',
    install_requires=open(requires).read().splitlines()
)
