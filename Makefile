.PHONY: all sdist wheel clean

all: sdist wheel

sdist:
	python3 setup.py sdist

wheel:
	python3 setup.py bdist_wheel

upload:
	find dist \
		-regex dist/curryproxy-[0-9]+\.[0-9]+\.[0-9]+\.tar.gz \
		-or -regex dist/curryproxy-[0-9]+\.[0-9]+\.[0-9]+-py3-none-any.whl \
		-print0 \
		xargs -0 twine -r curryproxy upload

clean:
	rm -rf build dist
