CurryProxy Style Conventions
============================

- Code: [PEP 8](http://www.python.org/dev/peps/pep-0008/)
- Comments:
  - [PEP 257](http://www.python.org/dev/peps/pep-0257/)
  - [Comments](http://google-styleguide.googlecode.com/svn/trunk/pyguide.html?showone=Comments#Comments) section of Google's Python Style Guide.

Imports
-------

- See the [Imports formatting](http://google-styleguide.googlecode.com/svn/trunk/pyguide.html?showone=Imports_formatting#Imports_formatting) section of Google's Python Style Guide.
- Use `from x import y as z` if two modules named `y` are to be imported.

Managing Releases
=================

Dependencies
------------

If you've made changes that alter the dependency list, you will need to
update the appropriate files under `deps`, the dependency tests in
`tox.ini`, and possibly `.travis.yml`.

Whether you've made dep changes or not, you should update
`deps/pip.frozen.txt` with the latest available, working dependency
versions, which you can get like this:

```
virtualenv venv
. venv/bin/activate
pip install .
pip freeze | grep -v curryproxy
```
