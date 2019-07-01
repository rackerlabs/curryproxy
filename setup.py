# Copyright (c) 2013 Rackspace, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or
# implied.
# See the License for the specific language governing permissions and
# limitations under the License.
from setuptools import find_packages
from setuptools import setup


def readdeps(filename):
    """ Get a dependency list from a file.

        Filters out comments and blank lines, so the result is suitable
        to feed to setup() args.
    """

    with open(filename) as f:
        return [line for line in f
                if line and not line.startswith("#")]

# Load dependencies
deps = {"install": readdeps("deps/pip.install.txt"),
        "frozen" : readdeps("deps/pip.frozen.txt"),
        "tests"  : readdeps("deps/pip.tests.txt")}

setup(
    name='curryproxy',
    setup_requires=['setuptools_scm'],
    use_scm_version={'write_to': 'curryproxy/version.txt'},
    description='A proxy and aggregator for querying multiple instances of an '
    'API spread across globally distributed data centers.',
    long_description=open('README.rst').read(),
    author='Bryan Davidson',
    author_email='bryan.davidson@rackspace.com',
    url='https://github.com/rackerlabs/curryproxy',
    packages=find_packages(),
    install_requires=deps['install'],
    license='Apache 2.0',
    tests_require=deps['tests'],
    extras_require={'tests': deps['tests'],
                    'frozen': deps['frozen']},
    test_suite='nose.collector',
    classifiers=(
        'Development Status :: 5 - Production/Stable',
        'License :: OSI Approved :: Apache Software License',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Topic :: Internet :: Proxy Servers',
        'Topic :: Internet :: WWW/HTTP :: WSGI :: Application',
        'Topic :: Software Development :: Libraries :: Python Modules'
    )
)
